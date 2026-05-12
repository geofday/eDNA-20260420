import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# 1. Atlantic Salmon BLAST status — critical, federally endangered
print("=== 1. ATLANTIC SALMON — BLAST STATUS ===")
rows = conn.execute("""
    SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
           e.blast_pct, e.blast_notes, LENGTH(e.sequence) as seqlen,
           SUM(r.read_count) as reads
    FROM esvs e LEFT JOIN reads r ON r.esv_id=e.esv_id
    WHERE e.blast_genus='Salmo' OR e.genus='Salmo'
       OR e.blast_species LIKE '%salar%' OR e.species LIKE '%salar%'
       OR e.blast_species LIKE '%trutta%' OR e.species LIKE '%trutta%'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  JV={r[1]} {r[2]}  BLAST={r[3]} {r[4]}  {r[5]}%  seq={r[7]}bp  {r[8]:,}r  [{r[6]}]")

# 2. Geographically implausible species
print("\n=== 2. GEOGRAPHICALLY IMPLAUSIBLE SPECIES ===")
IMPLAUSIBLE = [
    'Taricha', 'Xiphister', 'Platygobio', 'Microtus montanus',
    'Hybognathus', 'Etheostoma', 'Spatula', 'Anas diazi',
    'Sphingopyxis', 'Sturnus'
]
for taxon in IMPLAUSIBLE:
    parts = taxon.split()
    if len(parts) == 2:
        rows = conn.execute("""
            SELECT COALESCE(e.blast_genus,e.genus), COALESCE(e.blast_species,e.species),
                   e.blast_pct, SUM(r.read_count) as reads,
                   COUNT(DISTINCT r.sample_code) as sites
            FROM esvs e JOIN reads r ON r.esv_id=r.esv_id
            WHERE (e.blast_genus=? AND e.blast_species LIKE ?)
               OR (e.genus=? AND e.species LIKE ?)
            GROUP BY e.esv_id ORDER BY reads DESC LIMIT 3
        """, (parts[0], f'%{parts[1]}%', parts[0], f'%{parts[1]}%')).fetchall()
    else:
        rows = conn.execute("""
            SELECT COALESCE(e.blast_genus,e.genus), COALESCE(e.blast_species,e.species),
                   e.blast_pct, SUM(r.read_count) as reads,
                   COUNT(DISTINCT r.sample_code) as sites
            FROM esvs e JOIN reads r ON r.esv_id=r.esv_id
            WHERE e.blast_genus=? OR e.genus=?
            GROUP BY e.esv_id ORDER BY reads DESC LIMIT 3
        """, (taxon, taxon)).fetchall()
    for r in rows:
        if r[3]:
            print(f"  {str(r[0]):20} {str(r[1]):35} {str(r[2]):5}%  {r[3]:,}r  {r[4]} sites")

# 3. Anas diazi — mallard misID check
print("\n=== 3. Anas diazi — likely Mallard misID? ===")
rows = conn.execute("""
    SELECT e.esv_id, e.blast_genus, e.blast_species, e.blast_pct,
           e.blast_notes, SUM(r.read_count) as reads,
           COUNT(DISTINCT r.sample_code) as sites
    FROM esvs e JOIN reads r ON r.esv_id=r.esv_id
    WHERE e.blast_genus='Anas' OR e.genus='Anas'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {r[1]} {r[2]}  {r[3]}%  {r[5]:,}r  {r[6]} sites  [{r[4]}]")

# 4. Salmo salar vs trutta distinguishable at 173bp?
print("\n=== 4. Salmo salar vs trutta sequence comparison ===")
seqs = conn.execute("""
    SELECT e.blast_species, e.blast_pct, e.sequence, SUM(r.read_count) as reads
    FROM esvs e JOIN reads r ON r.esv_id=r.esv_id
    WHERE e.blast_genus='Salmo' OR e.genus='Salmo'
    GROUP BY e.esv_id ORDER BY reads DESC
""").fetchall()
for r in seqs:
    print(f"  {str(r[0]):35} {r[1]}%  {r[3]:,}r")
    if r[2]:
        print(f"    seq: {r[2][:80]}...")

conn.close()
