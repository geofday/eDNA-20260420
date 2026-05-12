"""
enrich_site_names.py — Load canonical site names from the JV master manifest XLSX
and update the samples table in edna.db.

The manifest maps sample codes (8-char alphanum, e.g. ZVYQK9TP) to real place
names (e.g. "Lower Rd. Brewster MA"). This is the single source of truth for
site identity across all batches.

Usage:
  python enrich_site_names.py
"""

import sqlite3
import re
import pandas as pd
from pathlib import Path

DB_PATH       = r'C:\repos\eDNA-20270420\edna.db'
MANIFEST_PATH = r'C:\Users\geofd\OneDrive\LOCAL - NON - Onedrive - Storage - 2024\JV_MASTER_BEST_20260413 (version 2).xlsx'

SAMPLE_CODE_RE = re.compile(r'^[A-Z0-9]{8}$')


def extract_site_names(xlsx_path: str) -> dict:
    """
    Parse the master manifest and return {sample_code_with_.1: canonical_site_name}.
    Sample rows are identified by Status matching the 8-char alphanumeric pattern.
    """
    df = pd.read_excel(xlsx_path, dtype=str)
    df = df.fillna('')

    mapping = {}
    for _, row in df.iterrows():
        status = row.get('Status', '').strip()
        if not SAMPLE_CODE_RE.match(status):
            continue                          # batch-level row or header, skip

        site_name = row.get('Test', '').strip()
        if not site_name or site_name in ('MiFishU', '23S', 'UniCOI', 'nan'):
            continue

        sample_code = status + '.1'
        mapping[sample_code] = site_name

    return mapping


def main():
    mapping = extract_site_names(MANIFEST_PATH)
    print(f'Site name mappings found in manifest: {len(mapping)}')
    for code, name in sorted(mapping.items()):
        print(f'  {code}  ->  {name}')

    conn = sqlite3.connect(DB_PATH)

    # Ensure column exists
    try:
        conn.execute('ALTER TABLE samples ADD COLUMN canonical_site TEXT')
    except Exception:
        pass

    updated = skipped = 0
    for sample_code, site_name in mapping.items():
        cur = conn.execute(
            'UPDATE samples SET canonical_site = ? WHERE sample_code = ?',
            (site_name, sample_code)
        )
        if cur.rowcount:
            updated += cur.rowcount
        else:
            skipped += 1   # sample not yet in DB — will apply when batch is loaded

    conn.commit()

    print(f'\nUpdated {updated} sample rows in DB.')
    print(f'{skipped} mappings have no matching sample yet (will apply when batch is imported).')

    print('\nSamples table now:')
    rows = conn.execute(
        'SELECT sample_code, batch_id, site_name, canonical_site FROM samples ORDER BY batch_id, sample_code'
    ).fetchall()
    for code, batch, jv_name, canon in rows:
        print(f'  {batch}  {code}  JV: "{jv_name or ""}"  ->  Canon: "{canon or ""}"')

    conn.close()


if __name__ == '__main__':
    main()
