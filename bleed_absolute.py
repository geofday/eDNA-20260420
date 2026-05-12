import sqlite3, csv

conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

rows = conn.execute("""
    SELECT
        s.batch_id,
        s.sample_code,
        s.site_name,
        COALESCE(SUM(r.read_count), 0) as total_reads,
        COALESCE(SUM(CASE WHEN e.blast_genus='Struthio' OR e.genus='Struthio'
                         THEN r.read_count ELSE 0 END), 0) as ostrich_reads
    FROM samples s
    LEFT JOIN reads r ON r.sample_code = s.sample_code
    LEFT JOIN esvs e ON e.esv_id = r.esv_id AND e.assay = 'MiFishU'
    GROUP BY s.sample_code
    ORDER BY s.batch_id, ostrich_reads DESC
""").fetchall()

# Group by batch
from collections import defaultdict
batches = defaultdict(list)
for batch, sample, site, total, ostrich in rows:
    batches[batch].append((sample, site, total, ostrich))

print("=== OSTRICH ABSOLUTE READ COUNTS BY BATCH ===")
print("(A controlled spike should be roughly constant within a batch)\n")

out_rows = []
for batch in sorted(batches.keys()):
    samples = batches[batch]
    ostrich_counts = [s[3] for s in samples if s[3] > 0]
    if not ostrich_counts:
        mn, mx, ratio = 0, 0, 1
    else:
        mn, mx = min(ostrich_counts), max(ostrich_counts)
        ratio = mx / mn if mn > 0 else 999

    flag = ''
    if ratio > 10:
        flag = '*** BLEED LIKELY (>10x range)'
    elif ratio > 4:
        flag = '* ELEVATED VARIATION (>4x range)'

    print(f"  {batch}  min={mn:,}  max={mx:,}  ratio={ratio:.1f}x  {flag}")
    for sample, site, total, ostrich in samples:
        pct = ostrich/total*100 if total else 0
        bar = '#' * int(ostrich / 2000)
        print(f"    {ostrich:6,}  {bar:25}  ({pct:.0f}%)  {str(site)[:38]}")
        out_rows.append([batch, sample, site, total, ostrich, round(pct,1), round(ratio,1)])
    print()

out = r'c:\repos\eDNA-20270420\output\bleed_absolute.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Batch', 'Sample', 'Site', 'Total Reads', 'Ostrich Reads',
                'Ostrich %', 'Batch Max/Min Ratio'])
    w.writerows(out_rows)
print(f"CSV written: {out}")
conn.close()
