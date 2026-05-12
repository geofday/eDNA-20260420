import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
total = conn.execute('SELECT COUNT(*) FROM esvs').fetchone()[0]
blasted = conn.execute('SELECT COUNT(*) FROM esvs WHERE blast_genus IS NOT NULL').fetchone()[0]
unblasted = conn.execute('SELECT COUNT(*) FROM esvs WHERE blast_genus IS NULL').fetchone()[0]
mismatches = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE '%MISMATCH%'").fetchone()[0]
print(f'Total ESVs:     {total:,}')
print(f'Blasted:        {blasted:,}')
print(f'Unblasted:      {unblasted:,}')
print(f'Mismatches:     {mismatches:,}')
print()
print('=== MISMATCH patterns (JV genus => BLAST genus) ===')
rows = conn.execute("""
  SELECT genus, blast_genus, COUNT(*) as n
  FROM esvs WHERE blast_notes LIKE '%MISMATCH%'
  GROUP BY genus, blast_genus ORDER BY n DESC LIMIT 25
""").fetchall()
for r in rows:
    print(f'  JV={str(r[0]):22} => BLAST={str(r[1]):22}  ({r[2]}x)')

print()
print('=== Newly resolved (no JV genus, now has BLAST) ===')
rows2 = conn.execute("""
  SELECT blast_genus, COUNT(*) as n
  FROM esvs WHERE blast_notes='newly resolved' AND blast_genus IS NOT NULL
  GROUP BY blast_genus ORDER BY n DESC LIMIT 20
""").fetchall()
for r in rows2:
    print(f'  {str(r[0]):25}  ({r[1]}x)')

conn.close()
