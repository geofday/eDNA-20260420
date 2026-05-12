import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== STRUTHIO BLEED — all samples with ostrich reads ===\n")

rows = conn.execute("""
    SELECT r.sample_code, s.site_name, s.batch_id, s.capture_time,
           SUM(r.read_count) as ostrich_reads
    FROM reads r
    JOIN esvs e ON e.esv_id = r.esv_id
    JOIN samples s ON s.sample_code = r.sample_code
    WHERE e.blast_genus = 'Struthio' OR e.genus = 'Struthio'
    GROUP BY r.sample_code
    ORDER BY ostrich_reads DESC
""").fetchall()

# Get total reads per sample for percentage
total_by_sample = {}
for row in conn.execute("""
    SELECT r.sample_code, SUM(r.read_count)
    FROM reads r JOIN esvs e ON e.esv_id=r.esv_id
    WHERE e.assay='MiFishU'
    GROUP BY r.sample_code
""").fetchall():
    total_by_sample[row[0]] = row[1]

print(f"  {'Sample':15} {'Batch':12} {'Site':38} {'Ostrich':>8} {'Total':>8} {'%':>6}  Flag")
print(f"  {'-'*15} {'-'*12} {'-'*38} {'-'*8} {'-'*8} {'-'*6}")
for r in rows:
    sample, site, batch, time, ostr = r
    total = total_by_sample.get(sample, ostr)
    pct = ostr / total * 100 if total else 0
    flag = ''
    if pct > 40:
        flag = '*** SEVERE'
    elif pct > 15:
        flag = '** HIGH'
    elif pct > 5:
        flag = '* ELEVATED'
    print(f"  {str(sample):15} {str(batch):12} {str(site)[:38]:38} {ostr:8,} {total:8,} {pct:6.1f}%  {flag}")

print(f"\n  Total samples with any ostrich reads: {len(rows)}")
severe = sum(1 for r in rows if r[4]/total_by_sample.get(r[0],r[4])*100 > 40)
high   = sum(1 for r in rows if 15 < r[4]/total_by_sample.get(r[0],r[4])*100 <= 40)
elev   = sum(1 for r in rows if 5  < r[4]/total_by_sample.get(r[0],r[4])*100 <= 15)
print(f"  SEVERE (>40%): {severe}  |  HIGH (15-40%): {high}  |  ELEVATED (5-15%): {elev}")

conn.close()
