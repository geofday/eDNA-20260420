import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== UNNAMED SAMPLES — algal fingerprint by batch ===")
print("    (comparing to known site profiles)\n")

unnamed_batches = [
    ('JVB3759', ['D8F0GB5R.1']),
    ('JVB3787', ['4JSG0AYS.1','5K41GBHR.1','C42JWLMM.1','F5LP8C1M.1',
                 'L08BN6EZ.1','OTLHJZBA.1','TYKBU74R.1','UG79PNJS.1',
                 'UH7L508D.1','WRMXR4RT.1']),
    ('JVB3988', ['FYREF4C4.1','O5S2DTMM.1','VD2H2Z3Q.1','ZAGSQ1TX.1']),
    ('JVB4981', ['I866I93J.1']),
    ('JVB5776', ['CA66THTZ.1','CVVU52A9.1']),
]

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

def get_taxa_reads(samples):
    placeholders = ','.join('?' for _ in samples)
    results = {}
    for genus, cat in KEY_TAXA:
        r = conn.execute(f"""
          SELECT SUM(r.read_count) FROM esvs e
          JOIN reads r ON r.esv_id = e.esv_id
          WHERE r.sample_code IN ({placeholders})
            AND e.assay != 'MiFishU'
            AND (e.blast_genus=? OR e.genus=?)
        """, samples + [genus, genus]).fetchone()[0] or 0
        results[genus] = r
    total = conn.execute(f"""
      SELECT SUM(r.read_count) FROM reads r
      JOIN esvs e ON e.esv_id = r.esv_id
      WHERE r.sample_code IN ({placeholders}) AND e.assay != 'MiFishU'
    """, samples).fetchone()[0] or 1
    return results, total

# Print each unnamed batch profile
for batch, samples in unnamed_batches:
    taxa, total = get_taxa_reads(samples)
    print(f"  Batch {batch} ({len(samples)} samples, {total:,} total algal reads):")
    dominant = [(v,k) for k,v in taxa.items() if v > 0]
    dominant.sort(reverse=True)
    for reads, genus in dominant[:8]:
        cat = next(c for g,c in KEY_TAXA if g==genus)
        pct = reads/total*100
        print(f"    {str(genus):20} {reads:7,} reads ({pct:4.1f}%)  [{cat}]")
    print()

# Now compare to the known-site profiles using inferred pH score
print("=== BEST MATCH: unnamed batch vs. known sites ===\n")

# Get algal profile for each named site
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
    if site_samples:
        taxa, total = get_taxa_reads(site_samples)
        site_profiles[site] = (taxa, total, ph)

def similarity(a_taxa, a_tot, b_taxa, b_tot):
    # Simple cosine-like similarity on relative abundances
    score = 0
    for genus, _ in KEY_TAXA:
        pa = a_taxa.get(genus,0) / a_tot if a_tot else 0
        pb = b_taxa.get(genus,0) / b_tot if b_tot else 0
        score += pa * pb
    return score

for batch, samples in unnamed_batches:
    u_taxa, u_tot = get_taxa_reads(samples)
    if u_tot < 100:
        continue
    scores = []
    for site, (s_taxa, s_tot, ph) in site_profiles.items():
        sim = similarity(u_taxa, u_tot, s_taxa, s_tot)
        scores.append((sim, site, ph))
    scores.sort(reverse=True)
    print(f"  Batch {batch} best matches:")
    for sim, site, ph in scores[:5]:
        ph_str = f"pH={ph}" if ph else "     "
        print(f"    {sim:.4f}  {ph_str:>6}  {site}")
    print()

conn.close()
