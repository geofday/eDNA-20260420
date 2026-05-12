"""
enrich_common_names.py — Load common names from any JVB read-data CSV that has
a 'Common Name' column and update the esvs table in edna.db.

ESV IDs are consistent across batches, so common names loaded from any batch
apply everywhere in the database.

Usage:
  python enrich_common_names.py                  # scans default sources
  python enrich_common_names.py --db edna.db     # alternate db path
"""

import sqlite3
import csv
import argparse
from pathlib import Path

DB_PATH = r'C:\repos\eDNA-20270420\edna.db'

# CSVs known to have a 'Common Name' column — add more as found
SOURCES = [
    r'F:\RESCUE_USERS\geofd\Downloads\JVB4678-MiFishU-read-data_with_common.csv',
    r'F:\RESCUE_USERS\geofd\Downloads\JVB4678-MiFishU-read-data_FINAL_with_family.csv',
]


def load_common_names(path: str) -> dict:
    """Return {esv_id: common_name} from a CSV that has a 'Common Name' column."""
    names = {}
    p = Path(path)
    if not p.exists():
        print(f'  SKIP (not found): {path}')
        return names

    with open(p, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if 'Common Name' not in (reader.fieldnames or []):
            print(f'  SKIP (no Common Name column): {p.name}')
            return names

        for row in reader:
            esv_id = (row.get('ESVId') or '').strip()
            name   = (row.get('Common Name') or '').strip()
            if esv_id and name:
                names[esv_id] = name

    print(f'  {p.name}: {len(names)} common names found')
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', default=DB_PATH)
    args = ap.parse_args()

    # Merge all sources — later sources win on conflict
    all_names = {}
    print('Reading common name sources:')
    for src in SOURCES:
        all_names.update(load_common_names(src))

    print(f'\nTotal unique ESV common name mappings: {len(all_names)}')

    conn = sqlite3.connect(args.db)

    # Ensure column exists (idempotent)
    try:
        conn.execute('ALTER TABLE esvs ADD COLUMN common_name TEXT')
    except Exception:
        pass  # column already exists

    updated = 0
    for esv_id, name in all_names.items():
        cur = conn.execute(
            'UPDATE esvs SET common_name = ? WHERE esv_id = ? AND common_name IS NULL',
            (name, esv_id)
        )
        updated += cur.rowcount

    conn.commit()
    conn.close()

    print(f'Updated {updated} rows in esvs table.')

    # Quick preview
    conn = sqlite3.connect(args.db)
    print('\nSample — esvs with common names now set:')
    rows = conn.execute(
        "SELECT esv_id, genus, species, common_name FROM esvs "
        "WHERE common_name IS NOT NULL LIMIT 15"
    ).fetchall()
    for esv_id, genus, species, cn in rows:
        print(f'  {esv_id}  {genus or ""} {species or "":30}  {cn}')
    conn.close()


if __name__ == '__main__':
    main()
