import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== PROCTOR POINT DOCK MBTS — full species inventory ===")
rows = conn.execute("""
  SELECT e.assay,
         COALESCE(e.blast_genus, e.genus, '?') as genus,
         COALESCE(e.blast_species, e.species, '?') as species,
         e.blast_pct, e.blast_notes,
         SUM(r.read_count) as reads,
         COUNT(DISTINCT e.esv_id) as n_esvs
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE s.site_name = 'Proctor Point Dock MBTS'
  GROUP BY e.assay, genus, species, e.blast_pct, e.blast_notes
  ORDER BY reads DESC
""").fetchall()

current_assay = None
for r in rows:
    if r[0] != current_assay:
        current_assay = r[0]
        print(f"\n  [{current_assay}]")
    flag = '*** MISMATCH' if r[4] and 'MISMATCH' in r[4] else ''
    flag = '*** NEW' if r[4] == 'newly resolved' else flag
    print(f"    {str(r[1]):22} {str(r[2]):40} {str(r[3]):5}%  {r[5]:8,} reads  {flag}")

print()
print("=== PROCTOR POINT vs. other MBTS sites — key taxa ===")
mbts_sites = conn.execute("""
  SELECT DISTINCT site_name FROM samples
  WHERE site_name LIKE '%MBTS%' OR site_name LIKE '%Meatball%'
    OR site_name LIKE '%pond%' OR site_name LIKE '%Second%'
  ORDER BY site_name
""").fetchall()

key = [
    ('Alosa mediocris',   'Hickory Shad'),
    ('Alosa pseudoharengus','Alewife'),
    ('Clupea',            'Atlantic Herring'),
    ('Scomber',           'Atlantic Mackerel'),
    ('Menidia',           'Silverside'),
    ('Stenotomus',        'Scup'),
    ('Morone',            'Bass/Perch'),
    ('Fundulus',          'Mummichog'),
    ('Apeltes',           'Stickleback'),
    ('Bos',               'Cattle'),
]
print(f"  {'Taxon':22}", end='')
for (site,) in mbts_sites:
    print(f"  {str(site)[:18]:>18}", end='')
print()
for genus, common in key:
    print(f"  {common:22}", end='')
    for (site,) in mbts_sites:
        r = conn.execute("""
          SELECT SUM(r.read_count) FROM esvs e
          JOIN reads r ON r.esv_id = e.esv_id
          JOIN samples s ON s.sample_code = r.sample_code
          WHERE s.site_name=? AND (e.blast_genus LIKE ? OR e.genus LIKE ?)
        """, (site, f'%{genus.split()[0]}%', f'%{genus.split()[0]}%')).fetchone()[0] or 0
        print(f"  {r:>18,}", end='')
    print()

conn.close()
