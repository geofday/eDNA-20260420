"""
blast_ebi.py — BLAST all unresolved ESVs via EBI's async REST API.

Submits up to 25 jobs simultaneously to EBI's NCBI BLAST cluster,
polls all in parallel, writes results to DB as they arrive.

Target priority:
  1. All vertebrate non-fish (Mammalia, Aves, Amphibia, Hyperoartia)
  2. Top 50 unresolved 23S (NULL class or NULL genus, by read count)
  3. Top 30 genus-only / multi-species Actinopteri fish

Safe to interrupt and resume — only blast_genus IS NULL rows are queried.

EBI BLAST REST API: https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/
Rate limits: 25 concurrent jobs per user; poll every 5s minimum.
"""

import sqlite3, time, sys, re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DB_PATH  = r'C:\repos\eDNA-20270420\edna.db'
EMAIL    = 'geofday@gmail.com'
EBI_BASE = 'https://www.ebi.ac.uk/Tools/services/rest/ncbiblast'
MAX_CONCURRENT = 20   # stay under EBI's 25-job limit
POLL_INTERVAL  = 6    # seconds between status polls

# Entrez/organism filter per class — passed as 'exp' filter to EBI
# EBI uses 'database' param; we steer via sequence + database choice
ENTREZ_HINT = {
    'Mammalia':    'Mammalia[Organism]',
    'Aves':        'Aves[Organism]',
    'Amphibia':    'Amphibia[Organism]',
    'Hyperoartia': 'Petromyzontiformes[Organism]',
    'Actinopteri': 'Actinopterygii[Organism]',
}


# ── DB helpers ────────────────────────────────────────────────────────────────

def get_conn():
    return sqlite3.connect(DB_PATH)


def pre_mark_artifacts(conn):
    """Mark known artifacts without BLASTing."""
    n1 = conn.execute("""
        UPDATE esvs SET blast_genus='Struthio', blast_species='Struthio camelus',
                        blast_pct=NULL,
                        blast_notes='JV PositiveControl artifact (ostrich DNA)'
        WHERE genus='Struthio' AND species='Struthio camelus'
          AND blast_genus IS NULL
    """).rowcount
    n2 = conn.execute("""
        UPDATE esvs SET blast_genus='Homo', blast_species='Homo sapiens',
                        blast_pct=NULL, blast_notes='Human field contamination'
        WHERE genus='Homo' AND species='Homo sapiens'
          AND blast_genus IS NULL
    """).rowcount
    conn.commit()
    if n1: print(f'Pre-marked {n1} Struthio (PositiveControl) ESVs')
    if n2: print(f'Pre-marked {n2} Homo sapiens (human contamination) ESVs')


