import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

MBTS_CODES = [
    'CVVU52A9.1','CDWD42KP.1','C4SUMTFY.1','5K41GBHR.1','UG79PNJS.1',
    'OTLHJZBA.1','NVN8LUTP.1','OC41MHKC.1','UTEVR3WT.1','LZAC7T2X.1',
    'AEFBOYWK.1','KXUG2Y6J.1','2KL87R0I.1','HVFHCKJQ.1',
]
placeholders = ','.join('?' * len(MBTS_CODES))

rows = conn.execute(f"""
    SELECT
        r.sample_code,
        COALESCE(s.site_name, s.canonical_site) as site,
        e.esv_id,
        e.genus,
        e.species,
        e.blast_genus,
        e.blast_species,
        r.read_count,
        e.assay
    FROM reads r
    JOIN esvs e ON e.esv_id = r.esv_id
    JOIN samples s ON s.sample_code = r.sample_code
    WHERE r.sample_code IN ({placeholders})
    AND e.assay != 'MiFishU'
    ORDER BY r.sample_code, r.read_count DESC
""", MBTS_CODES).fetchall()

print(f"Total MBTS non-fish reads (algae/23S): {len(rows)}")
print()

# Group by sample
from collections import defaultdict
by_site = defaultdict(list)
for row in rows:
    by_site[(row[0], row[1], row[8])].append(row)

for (sc, site, assay), site_rows in sorted(by_site.items()):
    total = sum(r[7] for r in site_rows)
    print(f"\n{'='*70}")
    print(f"{sc} | {site} | assay={assay} | total reads={total:,} | ESVs={len(site_rows)}")
    print(f"{'─'*70}")

    # Show all taxa with read counts and blast status
    for sc2, site2, esv, genus, species, bgenus, bspecies, cnt, assay2 in site_rows:
        pct = cnt/total*100 if total else 0
        name = bspecies or species or bgenus or genus or '(unresolved)'
        blast_flag = ''
        if bspecies and not species:
            blast_flag = ' ← BLAST new'
        elif bspecies and species and bspecies != species:
            blast_flag = f' ← was: {species}'
        elif not bspecies and not species and (genus or bgenus):
            blast_flag = ' [genus only]'
        elif not bspecies and not species and not genus and not bgenus:
            blast_flag = ' [UNRESOLVED]'
        print(f"  {pct:5.1f}%  {cnt:6,}  {name}{blast_flag}")

conn.close()
