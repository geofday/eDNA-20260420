import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

SAMPLE = 'I866I93J.1'

KEY_TAXA = [
    ('Eunotia',          'Acid-X'),
    ('Pinnularia',       'Acid-X'),
    ('Synura',           'Oligo'),
    ('Dinobryon',        'Oligo'),
    ('Chrysochromulina', 'Oligo'),
    ('Cryptomonas',      'Oligo'),
    ('Epipyxis',         'Oligo'),
    ('Achnanthidium',    'Neutral'),
    ('Diatoma',          'Neutral'),
    ('Chroomonas',       'Neutral'),
    ('Stephanocyclus',   'Alk'),
    ('Cyanobium',        'Alk'),
    ('Synechococcus',    'Alk'),
    ('Teleaulax',        'Tidal'),
    ('Ostreococcus',     'Tidal'),
    ('Nitellopsis',      'Aquatic-plant'),
    ('Toona',            'Ornamental'),
    ('Rhopalodia',       'Enrich'),
]

print(f"=== MYSTERY SAMPLE: {SAMPLE} (JVB4981) ===\n")

# Basic metadata
meta = conn.execute("""
    SELECT batch_id, site_name, lat, lon, capture_time, notes, field_notes
    FROM samples WHERE sample_code=?
""", (SAMPLE,)).fetchone()
if meta:
    print(f"  batch={meta[0]}  site={meta[1]}  lat={meta[2]}  lon={meta[3]}")
    print(f"  time={meta[4]}  notes={meta[5]}  field={meta[6]}")
print()

# Fish community
print("--- Fish (MiFishU) ---")
fish = conn.execute("""
    SELECT e.blast_genus, e.blast_species, e.blast_pct, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE r.sample_code=? AND e.assay='MiFishU'
      AND e.blast_genus NOT IN ('Struthio','Homo')
      AND e.blast_genus IS NOT NULL
    GROUP BY e.blast_genus, e.blast_species, e.blast_pct
    ORDER BY reads DESC LIMIT 15
""", (SAMPLE,)).fetchall()
fish_total = sum(r[3] for r in fish) or 1
for r in fish:
    print(f"  {str(r[0]):22} {str(r[1]):35} {str(r[2]):5}%  {r[3]:7,} reads ({r[3]/fish_total*100:.1f}%)")
print()

# Algal community — all taxa
print("--- Algae (23S) — top 20 ---")
algae = conn.execute("""
    SELECT COALESCE(e.blast_genus, e.genus, '?') as genus,
           COALESCE(e.blast_species, e.species, '?') as species,
           SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE r.sample_code=? AND e.assay!='MiFishU'
    GROUP BY genus, species ORDER BY reads DESC LIMIT 20
""", (SAMPLE,)).fetchall()
alg_total = conn.execute("""
    SELECT SUM(r.read_count) FROM reads r JOIN esvs e ON e.esv_id=r.esv_id
    WHERE r.sample_code=? AND e.assay!='MiFishU'
""", (SAMPLE,)).fetchone()[0] or 1
for r in algae:
    print(f"  {str(r[0]):22} {str(r[1]):35}  {r[2]:7,} reads ({r[2]/alg_total*100:.1f}%)")
print(f"  Total algal reads: {alg_total:,}")
print()

# Key taxa fingerprint
print("--- Key taxa fingerprint ---")
taxa_reads = {}
for genus, cat in KEY_TAXA:
    n = conn.execute("""
        SELECT SUM(r.read_count) FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
        WHERE r.sample_code=? AND e.assay!='MiFishU'
          AND (e.blast_genus=? OR e.genus=?)
    """, (SAMPLE, genus, genus)).fetchone()[0] or 0
    taxa_reads[genus] = n
    if n > 0:
        print(f"  {str(genus):20} {n:6,} reads ({n/alg_total*100:.1f}%)  [{cat}]")
print()

# Cosine similarity against all named sites
print("--- Best site matches (cosine similarity on algal profile) ---")
site_profiles = {}
sites = conn.execute("""
    SELECT DISTINCT s.site_name, s.ph_field
    FROM samples s JOIN reads r ON r.sample_code=s.sample_code
    JOIN esvs e ON e.esv_id=r.esv_id
    WHERE e.assay!='MiFishU' AND s.site_name IS NOT NULL AND s.site_name!=''
""").fetchall()

for (site, ph) in sites:
    site_samples = [r[0] for r in conn.execute(
        "SELECT sample_code FROM samples WHERE site_name=?", (site,)).fetchall()]
    if not site_samples:
        continue
    placeholders = ','.join('?' for _ in site_samples)
    s_taxa = {}
    for genus, cat in KEY_TAXA:
        n = conn.execute(f"""
            SELECT SUM(r.read_count) FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
            WHERE r.sample_code IN ({placeholders}) AND e.assay!='MiFishU'
              AND (e.blast_genus=? OR e.genus=?)
        """, site_samples + [genus, genus]).fetchone()[0] or 0
        s_taxa[genus] = n
    s_tot = conn.execute(f"""
        SELECT SUM(r.read_count) FROM reads r JOIN esvs e ON e.esv_id=r.esv_id
        WHERE r.sample_code IN ({placeholders}) AND e.assay!='MiFishU'
    """, site_samples).fetchone()[0] or 1
    site_profiles[site] = (s_taxa, s_tot, ph)

scores = []
for site, (s_taxa, s_tot, ph) in site_profiles.items():
    score = sum(
        (taxa_reads.get(g, 0) / alg_total) * (s_taxa.get(g, 0) / s_tot)
        for g, _ in KEY_TAXA
    )
    scores.append((score, site, ph))
scores.sort(reverse=True)

for sim, site, ph in scores[:10]:
    ph_str = f"pH={ph}" if ph else "     "
    print(f"  {sim:.4f}  {ph_str:>6}  {site}")

conn.close()
