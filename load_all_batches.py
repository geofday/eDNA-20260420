"""
load_all_batches.py — Load all JVB batches into edna.db.

MiFish + 23S:  JVB3759, JVB3787, JVB3988, JVB4307, JVB4678, JVB5776
MiFish only:   JVB4279, JVB4846, JVB4981
Already in DB: JVB5403 (INSERT OR IGNORE handles duplicates safely)
qPCR:          JVB4683 (separate table)
"""

import sqlite3
import csv
import glob
import os
from pathlib import Path

DB_PATH = r'C:\repos\eDNA-20270420\edna.db'

SEARCH_ROOTS = [
    r'F:\RESCUE_USERS\geofd\Downloads',
    r'C:\Users\geofd\Downloads\jonahdna',
    r'C:\Users\geofd\Downloads',
    r'C:\Users\geofd\OneDrive\LOCAL - NON - Onedrive - Storage - 2024',
]

QPCR_SCHEMA = """
CREATE TABLE IF NOT EXISTS qpcr_results (
    sample_code   TEXT REFERENCES samples(sample_code),
    batch_id      TEXT,
    assay         TEXT,        -- e.g. BrookTrout01
    rep1          REAL,
    rep2          REAL,
    rep3          REAL,
    avg_copy_num  REAL,
    pct_detection REAL,
    PRIMARY KEY (sample_code, assay)
);
CREATE INDEX IF NOT EXISTS idx_qpcr_sample ON qpcr_results(sample_code);
CREATE INDEX IF NOT EXISTS idx_qpcr_assay  ON qpcr_results(assay);
"""

FIXED_READ_COLS = {
    'TestId','ESVId','sequence','Kingdom','Phylum','Class',
    'Order','Family','Genus','Species','% match','# species',
    'Common Name','Unnamed: 17'
}

MANIFEST_PATH = r'C:\Users\geofd\OneDrive\LOCAL - NON - Onedrive - Storage - 2024\JV_MASTER_BEST_20260413 (version 2).xlsx'


# ── File finder ───────────────────────────────────────────────────────────────

def find_file(batch: str, pattern: str) -> str | None:
    """Find best matching file for batch+pattern across all search roots."""
    candidates = []
    for root in SEARCH_ROOTS:
        candidates += glob.glob(f'{root}/**/{batch}-{pattern}*.csv', recursive=True)
        candidates += glob.glob(f'{root}/{batch}-{pattern}*.csv')

    if not candidates:
        return None

    # Prefer: FINAL > no-parens > (1) > (2) etc; avoid ESV_Double_Check dirs
    def score(p):
        name = Path(p).name
        in_subdir_penalty = 1 if 'Double_Check' in p or 'processed' in p.lower() else 0
        has_final   = 2 if 'FINAL' in name and 'with_common' not in name else 0
        has_parens  = -name.count('(')
        return (in_subdir_penalty * -10, has_final, has_parens)

    candidates.sort(key=lambda p: score(p), reverse=True)
    return candidates[0]


# ── Loaders (reused from build_db.py logic) ──────────────────────────────────

def _str(val):
    s = (val or '').strip()
    return s if s else None


