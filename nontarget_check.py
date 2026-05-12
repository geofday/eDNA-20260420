import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

targets = [
    ('Bos',       'Cattle'),
    ('Anas',      'Duck'),
    ('Procyon',   'Raccoon'),
    ('Ondatra',   'Muskrat'),
    ('Sturnus',   'Starling'),
    ('Notophthalmus', 'Eastern Newt'),
    ('Melanogrammus', 'Haddock'),
    ('Hyperoplus','Sandeel'),
    ('Platygobio','Flathead Chub'),
]

for genus, common in targets:
    rows = conn.execute("""
      SELECT s.site_name, COUNT(DISTINCT e.esv_id) as n_esv, SUM(r.read_count) as reads
      FROM esvs e
      JOIN reads r ON r.esv_id = e.esv_id
      JOIN samples s ON s.sample_code = r.sample_code
      WHERE e.blast_genus = ? OR e.genus = ?
      GROUP BY s.site_name ORDER BY reads DESC LIMIT 8
    """, (genus, genus)).fetchall()
    if rows:
        total_reads = sum(r[2] for r in rows if r[2])
        print(f"--- {common} ({genus}) — {total_reads:,} total reads ---")
        for r in rows:
            print(f"  {str(r[0]):42}  {r[1]:2} ESVs  {r[2]:8,} reads")
        print()

# Also check: are the marine fish at tidal/coastal sites?
print("--- Marine fish (Clupea/Menidia/Apeltes/Scomber/Morone) by site ---")
rows = conn.execute("""
  SELECT e.blast_genus, e.genus, s.site_name, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE (e.blast_genus IN ('Melanogrammus','Hyperoplus','Scomber','Clupea')
      OR e.genus IN ('Melanogrammus','Hyperoplus','Scomber','Clupea'))
  GROUP BY e.blast_genus, e.genus, s.site_name ORDER BY reads DESC LIMIT 20
""").fetchall()
for r in rows:
    print(f"  blast={str(r[0]):18} jv={str(r[1]):18} {str(r[2]):42}  {r[3]:,} reads")

conn.close()
