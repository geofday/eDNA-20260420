"""
blast_all.py — BLAST the entire unblasted ESV corpus via NCBI parallel REST API.

Submits every unblasted ESV with a sequence. No sampling, no priority cutoffs.
Submissions staggered at 0.5/sec (safe under NCBI's 3/sec registered limit).
All jobs poll concurrently — wall time ~30 min for ~3,300 ESVs.

Safe to interrupt and resume — only blast_genus IS NULL rows are targeted.
Results written to DB per-job as they complete.
"""

import sqlite3, time, sys, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

DB_PATH       = r'C:\repos\eDNA-20270420\edna.db'
EMAIL         = 'geofday@gmail.com'
BLAST_URL     = 'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi'
SUBMIT_DELAY  = 0.5    # seconds between submissions (2/sec — well under 3/sec limit)
POLL_INTERVAL = 10     # seconds between status polls per job
MAX_POLL_WAIT = 600    # 10 min max per job before giving up
MAX_WORKERS   = 200    # concurrent polling threads

submit_lock  = threading.Lock()
last_submit  = [0.0]
print_lock   = threading.Lock()
counter      = [0]

# Organism filter speeds up search and improves accuracy for known classes
ENTREZ_FILTER = {
    'Mammalia':         'Mammalia[Organism]',
    'Aves':             'Aves[Organism]',
    'Amphibia':         'Amphibia[Organism]',
    'Hyperoartia':      'Petromyzontiformes[Organism]',
    'Actinopteri':      'Actinopterygii[Organism]',
    'Bacillariophyceae':'Bacillariophyta[Organism]',
    'Bacillariophyta':  'Bacillariophyta[Organism]',
    'Fragilariophyceae':'Bacillariophyta[Organism]',
    'Coscinodiscophyceae':'Bacillariophyta[Organism]',
    'Mediophyceae':     'Bacillariophyta[Organism]',
}


def get_conn():
    return sqlite3.connect(DB_PATH, timeout=30)


def pre_mark_artifacts(conn):
    n1 = conn.execute("""
        UPDATE esvs SET blast_genus='Struthio', blast_species='Struthio camelus',
            blast_pct=NULL, blast_notes='JV PositiveControl artifact (ostrich DNA)'
        WHERE genus='Struthio' AND species='Struthio camelus' AND blast_genus IS NULL
    """).rowcount
    n2 = conn.execute("""
        UPDATE esvs SET blast_genus='Homo', blast_species='Homo sapiens',
            blast_pct=NULL, blast_notes='Human field contamination'
        WHERE genus='Homo' AND species='Homo sapiens' AND blast_genus IS NULL
    """).rowcount
    conn.commit()
    if n1: print(f'Pre-marked {n1} Struthio (PositiveControl) ESVs')
    if n2: print(f'Pre-marked {n2} Homo sapiens ESVs')


