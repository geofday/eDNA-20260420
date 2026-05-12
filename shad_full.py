import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
cols = [d[0] for d in conn.execute("PRAGMA table_info(samples)").fetchall()]
print("Columns:", cols)
row = conn.execute("SELECT * FROM samples WHERE sample_code='D8F0GB5R.1'").fetchone()
for i, (c, v) in enumerate(zip(cols, row)):
    print(f"  [{i}] {c}: {v}")
conn.close()
