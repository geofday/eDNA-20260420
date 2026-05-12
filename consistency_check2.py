import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# 1. Atlantic Salmon — confirmed ESVs only
print("=== 1. SALMO ESVs — BLAST STATUS ===")
rows = conn.execute("""
    SELECT e.esv_id, e.blast_species, e.blast_pct, e.blast_notes,
           LENGTH(e.sequence) as seqlen, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Salmo' OR e.genus='Salmo'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    flag = 'CONFIRMED' if r[2] and r[2]>=99 else ('UNCONFIRMED' if not r[2] else f'{r[2]}%')
    print(f"  {r[0]}  {str(r[1]):35} {flag:12}  {r[4]}bp  {r[5]:,}r  [{r[3]}]")

# 2. Taricha — likely Notophthalmus misID
print("\n=== 2. TARICHA — likely Notophthalmus misidentification? ===")
rows = conn.execute("""
    SELECT e.esv_id, e.blast_species, e.blast_pct, e.blast_notes,
           SUM(r.read_count) as reads, COUNT(DISTINCT r.sample_code) as sites
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Taricha' OR e.genus='Taricha'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):40} {str(r[2]):5}%  {r[4]:,}r  {r[5]} sites  [{r[3]}]")

# 3. Anas diazi
print("\n=== 3. Anas diazi — Mallard misID? ===")
rows = conn.execute("""
    SELECT e.esv_id, e.blast_species, e.blast_pct, e.blast_notes,
           SUM(r.read_count) as reads, COUNT(DISTINCT r.sample_code) as sites
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Anas' OR e.genus='Anas'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):40} {str(r[2]):5}%  {r[4]:,}r  {r[5]} sites  [{r[3]}]")

# 4. Clearly implausible species
print("\n=== 4. CLEARLY IMPLAUSIBLE SPECIES (Pacific/Great Plains) ===")
IMPLAUSIBLE = ['Taricha','Xiphister','Platygobio']
for genus in IMPLAUSIBLE:
    rows = conn.execute("""
        SELECT e.esv_id, COALESCE(e.blast_genus,e.genus),
               COALESCE(e.blast_species,e.species), e.blast_pct,
               SUM(r.read_count) as reads, COUNT(DISTINCT r.sample_code) as sites
        FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
        WHERE e.blast_genus=? OR e.genus=?
        GROUP BY e.esv_id ORDER BY reads DESC
    """, (genus, genus)).fetchall()
    for r in rows:
        print(f"  {r[0]}  {str(r[1]):15} {str(r[2]):38} {str(r[3]):5}%  {r[4]:,}r  {r[5]} sites")

# 5. Xiphister specifically
rows = conn.execute("""
    SELECT e.esv_id, COALESCE(e.blast_genus,e.genus),
           COALESCE(e.blast_species,e.species), e.blast_pct,
           SUM(r.read_count) as reads, COUNT(DISTINCT r.sample_code) as sites
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Xiphister' OR e.genus='Xiphister'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):15} {str(r[2]):38} {str(r[3]):5}%  {r[4]:,}r  {r[5]} sites")

# 6. Etheostoma — actually valid in NE?
print("\n=== 5. ETHEOSTOMA olmstedi — valid in New England ===")
rows = conn.execute("""
    SELECT e.esv_id, COALESCE(e.blast_species,e.species), e.blast_pct,
           s.site_name, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    JOIN samples s ON s.sample_code=r.sample_code
    WHERE e.blast_genus='Etheostoma' OR e.genus='Etheostoma'
    GROUP BY e.esv_id, s.site_name ORDER BY reads DESC LIMIT 10
""").fetchall()
for r in rows:
    print(f"  {str(r[1]):40} {str(r[2]):5}%  {r[4]:,}r  {r[3]}")

# 7. Microtus montanus — western vole
print("\n=== 6. MICROTUS montanus — western species? ===")
rows = conn.execute("""
    SELECT e.esv_id, COALESCE(e.blast_species,e.species), e.blast_pct,
           e.blast_notes, SUM(r.read_count) as reads,
           COUNT(DISTINCT r.sample_code) as sites
    FROM esvs e JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Microtus' OR e.genus='Microtus'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[1]):40} {str(r[2]):5}%  {r[4]:,}r  {r[5]} sites  [{r[3]}]")

conn.close()