def load_all_targets(conn):
    """Load every unblasted ESV that has a sequence."""
    rows = conn.execute("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               COALESCE(
                   (SELECT SUM(r2.read_count) FROM reads r2
                    WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay), 0
               ) as total_reads,
               COALESCE(
                   (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
                    WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay), 0
               ) as n_sites
        FROM esvs e
        WHERE e.blast_genus IS NULL
          AND e.sequence IS NOT NULL
          AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
    """).fetchall()
    return rows


def submit_blast(seq, cls):
    """Submit to NCBI, return RID. Rate-limited by submit_lock."""
    entrez_q = ENTREZ_FILTER.get(cls or '', '')

    with submit_lock:
        gap = SUBMIT_DELAY - (time.time() - last_submit[0])
        if gap > 0:
            time.sleep(gap)
        last_submit[0] = time.time()

        for attempt in range(3):
            try:
                r = requests.post(BLAST_URL, data={
                    'CMD':          'Put',
                    'PROGRAM':      'blastn',
                    'DATABASE':     'nt',
                    'QUERY':        seq,
                    'ENTREZ_QUERY': entrez_q,
                    'EMAIL':        EMAIL,
                    'HITLIST_SIZE': '3',
                    'EXPECT':       '1e-10',
                    'FORMAT_TYPE':  'XML',
                    'WORD_SIZE':    '11',
                }, timeout=30)
                r.raise_for_status()
                m = re.search(r'RID\s*=\s*([A-Z0-9]+)', r.text)
                if m:
                    return m.group(1)
                raise ValueError('No RID in response')
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))


def poll_and_fetch(rid):
    """Poll until READY, return XML."""
    deadline = time.time() + MAX_POLL_WAIT
    while time.time() < deadline:
        r = requests.get(BLAST_URL, params={
            'CMD': 'Get', 'FORMAT_OBJECT': 'SearchInfo', 'RID': rid
        }, timeout=20)
        r.raise_for_status()
        txt = r.text
        if 'Status=WAITING' in txt:
            time.sleep(POLL_INTERVAL)
            continue
        if 'Status=FAILED' in txt or 'Status=UNKNOWN' in txt:
            raise ValueError(f'Job {rid} failed/expired')
        if 'Status=READY' in txt:
            xml_r = requests.get(BLAST_URL, params={
                'CMD': 'Get', 'FORMAT_TYPE': 'XML',
                'RID': rid, 'ALIGNMENTS': '3'
            }, timeout=60)
            xml_r.raise_for_status()
            return xml_r.text
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f'Job {rid} timed out')


def parse_xml(xml):
    hits = re.findall(
        r'<Hit_def>(.*?)</Hit_def>.*?'
        r'<Hsp_identity>(\d+)</Hsp_identity>.*?'
        r'<Hsp_align-len>(\d+)</Hsp_align-len>',
        xml, re.DOTALL
    )
    if not hits:
        return None, None, None
    title, ident, alen = hits[0]
    pct = round(100 * int(ident) / int(alen), 1)
    m = re.search(r'([A-Z][a-z]+)\s+([a-z]+(?:\s+[a-z]+)?)', title)
    genus   = m.group(1)   if m else None
    species = (m.group(1) + ' ' + m.group(2)) if m else title[:80]
    return genus, species, pct


def process_one(row, total):
    esv_id, assay, cls, genus, species, seq, reads, n_sites = row
    jv_id = f'{genus or "?"} {species or "?"}'.strip()

    try:
        rid  = submit_blast(seq, cls)
        xml  = poll_and_fetch(rid)
        bg, bs, bp = parse_xml(xml)

        notes = ('confirmed'      if genus and bg and bg == genus  else
                 f'JV={genus}, BLAST={bg} — MISMATCH' if genus and bg and bg != genus else
                 'newly resolved' if bg else
                 'no hit')
        if not bg:
            bg = bs = None

    except Exception as e:
        bg = bs = bp = None
        notes = f'error: {str(e)[:150]}'

    try:
        c = get_conn()
        c.execute("""UPDATE esvs SET blast_genus=?, blast_species=?, blast_pct=?, blast_notes=?
                     WHERE esv_id=? AND assay=?""",
                  (bg, bs, bp, notes, esv_id, assay))
        c.commit(); c.close()
    except Exception:
        pass

    with print_lock:
        counter[0] += 1
        n = counter[0]
        flag = '  *** MISMATCH' if 'MISMATCH' in notes else ''
        err  = '  ERROR'        if notes.startswith('error') else ''
        print(f'[{n:4}/{total}]  {esv_id:12}  {reads:>8,}r  '
              f'JV={jv_id[:20]:20}  =>  {str(bp or "?")[:5]:5}%  '
              f'{(bs or "(no hit)")[:45]}{flag}{err}')
        sys.stdout.flush()

    return {'esv_id': esv_id, 'reads': reads, 'jv': jv_id,
            'blast': bs, 'pct': bp, 'notes': notes}


# ── Main ──────────────────────────────────────────────────────────────────────

conn = get_conn()
pre_mark_artifacts(conn)
targets = load_all_targets(conn)
conn.close()

if not targets:
    print('All ESVs already blasted.')
    sys.exit(0)

total = len(targets)
est_min = (total * SUBMIT_DELAY + 90) / 60
print(f'\nFull corpus: {total} ESVs')
print(f'Submitting at {1/SUBMIT_DELAY:.1f}/sec  |  {MAX_WORKERS} concurrent pollers')
print(f'Estimated wall time: {est_min:.0f} min\n')

start = time.time()
results = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futures = {ex.submit(process_one, row, total): row for row in targets}
    for future in as_completed(futures):
        results.append(future.result())

elapsed = (time.time() - start) / 60

# ── Final summary ─────────────────────────────────────────────────────────────

ok         = [r for r in results if not r['notes'].startswith('error')]
mismatches = [r for r in ok if 'MISMATCH' in r['notes']]
resolved   = [r for r in ok if r['notes'] == 'newly resolved']
confirmed  = [r for r in ok if r['notes'] == 'confirmed']
no_hits    = [r for r in ok if r['notes'] == 'no hit']
errors     = [r for r in results if r['notes'].startswith('error')]

print(f'\n{"="*80}')
print(f'FULL CORPUS BLAST — {total} ESVs in {elapsed:.1f} min')
print(f'{"="*80}')
print(f'  Confirmed:       {len(confirmed):4}')
print(f'  Mismatches:      {len(mismatches):4}')
print(f'  Newly resolved:  {len(resolved):4}')
print(f'  No hits:         {len(no_hits):4}')
print(f'  Errors:          {len(errors):4}')

if mismatches:
    print('\n*** MISMATCHES — JV vs BLAST disagree ***')
    for r in sorted(mismatches, key=lambda x: -(x['reads'] or 0)):
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['notes']}")
        print(f"    BLAST {r['pct']}%  {r['blast']}")

print('\nTop 30 newly resolved by read count:')
for r in sorted(resolved, key=lambda x: -(x['reads'] or 0))[:30]:
    print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['pct']}%  {r['blast']}")

print('\nDone.')
