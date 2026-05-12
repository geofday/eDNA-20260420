import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# Find all Sawmill and Cat Brook sites
print("=== ALL SAWMILL & CAT BROOK SITES in DB ===")
sites = conn.execute("""
  SELECT DISTINCT site_name, ph_field, temp_f FROM samples
  WHERE site_name LIKE '%awmill%' OR site_name LIKE '%Cat Brook%' OR site_name LIKE '%school%'
  ORDER BY site_name
""").fetchall()
for s in sites:
    print(f"  {str(s[0]):45}  pH={str(s[1]):6}  temp={str(s[2])}")

print()
for site_pattern, label in [
    ('%awmill%', 'SAWMILL BROOK (all)'),
    ('%Cat Brook%', 'CAT BROOK'),
]:
    print(f"=== {label} — top organisms by reads ===")
    rows = conn.execute("""
      SELECT s.site_name,
             COALESCE(e.blast_genus, e.genus, '?') as genus,
             COALESCE(e.blast_species, e.species, '?') as species,
             e.blast_notes,
             e.assay,
             SUM(r.read_count) as reads,
             COUNT(*) as n_esvs
      FROM esvs e
      JOIN reads r ON r.esv_id = e.esv_id
      JOIN samples s ON s.sample_code = r.sample_code
      WHERE s.site_name LIKE ?
      GROUP BY s.site_name, genus, species, e.blast_notes, e.assay
      ORDER BY reads DESC LIMIT 25
    """, (site_pattern,)).fetchall()
    for r in rows:
        flag = '*** MISMATCH' if r[3] and 'MISMATCH' in r[3] else ''
        print(f"  [{r[4]:8}] {str(r[0]):35} {str(r[1]):20} {str(r[2]):35} {r[5]:8,} reads  {flag}")
    print()

print("=== SAWMILL vs CAT BROOK: side-by-side key taxa ===")
key_taxa = [
    ('Salvelinus', 'Brook Trout'),
    ('Eunotia', 'Acid indicator'),
    ('Teleaulax', 'Tidal cryptophyte'),
    ('Chrysochromulina', 'Oligotrophic flag.'),
    ('Alosa', 'Alewife/Herring'),
    ('Anguilla', 'American Eel'),
    ('Notophthalmus', 'Eastern Newt'),
    ('Ondatra', 'Muskrat'),
    ('Sus', 'Sus scrofa'),
    ('Fundulus', 'Mummichog'),
    ('Apeltes', 'Stickleback'),
]
print(f"  {'Taxon':22}  {'Cat Brook':>12}  {'Sawmill School':>14}  {'Sawmill Elm':>12}  {'Sawmill Golf':>12}  {'Sawmill Atwater':>15}")
for genus, common in key_taxa:
    def get_reads(site_pat):
        r = conn.execute("""
          SELECT SUM(r.read_count) FROM esvs e
          JOIN reads r ON r.esv_id = e.esv_id
          JOIN samples s ON s.sample_code = r.sample_code
          WHERE (e.blast_genus=? OR e.genus=?) AND s.site_name LIKE ?
        """, (genus, genus, site_pat)).fetchone()[0]
        return r or 0
    cat    = get_reads('%Cat Brook%')
    school = get_reads('%School%')
    elm    = get_reads('%Elm%')
    golf   = get_reads('%golf%')
    atw    = get_reads('%Atwater%')
    if any([cat, school, elm, golf, atw]):
        print(f"  {common:22}  {cat:12,}  {school:14,}  {elm:12,}  {golf:12,}  {atw:15,}")

conn.close()
