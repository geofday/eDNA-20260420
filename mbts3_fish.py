import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print('=== MBTS #3 / AEFBOYWK.1 (JVB4846, 4/12/2025) ===')
print('Coords: 44.77N, -67.37W (Downeast Maine)')
print()

rows = conn.execute("""
    SELECT e.blast_genus, e.blast_species, e.blast_pct, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE r.sample_code='AEFBOYWK.1' AND e.assay='MiFishU'
    GROUP BY e.blast_genus, e.blast_species, e.blast_pct
    ORDER BY reads DESC
""").fetchall()
total = sum(r[3] for r in rows) or 1
for r in rows:
    print(f'  {str(r[0]):22} {str(r[1]):35} {str(r[2]):5}%  {r[3]:7,} ({r[3]/total*100:.1f}%)')

print()
print('=== All JVB4846 samples ===')
rows = conn.execute("""
    SELECT sample_code, site_name, lat, lon, capture_time
    FROM samples WHERE batch_id='JVB4846' ORDER BY capture_time
""").fetchall()
for r in rows:
    print(f'  {r[0]}  site={str(r[1]):35}  lat={str(r[2]):10}  lon={str(r[3]):12}  time={r[4]}')

conn.close()
