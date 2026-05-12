import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# Diatom taxa grouped by pH preference — based on published optima
# Acidobionts (pH < 5.5): Eunotia, Pinnularia, Frustulia, Stenopterobia
# Acidophiles (pH 5-6.5): Synura, Dinobryon, Chrysochromulina, Cryptomonas
# Circumneutral (pH 6-7.5): Achnanthidium, Diatoma, Ulnaria, Fragilaria, Chroomonas
# Alkaliphiles / enriched (pH > 7): Stephanocyclus, Nitzschia palea, Rhopalodia, Gomphonema parvulum

ACID_EXTREME   = ['Eunotia','Pinnularia','Frustulia','Stenopterobia']
ACID_MOD       = ['Synura','Dinobryon','Chrysochromulina','Cryptomonas','Hazenia','Monomastix']
CIRCUMNEUTRAL  = ['Achnanthidium','Diatoma','Ulnaria','Fragilaria','Chroomonas','Navicula','Sellaphora']
ALKALINE       = ['Stephanocyclus','Rhopalodia','Gomphonema','Nitzschia','Cyanobium','Synechococcus']
ENRICH_IND     = ['Nitzschia']  # palea specifically

def get_reads(site, genera):
    placeholders = ','.join('?' for _ in genera)
    r = conn.execute(f"""
      SELECT SUM(r.read_count) FROM esvs e
      JOIN reads r ON r.esv_id = e.esv_id
      JOIN samples s ON s.sample_code = r.sample_code
      WHERE s.site_name=? AND e.assay != 'MiFishU'
        AND (e.blast_genus IN ({placeholders}) OR e.genus IN ({placeholders}))
    """, [site] + genera + genera).fetchone()[0] or 0
    return r

print("=== ALGAL pH INFERENCE — site ranking (most acidic to most alkaline) ===")
print("    [Field pH where measured]")
print()

sites = conn.execute("""
  SELECT DISTINCT s.site_name, s.ph_field
  FROM samples s
  JOIN reads r ON r.sample_code = s.sample_code
  JOIN esvs e ON e.esv_id = r.esv_id
  WHERE e.assay != 'MiFishU' AND s.site_name IS NOT NULL AND s.site_name != ''
  ORDER BY s.site_name
""").fetchall()

results = []
for (site, ph) in sites:
    acid_x  = get_reads(site, ACID_EXTREME)
    acid_m  = get_reads(site, ACID_MOD)
    neutral = get_reads(site, CIRCUMNEUTRAL)
    alk     = get_reads(site, ALKALINE)
    total   = acid_x + acid_m + neutral + alk
    if total == 0:
        continue
    # Simple index: weighted pH score (lower = more acidic)
    # Extreme acid weighted 4, moderate acid 5.5, neutral 7, alkaline 8
    score = (acid_x*4.0 + acid_m*5.5 + neutral*7.0 + alk*8.0) / total if total else 7.0

    # Specific enrichment indicator: Nitzschia palea
    npalea = conn.execute("""
      SELECT SUM(r.read_count) FROM esvs e
      JOIN reads r ON r.esv_id = e.esv_id
      JOIN samples s ON s.sample_code = r.sample_code
      WHERE s.site_name=? AND e.assay!='MiFishU'
        AND e.blast_species LIKE '%palea%'
    """, (site,)).fetchone()[0] or 0

    results.append((score, site, ph, acid_x, acid_m, neutral, alk, total, npalea))

results.sort()

print(f"  {'Inferred':>8}  {'Field':>6}  {'Site':42}  {'Acid-X':>7}  {'Acid-M':>7}  {'Neutral':>8}  {'Alkaline':>9}  {'N.palea':>8}")
for r in results:
    score, site, ph, ax, am, neu, alk, tot, np = r
    ph_str = f"pH={ph}" if ph else "     "
    np_flag = '  <<enriched' if np > 100 else ''
    print(f"  {score:8.2f}  {ph_str:>6}  {str(site):42}  {ax:7,}  {am:7,}  {neu:8,}  {alk:9,}  {np:8,}{np_flag}")

print()
print("=== RHOPALODIA (nitrogen-fixing diatom — enrichment indicator) by site ===")
rows = conn.execute("""
  SELECT s.site_name, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE (e.blast_genus='Rhopalodia' OR e.genus='Rhopalodia')
    AND e.assay != 'MiFishU'
  GROUP BY s.site_name ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):42}  {r[1]:,} reads")

conn.close()
