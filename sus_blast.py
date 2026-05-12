import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== Sus scrofa ESVs — JV vs BLAST ===\n")

rows = conn.execute("""
    SELECT e.esv_id, e.genus, e.species, e.blast_genus, e.blast_species,
           e.blast_pct, e.blast_notes, LENGTH(e.sequence) as seqlen,
           SUM(r.read_count) as reads
    FROM esvs e
    LEFT JOIN reads r ON r.esv_id = e.esv_id
    WHERE e.genus='Sus' OR e.species LIKE '%scrofa%'
       OR e.blast_genus='Sus' OR e.blast_species LIKE '%scrofa%'
    GROUP BY e.esv_id
    ORDER BY reads DESC
""").fetchall()

for r in rows:
    esv, jv_g, jv_sp, bl_g, bl_sp, pct, notes, seqlen, reads = r
    print(f"  {esv}")
    print(f"    JV:    {jv_g} {jv_sp}")
    print(f"    BLAST: {bl_g} {bl_sp}  {pct}%  seq={seqlen}bp")
    if notes:
        print(f"    Notes: {notes}")
    print(f"    Reads: {reads:,}")
    print()

# Also check what else BLAST hits at same % for Sus sequences
print("=== Sus sequence length context ===")
print("(MiFishU is 173bp — Sus scrofa 12S is similar length to many mammals)")
print()
print("Key: at 173bp, Sus scrofa 12S overlaps with other Suidae and some other")
print("mammals. BLAST top hit does not rule out closely related species.")

conn.close()
