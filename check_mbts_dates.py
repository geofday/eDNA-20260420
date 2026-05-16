import sys, io, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

MBTS_CODES = [
    'CVVU52A9.1','CDWD42KP.1','C4SUMTFY.1','5K41GBHR.1','UG79PNJS.1',
    'OTLHJZBA.1','NVN8LUTP.1','OC41MHKC.1','UTEVR3WT.1','LZAC7T2X.1',
    'AEFBOYWK.1','KXUG2Y6J.1','2KL87R0I.1','HVFHCKJQ.1',
]
placeholders = ','.join('?' * len(MBTS_CODES))

rows = conn.execute(f"""
    SELECT sample_code, COALESCE(site_name, canonical_site) as site,
           capture_time, batch_id
    FROM samples
    WHERE sample_code IN ({placeholders})
    ORDER BY capture_time, sample_code
""", MBTS_CODES).fetchall()

print(f"{'Sample':22s} {'Site':35s} {'capture_time':20s} {'Batch':12s}")
print('-' * 95)
for sc, site, ct, batch in rows:
    date_str = ct if ct else '*** MISSING ***'
    print(f"{sc:22s} {(site or '')[:35]:35s} {date_str:20s} {batch or ''}")

missing = [r for r in rows if not r[2]]
print(f"\n{len(missing)} of {len(rows)} MBTS samples missing capture_time")
conn.close()
