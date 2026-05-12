import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

total = conn.execute("SELECT COUNT(*) FROM esvs").fetchone()[0]

# BEFORE: JV state
jv_with_genus = conn.execute("SELECT COUNT(*) FROM esvs WHERE genus IS NOT NULL AND genus != '' AND genus != 'PositiveControl'").fetchone()[0]
jv_no_genus   = conn.execute("SELECT COUNT(*) FROM esvs WHERE (genus IS NULL OR genus = '')").fetchone()[0]

print("=== BEFORE (JV only) ===")
print(f"Total ESVs:                {total:,}")
print(f"JV had genus:              {jv_with_genus:,}")
print(f"JV had NO genus:           {jv_no_genus:,}")

# AFTER: BLAST results
confirmed = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='confirmed'").fetchone()[0]
resolved  = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='newly resolved'").fetchone()[0]
mismatch  = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE '%MISMATCH%'").fetchone()[0]
no_hit    = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='no hit'").fetchone()[0]
errors    = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE 'error%'").fetchone()[0]
artifact  = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE '%artifact%' OR blast_notes LIKE '%contamination%'").fetchone()[0]

print()
print("=== AFTER (BLAST validated) ===")
print(f"JV confirmed correct:      {confirmed:,}")
print(f"JV wrong (mismatch):       {mismatch:,}")
print(f"Newly identified (no JV):  {resolved:,}")
print(f"No hit:                    {no_hit:,}")
print(f"NCBI errors (unresolved):  {errors:,}")
print(f"Pre-marked artifacts:      {artifact:,}")

jv_attempted = confirmed + mismatch
print()
print("=== JV ACCURACY (where BLAST got a result) ===")
print(f"JV IDd + BLAST confirmed:  {jv_attempted:,}")
print(f"JV correct:                {confirmed:,}  ({100*confirmed/jv_attempted:.1f}%)")
print(f"JV wrong:                  {mismatch:,}  ({100*mismatch/jv_attempted:.1f}%)")

conn.close()
