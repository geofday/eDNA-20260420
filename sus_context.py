import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== SAMPLES WITH Sus scrofa READS ===\n")

sus_samples = conn.execute("""
    SELECT r.sample_code, s.site_name, s.batch_id, SUM(r.read_count) as sus_reads
    FROM reads r
    JOIN esvs e ON e.esv_id = r.esv_id
    JOIN samples s ON s.sample_code = r.sample_code
    WHERE (e.blast_genus='Sus' OR e.genus='Sus'
        OR e.blast_species LIKE '%scrofa%' OR e.species LIKE '%scrofa%')
    GROUP BY r.sample_code
    ORDER BY sus_reads DESC
""").fetchall()

print(f"  {'Sample':15} {'Batch':12} {'Sus reads':>10}  Site")
for sc, site, batch, sus in sus_samples:
    print(f"  {str(sc):15} {str(batch):12} {sus:10,}  {site}")
print()

# For each Sus sample, show all non-fish vertebrates + key indicators
INDICATORS = [
    'Sus', 'Homo', 'Bos', 'Ovis', 'Capra', 'Equus',  # livestock / human
    'Gallus', 'Meleagris',                              # poultry
    'Ondatra', 'Castor', 'Procyon', 'Mephitis',        # native mammals
    'Rattus', 'Mus',                                    # rodents
    'Canis', 'Felis',                                   # pets/feral
]

for sc, site, batch, sus_reads in sus_samples:
    total = conn.execute("""
        SELECT SUM(r.read_count) FROM reads r JOIN esvs e ON e.esv_id=r.esv_id
        WHERE r.sample_code=? AND e.assay='MiFishU'
    """, (sc,)).fetchone()[0] or 1

    print(f"--- {sc} | {batch} | {site} | Sus={sus_reads:,} reads ---")

    # All non-fish vertebrates
    others = conn.execute("""
        SELECT COALESCE(e.blast_genus,e.genus) as g,
               COALESCE(e.blast_species,e.species) as sp,
               SUM(r.read_count) as reads
        FROM reads r JOIN esvs e ON e.esv_id=r.esv_id
        WHERE r.sample_code=? AND e.assay='MiFishU'
          AND COALESCE(e.blast_genus,e.genus) NOT IN (
              'Struthio','Oncorhynchus','Salmo','Salvelinus','Esox',
              'Lepomis','Micropterus','Perca','Ameiurus','Catostomus',
              'Notemigonus','Fundulus','Alosa','Clupea','Anguilla',
              'Apeltes','Gasterosteus','Menidia','Stenotomus','Morone',
              'Brevoortia','Acipenser','Cyprinus','Carassius','Scomber',
              'Lophius','Phoxinus','Chrosomus','Microgadus','Hyperoplus',
              'Tautogolabrus','Pholis','Pomatomus','Chrysemys'
          )
          AND COALESCE(e.blast_genus,e.genus) IS NOT NULL
        GROUP BY g, sp ORDER BY reads DESC
    """, (sc,)).fetchall()

    for g, sp, reads in others:
        pct = reads/total*100
        tag = ''
        if g in ['Sus','Bos','Ovis','Capra','Gallus','Meleagris','Equus']:
            tag = '  [AGRICULTURAL]'
        elif g in ['Homo']:
            tag = '  [HUMAN]'
        elif g in ['Ondatra','Castor','Procyon','Mephitis','Neovison']:
            tag = '  [NATIVE MAMMAL]'
        elif g in ['Rattus','Mus']:
            tag = '  [RODENT]'
        print(f"  {str(g):20} {str(sp)[:40]:40} {reads:7,} ({pct:.1f}%){tag}")
    print()

conn.close()
