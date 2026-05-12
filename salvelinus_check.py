import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== All Salvelinus ESVs — full status ===")
rows = conn.execute("""
  SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
         e.blast_pct, e.blast_notes, SUM(r.read_count) as reads
  FROM esvs e
  LEFT JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.genus = 'Salvelinus' OR e.blast_genus = 'Salvelinus'
  GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  JV={r[1]} {str(r[2]):30} BLAST={str(r[3])} {str(r[4]):30} {str(r[5]):6} | {r[6][:50]}  [{r[7]:,} reads]")

print()
print("=== Salvelinus by site ===")
rows = conn.execute("""
  SELECT s.site_name, e.species, e.blast_notes, SUM(r.read_count) as reads, COUNT(*) as n
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.genus = 'Salvelinus' OR e.blast_genus = 'Salvelinus'
  GROUP BY s.site_name, e.species, e.blast_notes ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):42} species={str(r[1]):25} {str(r[2]):30} {r[3]:,} reads [{r[4]} ESVs]")

print()
print("=== Sequence lengths of Salvelinus ESVs ===")
rows = conn.execute("""
  SELECT esv_id, genus, species, blast_notes, LENGTH(sequence) as seqlen
  FROM esvs WHERE genus = 'Salvelinus'
  ORDER BY seqlen DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {r[1]} {str(r[2]):25}  seqlen={r[4]}  {r[3]}")

conn.close()
