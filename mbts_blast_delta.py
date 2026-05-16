import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

MBTS_CODES = [
    'CVVU52A9.1','CDWD42KP.1','C4SUMTFY.1','5K41GBHR.1','UG79PNJS.1',
    'OTLHJZBA.1','NVN8LUTP.1','OC41MHKC.1','UTEVR3WT.1','LZAC7T2X.1',
    'AEFBOYWK.1','KXUG2Y6J.1','2KL87R0I.1','HVFHCKJQ.1',
]

placeholders = ','.join('?' * len(MBTS_CODES))

# All MiFishU reads for MBTS — show blast_species vs species and flag where they differ
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
    AND e.assay = 'MiFishU'
    AND e.blast_genus NOT IN ('Struthio','Homo')
    ORDER BY r.sample_code, r.read_count DESC
""", MBTS_CODES).fetchall()

print(f"Total MBTS MiFishU reads: {len(rows)}")
print()

# Show ESVs where blast_species differs from species (= BLAST changed something)
print("=== BLAST changed or resolved species ===")
for sc, site, esv, genus, species, bgenus, bspecies, cnt, assay in rows:
    if bspecies and species and bspecies != species:
        print(f"  {sc:20s} {site[:25]:25s} {cnt:6d}  species={species}  blast={bspecies}")
    elif bspecies and not species:
        print(f"  {sc:20s} {site[:25]:25s} {cnt:6d}  species=None  blast={bspecies}  [newly resolved]")
    elif species and not bspecies:
        print(f"  {sc:20s} {site[:25]:25s} {cnt:6d}  species={species}  blast=None  [unconfirmed]")

print()
print("=== Still genus-only (blast_species=None, species=None) ===")
for sc, site, esv, genus, species, bgenus, bspecies, cnt, assay in rows:
    if not species and not bspecies and (genus or bgenus):
        print(f"  {sc:20s} {site[:25]:25s} {cnt:6d}  genus={genus or bgenus}")

print()
print("=== Per-site summary ===")
from collections import defaultdict
by_site = defaultdict(list)
for row in rows:
    by_site[(row[0], row[1])].append(row)

for (sc, site), site_rows in sorted(by_site.items()):
    total = sum(r[7] for r in site_rows)
    bt = sum(r[7] for r in site_rows if 'fontinalis' in str(r[4]) or 'fontinalis' in str(r[6]))
    blast_resolved = sum(1 for r in site_rows if r[6])
    unresolved = sum(1 for r in site_rows if not r[6] and not r[3])
    print(f"  {sc:20s} {site[:30]:30s} total={total:6d} BT={bt:5d} ({bt/total*100:.1f}%) ESVs={len(site_rows)} blast_resolved={blast_resolved}")

conn.close()
