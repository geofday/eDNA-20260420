import sqlite3, openpyxl

conn = sqlite3.connect(r'c:\repos\eDNA-20270420\edna.db')

# Create table
conn.execute("DROP TABLE IF EXISTS ccro_ph")
conn.execute("""
    CREATE TABLE ccro_ph (
        river       TEXT,
        month       INTEGER,
        month_name  TEXT,
        ph_avg      REAL,
        ph_stddev   REAL,
        source      TEXT DEFAULT 'Cape Cod Rivers Observatory (CCRO)'
    )
""")

RIVERS = ['Santuit', 'Mashpee', 'Quashnet', 'Coonamesset', 'Herring River', 'Red Brook']
MONTHS = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
          7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

wb = openpyxl.load_workbook(r'C:\Users\geofd\Downloads\Modified_CCRO_pH_Data.xlsx')
ws = wb['pH_Monthly_Summary']

# Monthly averages: rows 2-13 (month 1-12), cols C-H (index 2-7)
avg_rows = {}
for row in ws.iter_rows(min_row=2, max_row=13, values_only=True):
    month = row[0]
    if isinstance(month, int) and 1 <= month <= 12:
        avg_rows[month] = list(row[2:8])  # Santuit, Mashpee, Quashnet, Coonamesset, Herring River, Red Brook

# StdDev section: rows with integer month in col A in the StdDev block (rows 22-33)
stddev_rows = {}
for row in ws.iter_rows(min_row=22, max_row=33, values_only=True):
    month = row[0]
    if isinstance(month, int) and 1 <= month <= 12:
        stddev_rows[month] = list(row[2:8])

# Insert
for month in range(1, 13):
    avgs = avg_rows.get(month, [None]*6)
    stds = stddev_rows.get(month, [None]*6)
    for i, river in enumerate(RIVERS):
        conn.execute("""
            INSERT INTO ccro_ph (river, month, month_name, ph_avg, ph_stddev)
            VALUES (?,?,?,?,?)
        """, (river, month, MONTHS[month],
              round(avgs[i], 4) if avgs[i] else None,
              round(stds[i], 4) if i < len(stds) and stds[i] else None))

conn.commit()

# Verify
print("=== CCRO pH loaded — annual summary ===\n")
print(f"  {'River':20} {'Ann.Avg':>8}  {'Min Mo':>8}  {'Min pH':>7}  {'Max Mo':>8}  {'Max pH':>7}")
for river in RIVERS:
    rows = conn.execute("""
        SELECT month_name, ph_avg FROM ccro_ph
        WHERE river=? ORDER BY month
    """, (river,)).fetchall()
    vals = [(m, p) for m, p in rows if p]
    avg = sum(p for _, p in vals) / len(vals)
    mn = min(vals, key=lambda x: x[1])
    mx = max(vals, key=lambda x: x[1])
    print(f"  {river:20} {avg:8.3f}  {str(mn[0]):>8}  {mn[1]:7.3f}  {str(mx[0]):>8}  {mx[1]:7.3f}")

print(f"\n  Table rows loaded: {conn.execute('SELECT COUNT(*) FROM ccro_ph').fetchone()[0]}")

# Full Red Brook table
print("\n=== Red Brook pH by month (CCRO) ===")
rows = conn.execute("""
    SELECT month, month_name, ph_avg, ph_stddev FROM ccro_ph
    WHERE river='Red Brook' ORDER BY month
""").fetchall()
for r in rows:
    bar = '#' * int((r[2]-5.0)*10) if r[2] else ''
    print(f"  Month {r[0]:2} ({str(r[1]):10})  pH={r[2]:.3f}  ±{str(round(r[3],3)) if r[3] else '?':6}  {bar}")

conn.close()
