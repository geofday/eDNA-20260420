import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== BROOK TROUT PRESENCE vs. FIELD pH ===")
rows = conn.execute("""
  SELECT s.site_name, s.ph_field, s.temp_f,
    SUM(CASE WHEN e.blast_genus='Salvelinus' OR e.genus='Salvelinus' THEN r.read_count ELSE 0 END) as trout_reads,
    SUM(CASE WHEN e.blast_genus='Eunotia' OR (e.genus='Eunotia' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as eunotia_reads,
    SUM(CASE WHEN e.blast_genus='Pinnularia' OR (e.genus='Pinnularia' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as pinnularia_reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE s.ph_field IS NOT NULL AND s.ph_field != ''
  GROUP BY s.site_name, s.ph_field, s.temp_f
  ORDER BY CAST(s.ph_field AS REAL) ASC
""").fetchall()
print(f"  {'Site':42}  {'pH':>5}  {'Temp°F':>6}  {'BkTr reads':>10}  {'Eunotia':>8}  {'Pinnularia':>10}")
for r in rows:
    trout_flag = '*** TROUT' if r[3] > 0 else ''
    print(f"  {str(r[0]):42}  {str(r[1]):>5}  {str(r[2]):>6}  {r[3]:10,}  {r[4]:8,}  {r[5]:10,}  {trout_flag}")

print()
print("=== EUNOTIA NAEGELII — ecological signal summary ===")
rows = conn.execute("""
  SELECT e.blast_species, e.blast_pct, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.blast_genus = 'Eunotia'
  GROUP BY e.blast_species, e.blast_pct ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[2]:3} ESVs  {r[3]:8,} reads  {r[1]:.1f}%  {r[0]}")

print()
print("=== SYNURA at Crotch Camp Creek — species? ===")
rows = conn.execute("""
  SELECT e.blast_genus, e.blast_species, e.blast_pct, e.blast_notes,
         SUM(r.read_count) as reads, COUNT(*) as n
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE s.site_name = 'Crotch Camp Creek'
    AND e.assay != 'MiFishU'
  GROUP BY e.blast_genus, e.blast_species, e.blast_pct, e.blast_notes
  ORDER BY reads DESC LIMIT 15
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):20} {str(r[1]):35} {str(r[2]):5}%  {r[4]:8,} reads  [{r[5]} ESVs]  {r[3]}")

conn.close()
