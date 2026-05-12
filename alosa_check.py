import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== ALL ALOSA ESVs — species, confidence, notes ===")
rows = conn.execute("""
  SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
         e.blast_pct, e.blast_notes, LENGTH(e.sequence) as seqlen,
         SUM(r.read_count) as reads
  FROM esvs e
  LEFT JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.genus='Alosa' OR e.blast_genus='Alosa'
  GROUP BY e.esv_id ORDER BY e.blast_species, reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  JV={str(r[1])} {str(r[2]):28} BLAST={str(r[3])} {str(r[4]):35} {str(r[5]):5}%  seq={r[7]}bp  {r[8]:7,}r  [{r[6][:40]}]")

print()
print("=== ALOSA by site — do pseudoharengus and aestivalis separate spatially? ===")
for species, label in [
    ('Alosa pseudoharengus', 'Alewife'),
    ('Alosa aestivalis',     'Blueback Herring'),
    ('Alosa mediocris',      'Hickory Shad'),
]:
    print(f"\n  -- {label} ({species}) --")
    rows = conn.execute("""
      SELECT s.site_name, SUM(r.read_count) as reads, COUNT(DISTINCT e.esv_id) as n
      FROM esvs e
      JOIN reads r ON r.esv_id = e.esv_id
      JOIN samples s ON s.sample_code = r.sample_code
      WHERE (e.blast_species LIKE ? OR e.species LIKE ?)
      GROUP BY s.site_name ORDER BY reads DESC LIMIT 12
    """, (f'%{species.split()[1]}%', f'%{species.split()[1]}%')).fetchall()
    for r in rows:
        print(f"    {str(r[0]):42}  {r[2]:2} ESVs  {r[1]:8,} reads")

print()
print("=== SEQUENCE DIVERGENCE — compare pseudoharengus vs aestivalis ESV sequences ===")
rows = conn.execute("""
  SELECT e.esv_id, e.blast_species, e.blast_pct, e.sequence
  FROM esvs e
  WHERE (e.blast_species LIKE '%pseudoharengus%' OR e.blast_species LIKE '%aestivalis%')
    AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 100
  ORDER BY e.blast_species, e.blast_pct DESC
  LIMIT 6
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):35} {r[2]}%")
    print(f"    seq: {r[3][:80]}...")
    print()

print("=== UNRESOLVED ALOSA (species-level ambiguous) ===")
rows = conn.execute("""
  SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
         e.blast_pct, e.blast_notes, SUM(r.read_count) as reads
  FROM esvs e
  LEFT JOIN reads r ON r.esv_id = e.esv_id
  WHERE (e.genus='Alosa' OR e.blast_genus='Alosa')
    AND (e.blast_species IS NULL OR e.blast_species='None'
         OR e.blast_species NOT LIKE '%pseudoharengus%'
         AND e.blast_species NOT LIKE '%aestivalis%'
         AND e.blast_species NOT LIKE '%mediocris%'
         AND e.blast_species NOT LIKE '%sapidissima%')
  GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  JV={str(r[1])} {str(r[2]):25} BLAST={str(r[3])} {str(r[4]):30} {str(r[5]):5}%  {r[7]:,}r  [{str(r[6])[:50]}]")

conn.close()
