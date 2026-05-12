"""
blast_parallel.py — Parallel BLAST via NCBI's REST API directly.

Submits all jobs simultaneously (respecting 3 req/s rate limit),
then polls all in parallel, collects results concurrently.
~5-10x faster than serial NCBIWWW.qblast.

Safe to interrupt and resume — only blast_genus IS NULL rows queried.
"""

import sqlite3, time, sys, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

DB_PATH  = r'C:\repos\eDNA-20270420\edna.db'
EMAIL    = 'geofday@gmail.com'
BLAST_URL = 'https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi'
SUBMIT_DELAY = 0.4   # 2.5 submissions/sec — under NCBI's 3/sec limit
POLL_INTERVAL = 8    # seconds between status polls per job
MAX_POLL_WAIT = 300  # 5 minutes max per job

submit_lock = threading.Lock()
last_submit = [0.0]  # mutable for closure


def get_conn():
    return sqlite3.connect(DB_PATH)


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


def load_targets(conn):
    def q(sql): return conn.execute(sql).fetchall()

    verts = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.class IN ('Mammalia','Aves','Amphibia','Hyperoartia')
          AND e.blast_genus IS NULL
          AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
    """)

    algae = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.assay='23S' AND e.blast_genus IS NULL
          AND (e.class IS NULL OR e.genus IS NULL)
          AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
        LIMIT 50
    """)

    fish = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2 WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.class='Actinopteri' AND e.blast_genus IS NULL
          AND (e.species IS NULL OR e.n_species IS NULL OR e.n_species > 1)
          AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
        LIMIT 30
    """)

    return (
        [('VERTEBRATE', r) for r in verts] +
        [('23S',        r) for r in algae] +
        [('FISH',       r) for r in fish]
    )


ENTREZ_FILTER = {
    'Mammalia':    'Mammalia[Organism]',
    'Aves':        'Aves[Organism]',
    'Amphibia':    'Amphibia[Organism]',
    'Hyperoartia': 'Petromyzontiformes[Organism]',
    'Actinopteri': 'Actinopterygii[Organism]',
}


def submit_blast(seq, cls):
    """Submit to NCBI BLAST, return RID. Rate-limited to SUBMIT_DELAY between calls."""
    entrez_q = ENTREZ_FILTER.get(cls, '')

    with submit_lock:
        wait = SUBMIT_DELAY - (time.time() - last_submit[0])
        if wait > 0:
            time.sleep(wait)
        last_submit[0] = time.time()

        r = requests.post(BLAST_URL, data={
            'CMD':         'Put',
            'PROGRAM':     'blastn',
            'DATABASE':    'nt',
            'QUERY':       seq,
            'ENTREZ_QUERY': entrez_q,
            'EMAIL':       EMAIL,
            'HITLIST_SIZE': '5',
            'EXPECT':      '1e-10',
            'FORMAT_TYPE': 'XML',
            'WORD_SIZE':   '11',
        }, timeout=30)
        r.raise_for_status()

    # Extract RID from response HTML
    m = re.search(r'RID\s*=\s*([A-Z0-9]+)', r.text)
    if not m:
        raise ValueError('No RID in NCBI response')
    return m.group(1)


def poll_and_fetch(rid):
    """Poll until complete, return XML result string."""
    deadline = time.time() + MAX_POLL_WAIT
    while time.time() < deadline:
        r = requests.get(BLAST_URL, params={
            'CMD': 'Get', 'FORMAT_OBJECT': 'SearchInfo', 'RID': rid
        }, timeout=15)
        r.raise_for_status()

        if 'Status=WAITING' in r.text:
            time.sleep(POLL_INTERVAL)
            continue
        if 'Status=FAILED' in r.text or 'Status=UNKNOWN' in r.text:
            raise ValueError(f'BLAST job {rid} failed/expired')
        if 'Status=READY' in r.text:
            break
        time.sleep(POLL_INTERVAL)
    else:
        raise TimeoutError(f'Job {rid} timed out after {MAX_POLL_WAIT}s')

    xml_r = requests.get(BLAST_URL, params={
        'CMD': 'Get', 'FORMAT_TYPE': 'XML', 'RID': rid, 'ALIGNMENTS': '5'
    }, timeout=60)
    xml_r.raise_for_status()
    return xml_r.text


def parse_blast_xml(xml):
    """Extract best genus, species, pct_id from NCBI XML."""
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
    if m:
        genus   = m.group(1)
        species = m.group(1) + ' ' + m.group(2)
    else:
        genus, species = None, title[:80]
    return genus, species, pct


def process_one(row_tuple):
    group, (esv_id, assay, cls, genus, species, seq, reads, n_sites) = row_tuple
    reads  = reads or 0
    jv_id  = f'{genus or "?"} {species or "?"}'.strip()

    try:
        rid    = submit_blast(seq, cls)
        xml    = poll_and_fetch(rid)
        bg, bs, bp = parse_blast_xml(xml)

        if bg:
            notes = ('confirmed'      if genus and bg == genus else
                     f'JV={genus}, BLAST={bg} — MISMATCH' if genus else
                     'newly resolved')
        else:
            bg = bs = None
            notes = 'no hit'

        c = get_conn()
        c.execute("UPDATE esvs SET blast_genus=?, blast_species=?, blast_pct=?, blast_notes=? WHERE esv_id=? AND assay=?",
                  (bg, bs, bp, notes, esv_id, assay))
        c.commit(); c.close()

        return {'group': group, 'esv_id': esv_id, 'cls': cls or '?',
                'jv': jv_id, 'reads': reads, 'sites': n_sites,
                'blast': bs or '(no hit)', 'pct': bp, 'notes': notes}

    except Exception as e:
        try:
            c = get_conn()
            c.execute("UPDATE esvs SET blast_notes=? WHERE esv_id=? AND assay=?",
                      (f'BLAST error: {str(e)[:200]}', esv_id, assay))
            c.commit(); c.close()
        except Exception:
            pass
        return {'esv_id': esv_id, 'error': str(e)[:80], 'jv': jv_id, 'reads': reads}


# ── Main ──────────────────────────────────────────────────────────────────────

conn = get_conn()
pre_mark_artifacts(conn)
targets = load_targets(conn)
conn.close()

if not targets:
    print('All priority ESVs already blasted. Done.')
    sys.exit(0)

# Estimate: submit all over ~N/2.5 sec, then ~90s processing = ~N/2.5 + 90s total
est_sec = len(targets) / 2.5 + 90
print(f'\nTargets: {len(targets)}  |  Submitting at 2.5/sec, parallel polling')
print(f'Estimated runtime: {est_sec/60:.1f} min\n')

results = []
done    = 0

# Use enough workers to keep all jobs polling concurrently while submissions stagger
with ThreadPoolExecutor(max_workers=min(len(targets), 30)) as executor:
    futures = {executor.submit(process_one, t): t for t in targets}
    for future in as_completed(futures):
        done += 1
        r = future.result()
        results.append(r)

        if 'error' in r:
            print(f'[{done:3}/{len(targets)}]  {r["esv_id"]:12}  ERROR: {r["error"]}')
        else:
            flag = '  *** MISMATCH' if 'MISMATCH' in r.get('notes','') else ''
            print(f'[{done:3}/{len(targets)}]  {r["esv_id"]:12}  {r["reads"]:>8,}r  '
                  f'JV={r["jv"][:22]:22}  =>  {str(r.get("pct","?"))[:5]:5}%  '
                  f'{r["blast"][:45]}{flag}')
        sys.stdout.flush()

# ── Summary ───────────────────────────────────────────────────────────────────

ok         = [r for r in results if 'error' not in r]
mismatches = [r for r in ok if 'MISMATCH' in r.get('notes','')]
resolved   = [r for r in ok if r.get('notes') == 'newly resolved']
confirmed  = [r for r in ok if r.get('notes') == 'confirmed']
no_hits    = [r for r in ok if r.get('blast') == '(no hit)']
errors     = [r for r in results if 'error' in r]

print(f'\n{"="*80}')
print('PARALLEL BLAST SUMMARY')
print(f'{"="*80}')
print(f'  Confirmed:      {len(confirmed):3}')
print(f'  Mismatches:     {len(mismatches):3}')
print(f'  Newly resolved: {len(resolved):3}')
print(f'  No hits:        {len(no_hits):3}')
print(f'  Errors:         {len(errors):3}')

if mismatches:
    print('\n*** MISMATCHES — review these ***')
    for r in sorted(mismatches, key=lambda x: -x['reads']):
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['notes']}")
        print(f"    BLAST: {r['pct']}%  {r['blast']}")

if resolved:
    print('\n--- Newly resolved ---')
    for r in sorted(resolved, key=lambda x: -x['reads']):
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  cls={str(r['cls'])[:18]:18}  BLAST: {r['pct']}%  {r['blast']}")

print('\nDone.')