def load_targets(conn):
    """Return all unblasted ESVs in priority order."""

    def q(sql):
        return conn.execute(sql).fetchall()

    verts = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.class IN ('Mammalia','Aves','Amphibia','Hyperoartia')
          AND e.blast_genus IS NULL
          AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
    """)

    algae = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.assay='23S'
          AND e.blast_genus IS NULL
          AND (e.class IS NULL OR e.genus IS NULL)
          AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
        ORDER BY total_reads DESC
        LIMIT 50
    """)

    fish = q("""
        SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
               (SELECT SUM(r2.read_count) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
               (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
                WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
        FROM esvs e
        WHERE e.class='Actinopteri'
          AND e.blast_genus IS NULL
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


# ── EBI BLAST helpers ─────────────────────────────────────────────────────────

def submit_job(seq, cls):
    """Submit one BLAST job to EBI. Returns job_id or raises."""
    # For algae (23S) use EMBL ENA; for everything else NCBI nt
    database = 'em_rel_std' if cls in (None, 'Bacillariophyceae', 'Bacillariophyta') else 'nt'

    params = {
        'email':      EMAIL,
        'program':    'blastn',
        'database':   database,
        'sequence':   seq,
        'stype':      'dna',
        'exp':        '1e-10',
        'scores':     '5',
        'alignments': '5',
        'format':     'xml',
    }
    r = requests.post(f'{EBI_BASE}/run', data=params, timeout=30)
    r.raise_for_status()
    return r.text.strip()


def poll_job(job_id, timeout=300):
    """Poll until FINISHED/FAILED. Returns status string."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f'{EBI_BASE}/status/{job_id}', timeout=15)
        r.raise_for_status()
        status = r.text.strip()
        if status in ('FINISHED', 'FAILED', 'ERROR', 'NOT_FOUND'):
            return status
        time.sleep(POLL_INTERVAL)
    return 'TIMEOUT'


def fetch_result_xml(job_id):
    """Fetch XML result for a finished job."""
    r = requests.get(f'{EBI_BASE}/result/{job_id}/xml', timeout=30)
    r.raise_for_status()
    return r.text


def parse_xml(xml_text):
    """Extract best genus, species, pct_id from BLAST XML. Returns (genus, species, pct)."""
    # Lightweight regex parse — avoids importing BioPython XML which needs file handle
    hits = re.findall(
        r'<Hit_def>(.*?)</Hit_def>.*?'
        r'<Hsp_identity>(\d+)</Hsp_identity>.*?'
        r'<Hsp_align-len>(\d+)</Hsp_align-len>',
        xml_text, re.DOTALL
    )
    if not hits:
        return None, None, None

    title, ident, alen = hits[0]
    pct = round(100 * int(ident) / int(alen), 1)

    # Parse genus/species from hit title
    m = re.search(r'([A-Z][a-z]+)\s+([a-z]+(?:\s+[a-z]+)?)', title)
    if m:
        genus   = m.group(1)
        species = m.group(1) + ' ' + m.group(2)
    else:
        genus   = None
        species = title[:80]

    return genus, species, pct


def save_result(conn, esv_id, assay, jv_genus, blast_genus, blast_species, blast_pct, notes):
    conn.execute("""
        UPDATE esvs SET blast_genus=?, blast_species=?, blast_pct=?, blast_notes=?
        WHERE esv_id=? AND assay=?
    """, (blast_genus, blast_species, blast_pct, notes, esv_id, assay))
    conn.commit()


# ── Worker: submit → poll → parse → save ─────────────────────────────────────

def process_one(row_tuple):
    """Run in a thread pool. Returns summary dict."""
    group, (esv_id, assay, cls, genus, species, seq, reads, n_sites) = row_tuple
    reads = reads or 0
    jv_id = f'{genus or "?"} {species or "?"}'.strip()

    try:
        job_id = submit_job(seq, cls)
        status = poll_job(job_id)

        if status != 'FINISHED':
            return {'esv_id': esv_id, 'error': f'Job {status}', 'jv': jv_id, 'reads': reads}

        xml = fetch_result_xml(job_id)
        blast_genus, blast_species, blast_pct = parse_xml(xml)

        if blast_genus:
            if genus and blast_genus != genus:
                notes = f'JV={genus}, BLAST={blast_genus} — MISMATCH'
            elif genus:
                notes = 'confirmed'
            else:
                notes = 'newly resolved'
        else:
            blast_genus = blast_species = None
            notes = 'no hit'

        conn = get_conn()
        save_result(conn, esv_id, assay, genus, blast_genus, blast_species, blast_pct, notes)
        conn.close()

        return {
            'group': group, 'esv_id': esv_id, 'cls': cls or '?',
            'jv': jv_id, 'reads': reads, 'sites': n_sites,
            'blast': blast_species or '(no hit)', 'pct': blast_pct,
            'notes': notes,
        }

    except Exception as e:
        try:
            conn = get_conn()
            conn.execute("UPDATE esvs SET blast_notes=? WHERE esv_id=? AND assay=?",
                         (f'EBI error: {str(e)[:200]}', esv_id, assay))
            conn.commit()
            conn.close()
        except Exception:
            pass
        return {'esv_id': esv_id, 'error': str(e), 'jv': jv_id, 'reads': reads}


# ── Main ──────────────────────────────────────────────────────────────────────

conn = get_conn()
pre_mark_artifacts(conn)
targets = load_targets(conn)
conn.close()

print(f'\nTotal targets: {len(targets)}  (running {MAX_CONCURRENT} concurrent)')
print(f'Estimated time: {max(1, len(targets) // MAX_CONCURRENT) * 20 // 60 + 1} min\n')

results = []
done = 0

with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
    futures = {executor.submit(process_one, t): t for t in targets}
    for future in as_completed(futures):
        done += 1
        r = future.result()
        results.append(r)

        if 'error' in r:
            print(f'[{done}/{len(targets)}]  {r["esv_id"]:12}  ERROR: {r["error"][:60]}')
        else:
            flag = '  *** MISMATCH' if 'MISMATCH' in r.get('notes','') else ''
            print(f'[{done}/{len(targets)}]  {r["esv_id"]:12}  {r["reads"]:>8,}r  '
                  f'JV={r["jv"][:25]:25}  =>  {r.get("pct","?")!s:5}%  '
                  f'{r["blast"][:45]}{flag}')
        sys.stdout.flush()

# ── Summary ───────────────────────────────────────────────────────────────────

print('\n' + '='*80)
print('EBI BLAST RESULTS SUMMARY')
print('='*80)

ok        = [r for r in results if 'error' not in r]
mismatches = [r for r in ok if 'MISMATCH' in r.get('notes','')]
resolved   = [r for r in ok if r.get('notes') == 'newly resolved']
confirmed  = [r for r in ok if r.get('notes') == 'confirmed']
no_hits    = [r for r in ok if r.get('blast') == '(no hit)']
errors     = [r for r in results if 'error' in r]

print(f'\n  Confirmed (JV=BLAST):   {len(confirmed):3}')
print(f'  Mismatches:             {len(mismatches):3}')
print(f'  Newly resolved:         {len(resolved):3}')
print(f'  No hits:                {len(no_hits):3}')
print(f'  Errors:                 {len(errors):3}')

if mismatches:
    print('\n*** MISMATCHES ***')
    for r in sorted(mismatches, key=lambda x: -x['reads']):
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['notes']}")
        print(f"    BLAST: {r['pct']}%  {r['blast']}")

if resolved:
    print('\n--- Newly resolved ---')
    for r in sorted(resolved, key=lambda x: -x['reads']):
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  cls={str(r['cls'])[:20]:20}  "
              f"BLAST: {r['pct']}%  {r['blast']}")

print('\nDone.')
