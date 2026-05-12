import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

no_seq = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_genus IS NULL AND (sequence IS NULL OR LENGTH(sequence) <= 50)").fetchone()[0]
has_seq = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_genus IS NULL AND sequence IS NOT NULL AND LENGTH(sequence) > 50").fetchone()[0]
print(f'Unblasted — no/short sequence (expected):  {no_seq:,}')
print(f'Unblasted — has sequence, missed (should be 0): {has_seq:,}')
print()

confirmed  = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='confirmed'").fetchone()[0]
resolved   = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='newly resolved'").fetchone()[0]
mismatches = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE '%MISMATCH%'").fetchone()[0]
no_hit     = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes='no hit'").fetchone()[0]
errors     = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE 'error%'").fetchone()[0]
premarket  = conn.execute("SELECT COUNT(*) FROM esvs WHERE blast_notes LIKE '%artifact%' OR blast_notes LIKE '%contamination%'").fetchone()[0]

print('=== FINAL BLAST SUMMARY ===')
print(f'Confirmed (JV matches BLAST):  {confirmed:,}')
print(f'Newly resolved (no JV genus):  {resolved:,}')
print(f'Mismatches (JV != BLAST):      {mismatches:,}')
print(f'No hit:                        {no_hit:,}')
print(f'Errors:                        {errors:,}')
print(f'Pre-marked artifacts:          {premarket:,}')
print()

print('=== TOP MISMATCHES ===')
rows = conn.execute("""
  SELECT genus, blast_genus, COUNT(*) as n
  FROM esvs WHERE blast_notes LIKE '%MISMATCH%'
  GROUP BY genus, blast_genus ORDER BY n DESC
""").fetchall()
for r in rows:
    print(f'  JV={str(r[0]):22} => BLAST={str(r[1]):22}  ({r[2]}x)')

conn.close()
