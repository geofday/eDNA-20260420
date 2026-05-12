import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== UNNAMED SAMPLES — what do we know about them? ===")
rows = conn.execute("""
  SELECT sample_code, batch_id, site_name, lat, lon, capture_time, notes, field_notes
  FROM samples WHERE site_name IS NULL OR site_name = ''
  ORDER BY batch_id, sample_code
""").fetchall()
print(f"  Total unnamed samples: {len(rows)}")
print()
for r in rows:
    print(f"  {r[0]}  batch={str(r[1]):15}  lat={str(r[2]):10}  lon={str(r[3]):10}  time={str(r[4]):20}  notes={str(r[5])}  field={str(r[6])}")

print()
print("=== UNNAMED SAMPLES — batch distribution ===")
rows = conn.execute("""
  SELECT batch_id, COUNT(*) as n
  FROM samples WHERE site_name IS NULL OR site_name = ''
  GROUP BY batch_id ORDER BY batch_id
""").fetchall()
for r in rows:
    print(f"  batch={str(r[0]):20}  {r[1]} samples")

print()
print("=== THE AMERICAN SHAD ESV — which samples contain it? ===")
rows = conn.execute("""
  SELECT r.sample_code, s.batch_id, s.site_name, s.lat, s.lon,
         s.capture_time, s.notes, r.read_count
  FROM reads r
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE r.esv_id = 'ESV_007836'
  ORDER BY r.read_count DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  batch={str(r[1]):15}  site={str(r[2]):30}  lat={str(r[3])}  lon={str(r[4])}  time={str(r[5])}  reads={r[7]}  notes={str(r[6])}")

print()
print("=== UNNAMED SAMPLES — full fish community ===")
rows = conn.execute("""
  SELECT e.blast_genus, e.blast_species, e.blast_pct,
         SUM(r.read_count) as reads, COUNT(DISTINCT e.esv_id) as n
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  JOIN samples s ON s.sample_code = r.sample_code
  WHERE (s.site_name IS NULL OR s.site_name = '')
    AND e.assay = 'MiFishU'
    AND e.blast_genus NOT IN ('Struthio','Homo')
    AND e.blast_genus IS NOT NULL
  GROUP BY e.blast_genus, e.blast_species, e.blast_pct
  ORDER BY reads DESC LIMIT 30
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):22} {str(r[1]):40} {str(r[2]):5}%  {r[3]:8,} reads  [{r[4]} ESVs]")

print()
print("=== UNNAMED SAMPLES — batch co-occurrence with known sites ===")
# Find which batches the unnamed samples are in, then find other samples in same batch
none_batches = conn.execute("""
  SELECT DISTINCT batch_id FROM samples WHERE site_name IS NULL OR site_name=''
""").fetchall()
for (batch,) in none_batches:
    if batch:
        named = conn.execute("""
          SELECT DISTINCT site_name FROM samples
          WHERE batch_id=? AND site_name IS NOT NULL AND site_name != ''
          LIMIT 8
        """, (batch,)).fetchall()
        unnamed_n = conn.execute("""
          SELECT COUNT(*) FROM samples WHERE batch_id=? AND (site_name IS NULL OR site_name='')
        """, (batch,)).fetchone()[0]
        print(f"  Batch {batch}: {unnamed_n} unnamed + named sites: {[s[0] for s in named]}")

conn.close()
