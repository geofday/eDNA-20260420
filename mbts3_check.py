import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# Search for AEFBOYWK with and without suffix
for code in ['AEFBOYWK', 'AEFBOYWK.1']:
    row = conn.execute('SELECT sample_code, batch_id, site_name, lat, lon, capture_time, notes FROM samples WHERE sample_code=?', (code,)).fetchone()
    print(f'samples lookup [{code}]: {row}')
    reads = conn.execute('SELECT assay, COUNT(*), SUM(read_count) FROM reads WHERE sample_code=? GROUP BY assay', (code,)).fetchall()
    print(f'reads [{code}]: {reads}')

# Also search broadly
print()
print('LIKE search:')
rows = conn.execute("SELECT sample_code, batch_id, site_name FROM samples WHERE sample_code LIKE '%AEFBOYWK%'").fetchall()
print(rows)

# Check what MBTS #3 looks like in site names
print()
print('MBTS #3 site name search:')
rows = conn.execute("SELECT sample_code, batch_id, site_name FROM samples WHERE site_name LIKE '%MBTS%3%' OR site_name LIKE '%#3%' OR site_name LIKE '%3%MBTS%'").fetchall()
for r in rows:
    print(r)

conn.close()
