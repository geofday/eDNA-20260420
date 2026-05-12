import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== All Alosa detections ===")
rows = conn.execute("""
    SELECT s.sample_code, s.site_name, s.capture_time, s.batch_id,
           e.esv_id, e.blast_species, e.blast_pct, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    JOIN samples s ON s.sample_code=r.sample_code
    WHERE e.blast_genus='Alosa' OR e.genus='Alosa'
    GROUP BY s.sample_code, e.esv_id
    ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  site={str(r[1]):35}  date={r[2]}  batch={r[3]}  esv={r[4]}  sp={r[5]}  pct={r[6]}  reads={r[7]:,}")

print(f"\nTotal Alosa rows: {len(rows)}")

print("\n=== Alosa ESV details ===")
esvs = conn.execute("""
    SELECT e.esv_id, e.blast_genus, e.blast_species, e.blast_pct, e.blast_notes,
           e.genus, e.species, e.assay
    FROM esvs e
    WHERE e.blast_genus='Alosa' OR e.genus='Alosa'
""").fetchall()
for e in esvs:
    print(f"  {e[0]}  blast={e[1]} {e[2]} {e[3]}%  jv={e[5]} {e[6]}  assay={e[7]}  [{e[4]}]")

conn.close()
