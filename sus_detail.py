import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print('=== Sus scrofa ESVs — site-level detail ===')
rows = conn.execute("""
    SELECT e.esv_id, e.genus, e.species, e.perc_match, e.n_species,
           r.sample_code, r.read_count,
           COALESCE(s.canonical_site, s.site_name, r.sample_code) as site,
           s.batch_id
    FROM esvs e
    JOIN reads r ON e.esv_id=r.esv_id AND e.assay=r.assay
    JOIN samples s ON r.sample_code=s.sample_code
    WHERE e.genus='Sus'
    ORDER BY r.read_count DESC
""").fetchall()
for r in rows:
    print(f'  {r[0]:12} {str(r[1]):6} {str(r[2]):20} pm={r[3]}% n_sp={r[4]}  reads={r[6]:>6,}  site={str(r[7])[:40]:40}  batch={r[8]}')

print()
print('=== Sus scrofa sequences ===')
rows2 = conn.execute("""
    SELECT esv_id, perc_match, n_species, sequence
    FROM esvs
    WHERE genus='Sus'
    ORDER BY esv_id
""").fetchall()
for r in rows2:
    print(f'  {r[0]:12} pm={r[1]}% n_sp={r[2]}')
    print(f'    seq={str(r[3])[:120]}')

print()
print('=== Also: Raccoon site detail ===')
rows3 = conn.execute("""
    SELECT e.esv_id, e.species, e.perc_match,
           r.sample_code, r.read_count,
           COALESCE(s.canonical_site, s.site_name, r.sample_code) as site,
           s.batch_id
    FROM esvs e
    JOIN reads r ON e.esv_id=r.esv_id AND e.assay=r.assay
    JOIN samples s ON r.sample_code=s.sample_code
    WHERE e.genus='Procyon'
    ORDER BY r.read_count DESC
""").fetchall()
for r in rows3:
    print(f'  {r[0]:12} {str(r[1]):25} pm={r[2]}%  reads={r[4]:>8,}  site={str(r[5])[:40]}  batch={r[6]}')

conn.close()
