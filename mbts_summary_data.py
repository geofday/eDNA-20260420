import sys, io, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
conn = sqlite3.connect(r'c:\repos\eDNA-20260420\edna.db')

MBTS_CODES = [
    'CVVU52A9.1','CDWD42KP.1','C4SUMTFY.1','5K41GBHR.1','UG79PNJS.1',
    'OTLHJZBA.1','NVN8LUTP.1','OC41MHKC.1','UTEVR3WT.1','LZAC7T2X.1',
    'AEFBOYWK.1','KXUG2Y6J.1','2KL87R0I.1','HVFHCKJQ.1',
]
placeholders = ','.join('?' * len(MBTS_CODES))

print('=== BROOK TROUT + pH per site ===')
rows = conn.execute(f"""
    SELECT
        s.sample_code,
        COALESCE(s.site_name, s.canonical_site) as site,
        s.capture_time,
        s.ph_field,
        SUM(CASE WHEN e.blast_species LIKE '%fontinalis%' OR e.species LIKE '%fontinalis%'
                 THEN r.read_count ELSE 0 END) as bt_reads,
        SUM(CASE WHEN e.blast_genus NOT IN ('Struthio','Homo')
                 THEN r.read_count ELSE 0 END) as fish_reads
    FROM samples s
    JOIN reads r ON r.sample_code = s.sample_code
    JOIN esvs e ON e.esv_id = r.esv_id
    WHERE s.sample_code IN ({placeholders})
    AND e.assay = 'MiFishU'
    GROUP BY s.sample_code
    HAVING fish_reads > 0
    ORDER BY s.capture_time
""", MBTS_CODES).fetchall()

for sc, site, ct, ph, bt, fish in rows:
    pct = bt/fish*100 if fish else 0
    ph_str = f"pH {ph:.1f}" if ph else 'pH --'
    print(f"  {ct or '?':12s}  {site[:32]:32s}  BT={pct:5.1f}%  ({bt:5,}/{fish:6,})  {ph_str}")

print()
print('=== SENTINEL / INVASIVE FISH per MBTS site ===')
WATCH = ['carpio','promelas','salmoides','dolomieu','trutta','salar','salmonid',
         'alewife','pseudoharengus','saltator','majalis','gibbosus','nebulosus']
rows2 = conn.execute(f"""
    SELECT
        s.sample_code,
        COALESCE(s.site_name, s.canonical_site) as site,
        COALESCE(e.blast_species, e.species, e.blast_genus, e.genus) as name,
        r.read_count,
        SUM(CASE WHEN e.blast_genus NOT IN ('Struthio','Homo')
                 THEN r.read_count ELSE 0 END) OVER (PARTITION BY s.sample_code) as fish_total
    FROM samples s
    JOIN reads r ON r.sample_code = s.sample_code
    JOIN esvs e ON e.esv_id = r.esv_id
    WHERE s.sample_code IN ({placeholders})
    AND e.assay = 'MiFishU'
    AND ({' OR '.join(["LOWER(COALESCE(e.blast_species,'')) LIKE '%" + w + "%' OR LOWER(COALESCE(e.species,'')) LIKE '%" + w + "%'" for w in WATCH])})
    AND e.blast_genus NOT IN ('Struthio','Homo')
    ORDER BY s.sample_code, r.read_count DESC
""", MBTS_CODES).fetchall()

prev = None
for sc, site, name, cnt, total in rows2:
    if sc != prev:
        print(f"\n  {site} ({sc})")
        prev = sc
    pct = cnt/total*100 if total else 0
    print(f"    {pct:5.1f}%  {cnt:5,}  {name}")

conn.close()
