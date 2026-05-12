import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== Sample D8F0GB5R.1 full record ===")
row = conn.execute("SELECT * FROM samples WHERE sample_code='D8F0GB5R.1'").fetchone()
cols = [d[0] for d in conn.execute("PRAGMA table_info(samples)").fetchall()]
for c, v in zip(cols, row):
    if v: print(f"  {c}: {v}")

print("\n=== All JVB3759 samples with Union River in name ===")
rows = conn.execute("""
    SELECT sample_code, site_name, capture_time FROM samples
    WHERE batch_id='JVB3759' ORDER BY site_name
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):40}  {r[2]}")

print("\n=== Alosa sapidissima ESV_007836 across all samples ===")
rows = conn.execute("""
    SELECT s.sample_code, s.site_name, s.capture_time, s.batch_id, SUM(r.read_count) as reads
    FROM reads r JOIN samples s ON s.sample_code=r.sample_code
    WHERE r.esv_id='ESV_007836'
    GROUP BY s.sample_code ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  site={str(r[1]):40}  date={r[2]}  batch={r[3]}  reads={r[4]:,}")

conn.close()
