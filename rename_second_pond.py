import sys, io, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

print('Renaming Second Pond → L Mackintosh Pond in database...')
conn.execute("""
    UPDATE samples
    SET site_name      = REPLACE(REPLACE(LOWER(site_name), 'second pond', 'x'), 'x',
                         'L Mackintosh Pond'),
        canonical_site = REPLACE(REPLACE(LOWER(canonical_site), 'second pond', 'x'), 'x',
                         'L Mackintosh Pond')
    WHERE sample_code = 'OC41MHKC.1'
""")

# Simpler direct update
conn.execute("""
    UPDATE samples
    SET site_name      = 'L Mackintosh Pond MBTS',
        canonical_site = 'L Mackintosh Pond MBTS (Forrest Ln)'
    WHERE sample_code = 'OC41MHKC.1'
""")
conn.commit()

row = conn.execute("SELECT sample_code, site_name, canonical_site FROM samples WHERE sample_code='OC41MHKC.1'").fetchone()
print(f'  {row}')
conn.close()
print('Done.')