def load_samples(conn, batch_id: str):
    f = find_file(batch_id, 'samples')
    if not f:
        print(f'  samples: NOT FOUND')
        return []
    codes = []
    client_id = None
    with open(f, newline='', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            bid  = _str(row.get('BatchId')) or batch_id
            client_id = _str(row.get('ClientId'))
            sid  = _str(row.get('SampleId')) or ''
            if not sid:
                continue
            code = sid + '.1'
            lat_s = _str(row.get('Lat'))
            lon_s = _str(row.get('Long'))
            conn.execute('INSERT OR IGNORE INTO batches VALUES (?,?,?)',
                         (bid, client_id, 'Jonah Ventures'))
            conn.execute('INSERT OR IGNORE INTO samples VALUES (?,?,?,?,?,?,?,?)',
                         (code, bid,
                          _str(row.get('SiteName')),
                          float(lat_s) if lat_s else None,
                          float(lon_s) if lon_s else None,
                          _str(row.get('Capture time (MT)')),
                          _str(row.get('Notes')),
                          None))
            codes.append(code)
    print(f'  samples ({Path(f).name}): {len(codes)} codes')
    return codes


def load_esv_data(conn, batch_id: str, assay: str, prefix: str):
    f = find_file(batch_id, f'{prefix}-esv-data')
    if not f:
        return 0
    n = 0
    with open(f, newline='', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            esv_id    = _str(row.get('ESVId'))
            accession = _str(row.get('Accession'))
            if not esv_id or not accession:
                continue
            pm = row.get('PercMatch','').strip()
            conn.execute('INSERT OR IGNORE INTO esv_matches VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                         (esv_id, assay, accession,
                          _str(row.get('Kingdom')), _str(row.get('Phylum')),
                          _str(row.get('Class')),   _str(row.get('Order')),
                          _str(row.get('Family')),  _str(row.get('Genus')),
                          _str(row.get('Species')),
                          float(pm) if pm else None))
            n += 1
    print(f'  {assay} esv_matches ({Path(f).name}): {n}')
    return n


def load_read_data(conn, batch_id: str, assay: str, prefix: str):
    f = find_file(batch_id, f'{prefix}-read-data')
    if not f:
        print(f'  {assay} read-data: NOT FOUND')
        return 0
    esv_n = read_n = 0
    with open(f, newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        sample_cols = [c for c in (reader.fieldnames or [])
                       if c and c not in FIXED_READ_COLS]
        for row in reader:
            esv_id = _str(row.get('ESVId'))
            if not esv_id:
                continue
            pm = row.get('% match','').strip()
            ns = row.get('# species','').strip()
            conn.execute('INSERT OR IGNORE INTO esvs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         (esv_id, assay,
                          _str(row.get('sequence')),
                          _str(row.get('Kingdom')), _str(row.get('Phylum')),
                          _str(row.get('Class')),   _str(row.get('Order')),
                          _str(row.get('Family')),  _str(row.get('Genus')),
                          _str(row.get('Species')),
                          float(pm) if pm else None,
                          int(ns)   if ns else None,
                          _str(row.get('Common Name'))))
            esv_n += 1
            for col in sample_cols:
                raw = row.get(col,'').strip()
                cnt = int(float(raw)) if raw else 0
                if cnt > 0:
                    conn.execute('INSERT OR REPLACE INTO reads VALUES (?,?,?,?)',
                                 (col, esv_id, assay, cnt))
                    read_n += 1
    print(f'  {assay} ({Path(f).name}): {esv_n} esvs, {read_n} reads')
    return read_n


def load_qpcr(conn, batch_id: str):
    sf = find_file(batch_id, 'qpcr-samples')
    df = find_file(batch_id, 'qpcr-tabulated-data')
    if not df:
        print(f'  qPCR data: NOT FOUND')
        return 0

    # Load samples first
    if sf:
        with open(sf, newline='', encoding='utf-8-sig') as fh:
            for row in csv.DictReader(fh):
                sid = _str(row.get('SampleId')) or ''
                if not sid:
                    continue
                code = sid + '.1'
                lat_s = _str(row.get('Lat'))
                lon_s = _str(row.get('Long'))
                conn.execute('INSERT OR IGNORE INTO batches VALUES (?,?,?)',
                             (batch_id, _str(row.get('ClientId')), 'Jonah Ventures'))
                conn.execute('INSERT OR IGNORE INTO samples VALUES (?,?,?,?,?,?,?,?)',
                             (code, batch_id,
                              _str(row.get('SiteName')),
                              float(lat_s) if lat_s else None,
                              float(lon_s) if lon_s else None,
                              _str(row.get('Capture time (MT)')),
                              _str(row.get('Notes')),
                              None))

    n = 0
    with open(df, newline='', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            sid = _str(row.get('SampleId'))
            if not sid:
                continue
            code  = sid + '.1'
            assay = _str(row.get('Assay'))
            def _f(k): v = row.get(k,'').strip(); return float(v) if v else 0.0
            conn.execute('INSERT OR REPLACE INTO qpcr_results VALUES (?,?,?,?,?,?,?,?)',
                         (code, batch_id, assay,
                          _f('Rep1'), _f('Rep2'), _f('Rep3'),
                          _f('AvgCopyNum'), _f('PctDetection')))
            n += 1
    print(f'  qPCR results ({Path(df).name}): {n} rows')
    return n


def apply_canonical_names(conn):
    """Apply master manifest canonical site names to all samples."""
    import re
    try:
        import pandas as pd
        df = pd.read_excel(MANIFEST_PATH, dtype=str).fillna('')
        pat = re.compile(r'^[A-Z0-9]{8}$')
        updated = 0
        for _, row in df.iterrows():
            status = row.get('Status','').strip()
            if not pat.match(status):
                continue
            site = row.get('Test','').strip()
            if not site or site in ('MiFishU','23S','UniCOI','nan'):
                continue
            cur = conn.execute(
                'UPDATE samples SET canonical_site=? WHERE sample_code=? AND canonical_site IS NULL',
                (site, status+'.1'))
            updated += cur.rowcount
        print(f'  canonical site names applied: {updated} rows')
    except Exception as e:
        print(f'  canonical names skipped: {e}')


# ── Main ─────────────────────────────────────────────────────────────────────

METABARCODING_BATCHES = [
    # (batch_id, has_23S)
    ('JVB3759', True),
    ('JVB3787', True),
    ('JVB3988', True),
    ('JVB4279', False),
    ('JVB4307', True),
    ('JVB4678', True),
    ('JVB4846', False),
    ('JVB4981', False),
    ('JVB5403', True),   # already loaded; INSERT OR IGNORE is safe
    ('JVB5776', True),
]

conn = sqlite3.connect(DB_PATH)

# Add qPCR table
conn.executescript(QPCR_SCHEMA)

# Add common_name column if missing (idempotent)
try:
    conn.execute('ALTER TABLE esvs ADD COLUMN common_name TEXT')
except Exception:
    pass

# Add canonical_site column if missing (idempotent)
try:
    conn.execute('ALTER TABLE samples ADD COLUMN canonical_site TEXT')
except Exception:
    pass

conn.commit()

# Load all metabarcoding batches
for batch_id, has_23s in METABARCODING_BATCHES:
    print(f'\n{batch_id}')
    load_samples(conn, batch_id)
    load_esv_data(conn, batch_id, 'MiFishU', 'MiFishU')
    load_read_data(conn, batch_id, 'MiFishU', 'MiFishU')
    if has_23s:
        load_esv_data(conn, batch_id, '23S', '23S')
        load_read_data(conn, batch_id, '23S', '23S')
    conn.commit()

# Load qPCR
print('\nJVB4683 (qPCR)')
load_qpcr(conn, 'JVB4683')
conn.commit()

# Apply canonical site names from master manifest
print('\nApplying canonical site names...')
apply_canonical_names(conn)
conn.commit()

# Final summary
print('\n=== Database summary ===')
for t in ('batches','samples','esvs','esv_matches','reads','qpcr_results'):
    n = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    print(f'  {t:<15} {n:>8,} rows')

print('\n=== Samples with canonical names ===')
rows = conn.execute('''
    SELECT s.batch_id, s.sample_code,
           COALESCE(s.canonical_site, s.site_name, s.sample_code) AS name
    FROM samples s
    ORDER BY s.batch_id, s.sample_code
''').fetchall()
for batch, code, name in rows:
    print(f'  {batch}  {code}  {name}')

print('\n=== qPCR Brook Trout results ===')
rows = conn.execute('''
    SELECT s.sample_code,
           COALESCE(s.canonical_site, s.site_name) AS site,
           q.avg_copy_num, q.pct_detection
    FROM qpcr_results q
    JOIN samples s ON q.sample_code = s.sample_code
    WHERE q.assay = "BrookTrout01"
    ORDER BY q.avg_copy_num DESC
''').fetchall()
for code, site, copies, pct in rows:
    detected = 'DETECTED' if copies > 0 else 'not detected'
    print(f'  {code}  {site or "":35}  copies={copies:.2f}  {detected}')

conn.close()
size = os.path.getsize(DB_PATH) // 1024
print(f'\nDB: {DB_PATH}  ({size} KB)')
