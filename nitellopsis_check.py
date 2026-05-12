import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print('=== ESV_100357 — Nitellopsis/charophyte ===')
row = conn.execute("""
    SELECT esv_id, assay, class, "order", family, genus, species,
           perc_match, n_species, common_name, blast_genus, blast_species,
           blast_pct, blast_notes, sequence
    FROM esvs WHERE esv_id='ESV_100357'
""").fetchone()
if row:
    fields = ['esv_id','assay','class','order','family','genus','species',
              'perc_match','n_species','common_name','blast_genus','blast_species',
              'blast_pct','blast_notes','sequence']
    for f, v in zip(fields, row):
        if f == 'sequence':
            print(f'  {f}: {str(v)[:120]}')
        else:
            print(f'  {f}: {v}')

print()
print('=== Sites where ESV_100357 appears ===')
rows = conn.execute("""
    SELECT r.sample_code, r.read_count,
           COALESCE(s.canonical_site, s.site_name, r.sample_code) as site,
           s.batch_id
    FROM reads r
    JOIN samples s ON r.sample_code=s.sample_code
    WHERE r.esv_id='ESV_100357'
    ORDER BY r.read_count DESC
""").fetchall()
for r in rows:
    print(f'  {r[0]}  reads={r[1]:>6,}  site={str(r[2])[:50]}  batch={r[3]}')

print()
print('=== All Charophyceae ESVs in DB ===')
rows2 = conn.execute("""
    SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
           e.blast_pct, e.perc_match,
           SUM(r.read_count) as total_reads
    FROM esvs e
    JOIN reads r ON e.esv_id=r.esv_id AND e.assay=r.assay
    WHERE e.class='Charophyceae'
    GROUP BY e.esv_id
    ORDER BY total_reads DESC
""").fetchall()
for r in rows2:
    print(f'  {r[0]:12} JV={str(r[1]):15}/{str(r[2]):25}  BLAST={str(r[3]):15}/{str(r[4]):30} {r[5]}%  reads={r[7]:>6,}')

conn.close()
