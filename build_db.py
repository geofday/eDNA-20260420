"""
build_db.py — Build SQLite eDNA database from JV raw CSV exports.

Schema:
  batches     — one row per JV batch (JVB5403, etc.)
  samples     — one row per sample/site-visit
  esvs        — one row per ESV × assay (sequence + best-match taxonomy)
  esv_matches — all accession-level hits per ESV (the full tie list)
  reads       — one row per sample × ESV × assay, non-zero only (pivoted from wide CSV)

Usage:
  python build_db.py                                     # JVB5403 from default path
  python build_db.py --batch JVB5403 --dir C:/Users/geofd/Downloads/jonahdna
  python build_db.py --batch JVB3988 --dir C:/path/to/JVB3988
  python build_db.py --query ZLQM1TH7.1                 # quick site report, no import
"""

import sqlite3
import csv
import argparse
import os
from pathlib import Path

DB_PATH = r'C:\repos\eDNA-20270420\edna.db'

DEFAULT_BATCH_DIR = r'C:\Users\geofd\Downloads\jonahdna'

SCHEMA = """
CREATE TABLE IF NOT EXISTS batches (
    batch_id   TEXT PRIMARY KEY,
    client_id  TEXT,
    lab        TEXT DEFAULT 'Jonah Ventures'
);

CREATE TABLE IF NOT EXISTS samples (
    sample_code  TEXT PRIMARY KEY,   -- e.g. ZLQM1TH7.1  (.1 = replicate suffix)
    batch_id     TEXT REFERENCES batches(batch_id),
    site_name    TEXT,
    lat          REAL,
    lon          REAL,
    capture_time TEXT,
    notes        TEXT
);

CREATE TABLE IF NOT EXISTS esvs (
    esv_id      TEXT,
    assay       TEXT,        -- 'MiFishU' or '23S'
    sequence    TEXT,
    kingdom     TEXT,
    phylum      TEXT,
    class       TEXT,
    "order"     TEXT,
    family      TEXT,
    genus       TEXT,
    species     TEXT,        -- best/top match species (may be blank = genus-only)
    perc_match  REAL,        -- highest match % for this ESV
    n_species   INTEGER,     -- number of tied top-match species
    PRIMARY KEY (esv_id, assay)
);

CREATE TABLE IF NOT EXISTS esv_matches (
    esv_id      TEXT,
    assay       TEXT,
    accession   TEXT,        -- GenBank accession of the reference sequence
    kingdom     TEXT,
    phylum      TEXT,
    class       TEXT,
    "order"     TEXT,
    family      TEXT,
    genus       TEXT,
    species     TEXT,
    perc_match  REAL,
    PRIMARY KEY (esv_id, assay, accession)
);

CREATE TABLE IF NOT EXISTS reads (
    sample_code  TEXT REFERENCES samples(sample_code),
    esv_id       TEXT,
    assay        TEXT,
    read_count   INTEGER,
    PRIMARY KEY (sample_code, esv_id, assay)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_reads_sample  ON reads(sample_code);
CREATE INDEX IF NOT EXISTS idx_reads_esv     ON reads(esv_id, assay);
CREATE INDEX IF NOT EXISTS idx_esvs_class    ON esvs(class);
CREATE INDEX IF NOT EXISTS idx_esvs_genus    ON esvs(genus);
CREATE INDEX IF NOT EXISTS idx_samples_batch ON samples(batch_id);
"""

FIXED_READ_COLS = {
    'TestId', 'ESVId', 'sequence', 'Kingdom', 'Phylum', 'Class',
    'Order', 'Family', 'Genus', 'Species', '% match', '# species'
}


def _str(val):
    s = (val or '').strip()
    return s if s else None


