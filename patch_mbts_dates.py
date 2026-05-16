import sys, io, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

updates = [
    # JVB3787 — Aug 28, 2024 confirmed from document header
    ('8/28/2024', '5K41GBHR.1'),   # Sawmill Swamp
    ('8/28/2024', 'OTLHJZBA.1'),   # Sawmill Fire Station
    ('8/28/2024', 'UG79PNJS.1'),   # Sawmill School St
    # JVB5776 — Nov 22, 2025 (same batch as C4SUMTFY.1 and CDWD42KP.1 which both have that date)
    ('11/22/2025', 'CVVU52A9.1'),  # Upper Sawmill
]

for date_val, sc in updates:
    conn.execute("UPDATE samples SET capture_time = ? WHERE sample_code = ?", (date_val, sc))
    print(f"  Updated {sc} → {date_val}")

conn.commit()

# Verify
print()
MBTS_CODES = ['5K41GBHR.1','OTLHJZBA.1','UG79PNJS.1','CVVU52A9.1']
rows = conn.execute(
    "SELECT sample_code, COALESCE(site_name,canonical_site), capture_time FROM samples WHERE sample_code IN (?,?,?,?)",
    MBTS_CODES
).fetchall()
for r in rows:
    print(f"  {r[0]:22s} {(r[1] or '')[:35]:35s} {r[2]}")

conn.close()
print("\nDone.")
