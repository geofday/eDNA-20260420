import sqlite3, csv

conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

rows = conn.execute("""
    SELECT
        s.batch_id,
        s.sample_code,
        s.site_name,
        s.capture_time,
        COALESCE(SUM(r.read_count), 0) as total_reads,
        COALESCE(SUM(CASE WHEN e.blast_genus='Struthio' OR e.genus='Struthio'
                         THEN r.read_count ELSE 0 END), 0) as ostrich_reads
    FROM samples s
    LEFT JOIN reads r ON r.sample_code = s.sample_code
    LEFT JOIN esvs e ON e.esv_id = r.esv_id AND e.assay = 'MiFishU'
    GROUP BY s.sample_code
    ORDER BY s.batch_id, ostrich_reads DESC
""").fetchall()

out = r'c:\repos\eDNA-20270420\output\bleed_by_sample.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Batch', 'Sample', 'Site', 'Date', 'Total Reads', 'Ostrich Reads', 'Ostrich %'])
    for batch, sample, site, date, total, ostrich in rows:
        pct = round(ostrich / total * 100, 1) if total else 0
        w.writerow([batch, sample, site, date, total, ostrich, pct])

print(f"Written: {out}")
print(f"Rows: {len(rows)}")
conn.close()
