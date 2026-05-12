import sqlite3
conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

print("=== Mashpee / Red Brook / Cape Cod pH data in database ===")
rows = conn.execute("""
    SELECT sample_code, site_name, ph_field, temp_f, field_notes, notes, batch_id
    FROM samples
    WHERE site_name LIKE '%ashpee%'
       OR site_name LIKE '%Red Brook%'
       OR site_name LIKE '%Quashnet%'
       OR site_name LIKE '%Brewster%'
       OR site_name LIKE '%Orleans%'
       OR site_name LIKE '%Santuit%'
    ORDER BY site_name
""").fetchall()
for r in rows:
    print(f"  {r[0]}  {str(r[6]):12}  site={str(r[1]):35}  pH={r[2]}  temp={r[3]}  notes={r[4]}  {r[5]}")

conn.close()
