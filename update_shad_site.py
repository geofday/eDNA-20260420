import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
conn.execute("""
    UPDATE samples SET site_name='Union River Dam', capture_time='7/10/2024'
    WHERE sample_code='D8F0GB5R.1'
""")
conn.commit()
row = conn.execute("SELECT sample_code, site_name, capture_time, canonical_site, batch_id FROM samples WHERE sample_code='D8F0GB5R.1'").fetchone()
print("Updated:", row)
conn.close()
