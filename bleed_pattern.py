import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

BAD_BATCHES = ['JVB4678', 'JVB5776', 'JVB4846', 'JVB4981', 'JVB5403']

for batch in BAD_BATCHES:
    samples = conn.execute("""
        SELECT s.sample_code, s.site_name,
               COALESCE(SUM(CASE WHEN (e.blast_genus='Struthio' OR e.genus='Struthio')
                               THEN r.read_count ELSE 0 END), 0) as ostrich,
               COALESCE(SUM(r.read_count), 0) as total
        FROM samples s
        LEFT JOIN reads r ON r.sample_code = s.sample_code
        LEFT JOIN esvs e ON e.esv_id = r.esv_id AND e.assay = 'MiFishU'
        WHERE s.batch_id = ?
        GROUP BY s.sample_code
        ORDER BY ostrich DESC
    """, (batch,)).fetchall()

    print(f"=== {batch} ===")
    for sc, site, ostr, tot in samples:
        pct = ostr/tot*100 if tot else 0
        bar = '#' * int(pct / 5)
        print(f"  {pct:5.1f}%  {bar:20}  {ostr:6,}/{tot:6,}  {str(site)[:40]}")
    print()

conn.close()
