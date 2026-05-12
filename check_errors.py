import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

rows = conn.execute("""
    SELECT blast_notes, COUNT(*) as n
    FROM esvs WHERE blast_notes LIKE 'error%'
    GROUP BY blast_notes ORDER BY n DESC LIMIT 20
""").fetchall()
print('=== Error types ===')
for r in rows:
    print(f'  ({r[1]:4}x)  {r[0][:120]}')

print()
print('=== Sample of error ESVs ===')
rows2 = conn.execute("""
    SELECT esv_id, assay, genus, species, blast_notes
    FROM esvs WHERE blast_notes LIKE 'error%'
    LIMIT 10
""").fetchall()
for r in rows2:
    print(f'  {r[0]}  assay={r[1]}  JV={r[2]} {r[3]}')
    print(f'    {r[4][:120]}')

conn.close()