def load_samples(conn, batch_dir: Path, batch_id: str):
    f = batch_dir / f'{batch_id}-samples.csv'
    if not f.exists():
        print(f'  WARNING: {f} not found')
        return []

    codes = []
    client_id = None
    with open(f, newline='', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            bid      = _str(row.get('BatchId')) or batch_id
            client_id = _str(row.get('ClientId'))
            sid      = _str(row.get('SampleId')) or ''
            code     = sid + '.1'          # JV convention: SampleId + '.1'
            lat_s    = _str(row.get('Lat'))
            lon_s    = _str(row.get('Long'))
            conn.execute(
                'INSERT OR IGNORE INTO samples VALUES (?,?,?,?,?,?,?)',
                (code, bid,
                 _str(row.get('SiteName')),
                 float(lat_s) if lat_s else None,
                 float(lon_s) if lon_s else None,
                 _str(row.get('Capture time (MT)')),
                 _str(row.get('Notes')))
            )
            codes.append(code)

    conn.execute(
        'INSERT OR IGNORE INTO batches VALUES (?,?,?)',
        (batch_id, client_id, 'Jonah Ventures')
    )
    print(f'  samples  : {len(codes)}  {codes}')
    return codes


def load_esv_data(conn, batch_dir: Path, batch_id: str, assay: str, prefix: str):
    f = batch_dir / f'{batch_id}-{prefix}-esv-data.csv'
    if not f.exists():
        print(f'  WARNING: {f} not found')
        return 0

    n = 0
    with open(f, newline='', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            esv_id    = _str(row.get('ESVId'))
            accession = _str(row.get('Accession'))
            if not esv_id or not accession:
                continue
            pm = row.get('PercMatch', '').strip()
            conn.execute(
                'INSERT OR IGNORE INTO esv_matches VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (esv_id, assay, accession,
                 _str(row.get('Kingdom')), _str(row.get('Phylum')),
                 _str(row.get('Class')),   _str(row.get('Order')),
                 _str(row.get('Family')),  _str(row.get('Genus')),
                 _str(row.get('Species')),
                 float(pm) if pm else None)
            )
            n += 1

    print(f'  {assay:<8} esv_matches: {n}')
    return n


def load_read_data(conn, batch_dir: Path, batch_id: str, assay: str, prefix: str):
    f = batch_dir / f'{batch_id}-{prefix}-read-data.csv'
    if not f.exists():
        print(f'  WARNING: {f} not found')
        return 0

    esv_n = read_n = 0
    with open(f, newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        sample_cols = [c for c in reader.fieldnames if c and c not in FIXED_READ_COLS]

        for row in reader:
            esv_id = _str(row.get('ESVId'))
            if not esv_id:
                continue

            pm = row.get('% match', '').strip()
            ns = row.get('# species', '').strip()
            conn.execute(
                'INSERT OR IGNORE INTO esvs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (esv_id, assay,
                 _str(row.get('sequence')),
                 _str(row.get('Kingdom')), _str(row.get('Phylum')),
                 _str(row.get('Class')),   _str(row.get('Order')),
                 _str(row.get('Family')),  _str(row.get('Genus')),
                 _str(row.get('Species')),
                 float(pm) if pm else None,
                 int(ns)   if ns else None)
            )
            esv_n += 1

            for col in sample_cols:
                raw = row.get(col, '').strip()
                cnt = int(raw) if raw else 0
                if cnt > 0:
                    conn.execute(
                        'INSERT OR REPLACE INTO reads VALUES (?,?,?,?)',
                        (col, esv_id, assay, cnt)
                    )
                    read_n += 1

    print(f'  {assay:<8} esvs: {esv_n}  |  reads (non-zero): {read_n}')
    return read_n


def import_batch(conn, batch_id: str, batch_dir_str: str):
    d = Path(batch_dir_str)
    print(f'\nImporting {batch_id} from {d}')
    load_samples(conn, d, batch_id)
    load_esv_data(conn, d, batch_id, 'MiFishU', 'MiFishU')
    load_esv_data(conn, d, batch_id, '23S',     '23S')
    load_read_data(conn, d, batch_id, 'MiFishU', 'MiFishU')
    load_read_data(conn, d, batch_id, '23S',     '23S')
    conn.commit()
    print('  committed.')


def print_summary(conn):
    print('\n── Database totals ──────────────────────────────────────────')
    for t in ('batches', 'samples', 'esvs', 'esv_matches', 'reads'):
        n = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
        print(f'  {t:<15} {n:>7,} rows')


def site_report(conn, sample_code: str):
    print(f'\n── {sample_code} — fish (Actinopteri), all reads ─────────────')
    rows = conn.execute("""
        SELECT e.esv_id, e.genus, e.species, e.perc_match, e.n_species, r.read_count
        FROM reads r
        JOIN esvs e ON r.esv_id = e.esv_id AND r.assay = e.assay
        WHERE r.sample_code = ?
          AND r.assay = 'MiFishU'
          AND e.class = 'Actinopteri'
        ORDER BY r.read_count DESC
    """, (sample_code,)).fetchall()

    total = sum(rc for *_, rc in rows)
    print(f'  {"ESV":<12}  {"Reads":>7}  {"  %fish":>7}  {"Match%":>6}  {"n_spp":>5}  Taxon')
    for esv_id, genus, species, pct, ns, cnt in rows:
        taxon = f'{genus or ""} {species or ""}'.strip()
        pct_fish = 100 * cnt / total if total else 0
        print(f'  {esv_id:<12}  {cnt:>7,}  {pct_fish:>7.1f}%  {pct or 0:>5.1f}%  {ns or 0:>5}  {taxon}')
    print(f'  {"TOTAL":<12}  {total:>7,}')

    print(f'\n── {sample_code} — algae (23S), top 20 ──────────────────────')
    rows = conn.execute("""
        SELECT e.esv_id, e.class, e.genus, e.species, e.perc_match, r.read_count
        FROM reads r
        JOIN esvs e ON r.esv_id = e.esv_id AND r.assay = e.assay
        WHERE r.sample_code = ?
          AND r.assay = '23S'
        ORDER BY r.read_count DESC
        LIMIT 20
    """, (sample_code,)).fetchall()

    total_a = conn.execute(
        "SELECT SUM(read_count) FROM reads WHERE sample_code=? AND assay='23S'",
        (sample_code,)
    ).fetchone()[0] or 0

    print(f'  {"ESV":<12}  {"Reads":>7}  {" %algae":>7}  {"Match%":>6}  Class / Taxon')
    for esv_id, cls, genus, species, pct, cnt in rows:
        taxon = f'{genus or ""} {species or ""}'.strip()
        pct_a = 100 * cnt / total_a if total_a else 0
        print(f'  {esv_id:<12}  {cnt:>7,}  {pct_a:>7.1f}%  {pct or 0:>5.1f}%  {cls or ""}  {taxon}')
    print(f'  Total algae reads at this site: {total_a:,}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', default='JVB5403')
    ap.add_argument('--dir',   default=DEFAULT_BATCH_DIR)
    ap.add_argument('--db',    default=DB_PATH)
    ap.add_argument('--query', default=None,
                    help='Sample code to report (skip import, just query)')
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.executescript(SCHEMA)
    conn.commit()

    if not args.query:
        import_batch(conn, args.batch, args.dir)

    print_summary(conn)
    site_report(conn, args.query or 'ZLQM1TH7.1')

    conn.close()
    size = os.path.getsize(args.db) // 1024
    print(f'\nDB: {args.db}  ({size} KB)\n')


if __name__ == '__main__':
    main()
