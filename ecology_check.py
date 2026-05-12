import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== EUNOTIA (corrected from Halamphora) — by site ===")
rows = conn.execute("""
  SELECT s.site_name, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.blast_notes LIKE '%MISMATCH%'
    AND e.genus = 'Halamphora' AND e.blast_genus = 'Eunotia'
  GROUP BY s.site_name ORDER BY reads DESC LIMIT 20
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):40}  {r[1]:3} ESVs  {r[2]:8,} reads")

print()
print("=== TELEAULAX (corrected from Geminigera/Pseudopedinella) — by site ===")
rows = conn.execute("""
  SELECT s.site_name, e.genus as jv_genus, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.blast_notes LIKE '%MISMATCH%'
    AND e.blast_genus = 'Teleaulax'
  GROUP BY s.site_name, e.genus ORDER BY reads DESC LIMIT 20
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):40}  JV={str(r[1]):18}  {r[2]:3} ESVs  {r[3]:8,} reads")

print()
print("=== PHOXINUS fish (corrected from Chrosomus) — by site ===")
rows = conn.execute("""
  SELECT s.site_name, e.species, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.blast_notes LIKE '%MISMATCH%'
    AND e.genus = 'Chrosomus' AND e.blast_genus = 'Phoxinus'
  GROUP BY s.site_name, e.species ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):40}  species={str(r[1]):25}  {r[2]:3} ESVs  {r[3]:8,} reads")

print()
print("=== EPIPYXIS (corrected from Mallomonas) — by site ===")
rows = conn.execute("""
  SELECT s.site_name, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.blast_notes LIKE '%MISMATCH%'
    AND e.genus = 'Mallomonas' AND e.blast_genus = 'Epipyxis'
  GROUP BY s.site_name ORDER BY reads DESC LIMIT 15
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):40}  {r[1]:3} ESVs  {r[2]:8,} reads")

print()
print("=== EUNOTIA ecological signal: confirmed + corrected total by site ===")
rows = conn.execute("""
  SELECT s.site_name, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE (e.blast_genus = 'Eunotia' OR (e.genus = 'Eunotia' AND e.blast_notes = 'confirmed'))
  GROUP BY s.site_name ORDER BY reads DESC LIMIT 20
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):40}  {r[1]:3} ESVs  {r[2]:8,} reads")

conn.close()
