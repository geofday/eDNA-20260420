import sys, io, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

# Co-collected pH values (same day or next day as eDNA sample)
# Source: Vivosun pH meter, two-point calibration corrected, ±0.2 pH unit
# From MBTS_eDNA_Report v38 Table 1 and site measurement tables
updates = [
    (6.88, 'KXUG2Y6J.1'),   # Below Lincoln Pool, Jun 5, 2025 — same day as eDNA
    (6.15, '2KL87R0I.1'),   # Atwater, Jun 8, 2025 — same day as eDNA
    (6.66, 'CDWD42KP.1'),   # School St/Below School St, Nov 23, 2025 — one day after eDNA (Nov 22)
]

print('Updating ph_field in samples table:')
for ph, sc in updates:
    conn.execute("UPDATE samples SET ph_field = ? WHERE sample_code = ?", (ph, sc))
    print(f'  {sc} → ph_field = {ph}')

conn.commit()

print()
print('Verification:')
MBTS_CODES = [
    'CVVU52A9.1','CDWD42KP.1','C4SUMTFY.1','5K41GBHR.1','UG79PNJS.1',
    'OTLHJZBA.1','NVN8LUTP.1','OC41MHKC.1','UTEVR3WT.1','LZAC7T2X.1',
    'AEFBOYWK.1','KXUG2Y6J.1','2KL87R0I.1','HVFHCKJQ.1',
]
placeholders = ','.join('?' * len(MBTS_CODES))
rows = conn.execute(f"""
    SELECT sample_code, COALESCE(site_name, canonical_site), capture_time, ph_field
    FROM samples WHERE sample_code IN ({placeholders})
    ORDER BY capture_time
""", MBTS_CODES).fetchall()
for sc, site, ct, ph in rows:
    ph_str = f'pH {ph:.2f}' if ph else '---'
    print(f'  {sc:22s} {(site or "")[:32]:32s} {(ct or "?"):14s}  {ph_str}')

conn.close()
