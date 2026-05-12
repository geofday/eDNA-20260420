import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')
conn.execute("""
    UPDATE esvs
    SET blast_species = 'Characeae sp. (native stonewort)',
        blast_notes   = 'BLAST 95.8% to Nitellopsis obtusa — insufficient for species ID; likely native Chara or Nitella spp. Site is tidal/coastal Sawmill Brook Manchester MA; N. obtusa is freshwater-only invasive; 23S database for Characeae is sparse'
    WHERE esv_id = 'ESV_100357'
""")
conn.commit()
n = conn.execute("SELECT blast_species, blast_notes FROM esvs WHERE esv_id='ESV_100357'").fetchone()
print(f'Updated: {n[0]}')
print(f'Note:    {n[1]}')
conn.close()
