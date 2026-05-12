import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
print("samples columns:")
for c in conn.execute('PRAGMA table_info(samples)').fetchall():
    print(f"  {c[0]:3}  {c[1]:25}  {c[2]}")
conn.close()
