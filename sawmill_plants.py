import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== ALL 23S (plant/algal) signals at Sawmill Brook sites ===")
rows = conn.execute("""
  SELECT s.site_name, e.blast_genus, e.blast_species, e.blast_pct,
         e.genus as jv_genus, e.blast_notes,
         SUM(r.read_count) as reads, COUNT(*) as n
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE s.site_name LIKE '%awmill%' AND e.assay = '23S'
  GROUP BY s.site_name, e.blast_genus, e.blast_species, e.blast_pct, e.genus, e.blast_notes
  ORDER BY s.site_name, reads DESC
""").fetchall()

current_site = None
for r in rows:
    if r[0] != current_site:
        current_site = r[0]
        print(f"\n  -- {current_site} --")
    flag = '<<< ORNAMENTAL?' if r[1] and any(x in str(r[1]+str(r[2])) for x in ['Toona','Viburnum','Cladosiphon','Kryptoperidinium','Acanthoceras']) else ''
    flag = '<<< INVASIVE?' if 'Nitellopsis' in str(r[1]) else flag
    flag = '<<< TIDAL' if r[1] in ('Teleaulax','Ostreococcus','Florenciella') else flag
    print(f"    {str(r[1]):22} {str(r[2]):40} {str(r[3]):5}%  {r[6]:8,} reads  {flag}")

print()
print("=== CHLOROPLAST / LAND PLANT signals across ALL sites (blast_species contains 'chloroplast') ===")
rows = conn.execute("""
  SELECT e.blast_genus, e.blast_species, e.blast_pct,
         s.site_name, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE e.blast_species LIKE '%chloroplast%'
    AND e.blast_genus NOT IN ('Eunotia','Navicula','Diatoma','Nitzschia',
        'Stephanocyclus','Achnanthidium','Gomphonema','Pinnularia',
        'Sellaphora','Fragilaria','Synedra','Cymbella','Aulacoseira')
  GROUP BY e.blast_genus, e.blast_species, e.blast_pct, s.site_name
  ORDER BY reads DESC LIMIT 30
""").fetchall()
print(f"  {'Genus':22} {'Species':45} {'%':5}  {'Site':35}  {'Reads':>8}")
for r in rows:
    print(f"  {str(r[0]):22} {str(r[1]):45} {str(r[2]):5}  {str(r[3]):35}  {r[4]:8,}")

conn.close()
