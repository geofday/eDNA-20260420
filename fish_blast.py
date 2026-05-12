import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== FISH (MiFishU) BLAST SUMMARY ===")
fish_total    = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU'").fetchone()[0]
fish_blasted  = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_genus IS NOT NULL").fetchone()[0]
fish_confirm  = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_notes='confirmed'").fetchone()[0]
fish_resolved = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_notes='newly resolved'").fetchone()[0]
fish_mismatch = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_notes LIKE '%MISMATCH%'").fetchone()[0]
fish_nohit    = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_notes='no hit'").fetchone()[0]
fish_error    = conn.execute("SELECT COUNT(*) FROM esvs WHERE assay='MiFishU' AND blast_notes LIKE 'error%'").fetchone()[0]
print(f"Total MiFishU ESVs:        {fish_total:,}")
print(f"Confirmed (JV=BLAST):      {fish_confirm:,}")
print(f"Newly resolved:            {fish_resolved:,}")
print(f"Mismatched:                {fish_mismatch:,}")
print(f"No hit:                    {fish_nohit:,}")
print(f"NCBI errors:               {fish_error:,}")

print()
print("=== FISH MISMATCHES ===")
rows = conn.execute("""
  SELECT genus, species, blast_genus, blast_species, blast_pct, COUNT(*) as n
  FROM esvs WHERE assay='MiFishU' AND blast_notes LIKE '%MISMATCH%'
  GROUP BY genus, species, blast_genus, blast_species ORDER BY n DESC
""").fetchall()
for r in rows:
    print(f"  JV={str(r[0])} {str(r[1]):25} => BLAST={str(r[2])} {str(r[3]):25} ({r[4]:.1f}%)  [{r[5]}x]")

print()
print("=== NEWLY RESOLVED FISH (no JV genus, BLAST identified) ===")
rows = conn.execute("""
  SELECT blast_genus, blast_species, blast_pct, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.assay='MiFishU' AND e.blast_notes='newly resolved'
  GROUP BY blast_genus, blast_species ORDER BY reads DESC LIMIT 20
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):20} {str(r[1]):30} {r[2]:.1f}%  [{r[3]}x ESVs  {r[4]:,} reads]")

print()
print("=== ALL CONFIRMED FISH by read count ===")
rows = conn.execute("""
  SELECT e.genus, e.species, e.blast_pct, COUNT(*) as n, SUM(r.read_count) as reads
  FROM esvs e
  JOIN reads r ON r.esv_id = e.esv_id
  WHERE e.assay='MiFishU' AND e.blast_notes='confirmed'
  GROUP BY e.genus, e.species ORDER BY reads DESC LIMIT 30
""").fetchall()
for r in rows:
    print(f"  {str(r[0]):20} {str(r[1]):30} {r[2]:.1f}%  [{r[3]}x ESVs  {r[4]:,} reads]")

print()
print("=== FISH ERRORS — JV had ID (these we have to trust JV) ===")
rows = conn.execute("""
  SELECT genus, species, COUNT(*) as n
  FROM esvs WHERE assay='MiFishU' AND blast_notes LIKE 'error%'
    AND genus IS NOT NULL AND genus != ''
  GROUP BY genus, species ORDER BY n DESC
""").fetchall()
for r in rows:
    print(f"  JV={str(r[0]):20} {str(r[1]):30}  [{r[2]}x]")

conn.close()
