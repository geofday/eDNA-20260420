import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== FIELD pH DATA (where available) ===")
rows = conn.execute("""
  SELECT site_name, ph_field, temp_f, COUNT(*) as n_samples
  FROM samples WHERE ph_field IS NOT NULL AND ph_field != ''
  GROUP BY site_name, ph_field, temp_f ORDER BY ph_field ASC
""").fetchall()
for r in rows:
    print(f"  pH={str(r[1]):6}  {str(r[0]):42}  temp={str(r[2]):6}  [{r[3]} samples]")

print()
print("=== ACID-INDICATOR DIATOMS by site (Eunotia, Pinnularia, Achnanthidium) ===")
rows = conn.execute("""
  SELECT s.site_name,
    SUM(CASE WHEN e.blast_genus='Eunotia' OR (e.genus='Eunotia' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as eunotia,
    SUM(CASE WHEN e.blast_genus='Pinnularia' OR (e.genus='Pinnularia' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as pinnularia,
    SUM(CASE WHEN e.blast_genus='Achnanthidium' OR (e.genus='Achnanthidium' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as achnanthidium,
    SUM(r.read_count) as total_reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.assay != 'MiFishU'
  GROUP BY s.site_name
  HAVING (eunotia + pinnularia + achnanthidium) > 0
  ORDER BY eunotia DESC LIMIT 20
""").fetchall()
print(f"  {'Site':42}  {'Eunotia':>10}  {'Pinnularia':>10}  {'Achnanthidium':>13}  {'Total':>10}")
for r in rows:
    pct = (r[1]+r[2]+r[3])/r[4]*100 if r[4] else 0
    print(f"  {str(r[0]):42}  {r[1]:10,}  {r[2]:10,}  {r[3]:13,}  {r[4]:10,}  ({pct:.1f}% acid indicators)")

print()
print("=== OLIGOTROPHIC CHRYSOPHYTES by site (Dinobryon, Synura, Chrysochromulina, Epipyxis) ===")
rows = conn.execute("""
  SELECT s.site_name,
    SUM(CASE WHEN e.blast_genus='Dinobryon' OR (e.genus='Dinobryon' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as dinobryon,
    SUM(CASE WHEN e.blast_genus='Synura' OR (e.genus='Synura' AND e.blast_notes='confirmed') THEN r.read_count ELSE 0 END) as synura,
    SUM(CASE WHEN e.blast_genus='Chrysochromulina' THEN r.read_count ELSE 0 END) as chrysochromulina,
    SUM(CASE WHEN e.blast_genus='Epipyxis' THEN r.read_count ELSE 0 END) as epipyxis,
    SUM(r.read_count) as total_reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.assay != 'MiFishU'
  GROUP BY s.site_name
  HAVING (dinobryon + synura + chrysochromulina + epipyxis) > 0
  ORDER BY (dinobryon + synura + chrysochromulina + epipyxis) DESC LIMIT 20
""").fetchall()
print(f"  {'Site':42}  {'Dinobryon':>9}  {'Synura':>7}  {'Chryso':>7}  {'Epipyxis':>8}")
for r in rows:
    print(f"  {str(r[0]):42}  {r[1]:9,}  {r[2]:7,}  {r[3]:7,}  {r[4]:8,}")

print()
print("=== EUNOTIA SPECIES breakdown (which species?) ===")
rows = conn.execute("""
  SELECT e.blast_species, COUNT(*) as n_esvs, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.blast_genus = 'Eunotia'
  GROUP BY e.blast_species ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {str(r[1]):3} ESVs  {r[2]:8,} reads  {r[0]}")

conn.close()
