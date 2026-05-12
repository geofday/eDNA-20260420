import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# Spiked batches only
SPIKED = ['JVB4678', 'JVB4846', 'JVB4981', 'JVB5403', 'JVB5776']

print("=== AMPLIFICATION FAILURES — spiked batches only ===")
print("(spike present at batch-normal level, but environmental reads near-zero)\n")

for batch in SPIKED:
    samples = conn.execute("""
        SELECT s.sample_code, s.site_name, s.capture_time,
               COALESCE(SUM(CASE WHEN e.assay='MiFishU' THEN r.read_count ELSE 0 END), 0) as total,
               COALESCE(SUM(CASE WHEN e.assay='MiFishU'
                                  AND (e.blast_genus='Struthio' OR e.genus='Struthio')
                                 THEN r.read_count ELSE 0 END), 0) as ostrich
        FROM samples s
        LEFT JOIN reads r ON r.sample_code = s.sample_code
        LEFT JOIN esvs e ON e.esv_id = r.esv_id
        WHERE s.batch_id = ?
        GROUP BY s.sample_code
    """, (batch,)).fetchall()

    # Batch median ostrich as baseline
    ostrich_counts = sorted([s[4] for s in samples if s[4] > 0])
    if not ostrich_counts:
        continue
    n = len(ostrich_counts)
    baseline = ostrich_counts[n//2]

    print(f"  {batch}  (spike baseline ~{baseline:,} reads)")
    print(f"  {'Sample':15} {'Site':38} {'Date':18} {'Env.Reads':>10} {'Ostrich':>8} {'Flag'}")
    print(f"  {'-'*15} {'-'*38} {'-'*18} {'-'*10} {'-'*8}")

    for sample, site, date, total, ostrich in sorted(samples, key=lambda x: x[3]-x[4]):
        env = total - ostrich
        spike_ok = ostrich >= baseline * 0.3  # within reasonable range of baseline
        flag = ''
        if env < 1000 and spike_ok:
            flag = '*** AMP FAILURE — spike ok, no env. DNA'
        elif env < 3000 and spike_ok:
            flag = '* LOW ENV. READS'
        print(f"  {str(sample):15} {str(site)[:38]:38} {str(date)[:18]:18} {env:10,} {ostrich:8,}  {flag}")
    print()

conn.close()
