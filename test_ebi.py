"""Debug EBI BLAST API submission."""
import requests, sqlite3

conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
seq = conn.execute("SELECT sequence FROM esvs WHERE esv_id='ESV_010038'").fetchone()[0]
conn.close()

EBI_BASE = 'https://www.ebi.ac.uk/Tools/services/rest/ncbiblast'

# First, check what databases are valid
print('=== Valid databases (first 400 chars) ===')
r = requests.get(f'{EBI_BASE}/parameterdetails/database', timeout=15)
print(r.text[:800])
print()

# Try submission with FASTA-formatted sequence, no 'format' param
fasta_seq = f'>query\n{seq}'
params = {
    'email':      'geofday@gmail.com',
    'program':    'blastn',
    'database':   'em_rel_std',
    'sequence':   fasta_seq,
    'stype':      'dna',
    'exp':        '1e-10',
    'scores':     '5',
    'alignments': '5',
}
print('=== Submitting test job ===')
r = requests.post(f'{EBI_BASE}/run', data=params, timeout=30)
print(f'HTTP {r.status_code}')
print(r.text[:400])
