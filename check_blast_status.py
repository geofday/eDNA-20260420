import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
n_done = conn.execute("SELECT COUNT(esv_id) FROM esvs WHERE blast_genus IS NOT NULL").fetchone()[0]
n_todo = conn.execute("SELECT COUNT(esv_id) FROM esvs WHERE blast_genus IS NULL AND sequence IS NOT NULL AND LENGTH(sequence)>50").fetchone()[0]
print(f'Already blasted: {n_done}')
print(f'Still unblasted: {n_todo}')
rows = conn.execute("SELECT esv_id, blast_genus, blast_species, blast_notes FROM esvs WHERE blast_genus IS NOT NULL ORDER BY esv_id").fetchall()
for r in rows:
    print(f'  {r[0]:12} {str(r[1]):20} {str(r[2]):30} {str(r[3])[:40]}')
conn.close()
