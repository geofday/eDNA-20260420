"""
blast_diatoms.py — BLAST unresolved diatom ESVs against NCBI nt database.
Targets 23S ESVs with class=Bacillariophyta but no genus assignment.
"""

import sqlite3, time, sys
from Bio.Blast import NCBIWWW, NCBIXML

DB_PATH = r'C:\repos\eDNA-20270420\edna.db'
EMAIL   = 'geofday@gmail.com'
TOP_N   = 10   # number of ESVs to BLAST

conn = sqlite3.connect(DB_PATH)

# Pull top unresolved diatom ESVs by total reads
esv_rows = conn.execute("""
    SELECT e.esv_id, e.class, e.perc_match, e.sequence,
           SUM(r.read_count) as total_reads,
           COUNT(DISTINCT r.sample_code) as n_sites,
           GROUP_CONCAT(DISTINCT s.canonical_site) as sites
    FROM esvs e
    JOIN reads r ON e.esv_id=r.esv_id AND e.assay=r.assay
    JOIN samples s ON r.sample_code=s.sample_code
    WHERE e.assay='23S'
      AND e.phylum='Bacillariophyta'
      AND (e.genus IS NULL OR e.genus='')
      AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
    GROUP BY e.esv_id
    ORDER BY total_reads DESC
    LIMIT ?
""", (TOP_N,)).fetchall()

conn.close()

print(f'BLASTing {len(esv_rows)} unresolved diatom ESVs against NCBI nt...')
print('(~30-90 seconds per query — be patient)\n')

results = []

for i, (esv_id, cls, pm, seq, reads, n_sites, sites) in enumerate(esv_rows):
    sys.stdout.write(f'[{i+1}/{len(esv_rows)}] {esv_id}  {reads:,} reads  {n_sites} sites ... ')
    sys.stdout.flush()

    try:
        handle = NCBIWWW.qblast(
            program='blastn',
            database='nt',
            sequence=seq,
            entrez_query='Bacillariophyta[Organism]',
            hitlist_size=5,
            expect=1e-10,
            word_size=11,
        )
        blast_record = NCBIXML.read(handle)

        hits = []
        for alignment in blast_record.alignments[:3]:
            for hsp in alignment.hsps[:1]:
                pct_id = 100 * hsp.identities / hsp.align_length
                hits.append({
                    'title':  alignment.title[:120],
                    'pct_id': pct_id,
                    'evalue': hsp.expect,
                    'length': alignment.length,
                })
                break

        results.append({
            'esv_id':  esv_id,
            'class':   cls or '?',
            'jv_match': pm,
            'reads':   reads,
            'n_sites': n_sites,
            'sites':   sites,
            'hits':    hits,
        })

        if hits:
            top = hits[0]
            print(f'OK  top hit: {top["pct_id"]:.1f}% id  {top["title"][:60]}')
        else:
            print('no hits')

    except Exception as e:
        print(f'ERROR: {e}')
        results.append({'esv_id': esv_id, 'error': str(e)})

    time.sleep(5)   # NCBI rate limit: max 3 req/sec with email, 1/sec without

# Write report
print('\n' + '='*70)
print('BLAST RESULTS — Unresolved diatom ESVs')
print('='*70)
for r in results:
    if 'error' in r:
        print(f"\n{r['esv_id']}  ERROR: {r['error']}")
        continue
    print(f"\n{r['esv_id']}  ({r['reads']:,} reads, {r['n_sites']} sites, JV match {r['jv_match']}%)")
    print(f"  Sites: {r['sites'][:100]}")
    if r['hits']:
        for h in r['hits']:
            print(f"  BLAST {h['pct_id']:.1f}% id  e={h['evalue']:.1e}  {h['title'][:90]}")
    else:
        print('  No BLAST hits above threshold')
