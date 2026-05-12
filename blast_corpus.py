"""
blast_corpus.py — BLAST the full remaining corpus of ecologically interesting ESVs.

Targets (in priority order):
  1. ALL vertebrate non-fish ESVs: Mammalia, Aves, Amphibia, Hyperoartia
  2. Top 30 unresolved 23S (NULL class or NULL genus, highest reads)
  3. Top 20 genus-only or multi-species Actinopteri fish ESVs

Skips PositiveControl and ESVs already blasted.
Results written to esvs.blast_genus / blast_species / blast_pct / blast_notes.
Script is safe to interrupt and resume — only unblasted ESVs are queried.
"""

import sqlite3, time, sys
from Bio.Blast import NCBIWWW, NCBIXML

DB_PATH = r'C:\repos\eDNA-20270420\edna.db'

# NCBI entrez filter per class — narrows search for speed and accuracy
ENTREZ = {
    'Mammalia':   'Mammalia[Organism]',
    'Aves':       'Aves[Organism]',
    'Amphibia':   'Amphibia[Organism]',
    'Hyperoartia':'Petromyzontiformes[Organism]',
    'Actinopteri':'Actinopterygii[Organism]',
    None:         '',   # fully unresolved 23S — no filter
}

conn = sqlite3.connect(DB_PATH)

# ── 1. Pre-mark known artifacts (no BLAST needed) ───────────────────────────
# Struthio camelus in Aves = ostrich PositiveControl bleed
n = conn.execute("""
    UPDATE esvs SET blast_genus='Struthio', blast_species='Struthio camelus',
                    blast_pct=NULL, blast_notes='JV PositiveControl artifact (ostrich DNA)'
    WHERE genus='Struthio' AND species='Struthio camelus'
      AND blast_genus IS NULL
""").rowcount
if n: print(f'Pre-marked {n} Struthio (PositiveControl) ESVs — no BLAST needed')

# Homo sapiens = human field contamination
n = conn.execute("""
    UPDATE esvs SET blast_genus='Homo', blast_species='Homo sapiens',
                    blast_pct=NULL, blast_notes='Human field contamination'
    WHERE genus='Homo' AND species='Homo sapiens'
      AND blast_genus IS NULL
""").rowcount
if n: print(f'Pre-marked {n} Homo sapiens (human contamination) ESVs — no BLAST needed')

conn.commit()

# ── 2. Build target list ─────────────────────────────────────────────────────

def fetch_targets(sql):
    return conn.execute(sql).fetchall()

# All non-fish vertebrates (unblasted)
vert_rows = fetch_targets("""
    SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
           (SELECT SUM(r2.read_count) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
           (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
    FROM esvs e
    WHERE e.class IN ('Mammalia','Aves','Amphibia','Hyperoartia')
      AND e.blast_genus IS NULL
      AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
    ORDER BY total_reads DESC
""")

# Top 30 unresolved 23S (NULL class or NULL genus, highest reads)
algae_rows = fetch_targets("""
    SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
           (SELECT SUM(r2.read_count) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
           (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
    FROM esvs e
    WHERE e.assay='23S'
      AND e.blast_genus IS NULL
      AND (e.class IS NULL OR e.genus IS NULL)
      AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
    ORDER BY total_reads DESC
    LIMIT 30
""")

# Top 20 genus-only or multi-species Actinopteri
fish_rows = fetch_targets("""
    SELECT DISTINCT e.esv_id, e.assay, e.class, e.genus, e.species, e.sequence,
           (SELECT SUM(r2.read_count) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as total_reads,
           (SELECT COUNT(DISTINCT r2.sample_code) FROM reads r2
            WHERE r2.esv_id=e.esv_id AND r2.assay=e.assay) as n_sites
    FROM esvs e
    WHERE e.class='Actinopteri'
      AND e.blast_genus IS NULL
      AND (e.species IS NULL OR e.n_species IS NULL OR e.n_species > 1)
      AND e.sequence IS NOT NULL AND LENGTH(e.sequence) > 50
    ORDER BY total_reads DESC
    LIMIT 20
""")

all_targets = (
    [('VERTEBRATE', r) for r in vert_rows] +
    [('23S',        r) for r in algae_rows] +
    [('FISH',       r) for r in fish_rows]
)

print(f'\nTargets: {len(vert_rows)} vertebrates + {len(algae_rows)} algae + {len(fish_rows)} fish = {len(all_targets)} total')
print('(~30-90s per query — estimated runtime 2-4 hours)\n')

# ── 3. BLAST loop ────────────────────────────────────────────────────────────

results = []

for idx, (group, row) in enumerate(all_targets):
    esv_id, assay, cls, genus, species, seq, reads, n_sites = row
    reads = reads or 0

    label = f'[{idx+1}/{len(all_targets)}] {group}'
    jv_id = f'{genus or "?"} {species or "?"}'.strip()
    sys.stdout.write(f'{label}  {esv_id}  {reads:,}r  {n_sites}s  JV={jv_id[:35]}  ... ')
    sys.stdout.flush()

    entrez_q = ENTREZ.get(cls, '')

    try:
        handle = NCBIWWW.qblast(
            program='blastn',
            database='nt',
            sequence=seq,
            entrez_query=entrez_q,
            hitlist_size=5,
            expect=1e-10,
            word_size=11,
        )
        blast_record = NCBIXML.read(handle)

        best_genus = best_species = best_pct = best_title = None
        if blast_record.alignments:
            aln = blast_record.alignments[0]
            hsp = aln.hsps[0]
            best_pct   = round(100 * hsp.identities / hsp.align_length, 1)
            best_title = aln.title[:200]

            # Parse genus/species from NCBI title
            # Titles look like: "gi|xxx|...|... Genus species strain ..."
            import re
            m = re.search(r'\s([A-Z][a-z]+)\s+([a-z]+(?:\s+[a-z]+)?)', aln.title)
            if m:
                best_genus   = m.group(1)
                best_species = m.group(1) + ' ' + m.group(2)

        # Flag JV/BLAST disagreements
        notes = ''
        if genus and best_genus and genus != best_genus:
            notes = f'JV={genus}, BLAST={best_genus} — MISMATCH'
        elif genus and best_genus:
            notes = 'confirmed'
        elif best_genus:
            notes = 'newly resolved'
        else:
            notes = 'no hit'

        conn.execute("""
            UPDATE esvs SET blast_genus=?, blast_species=?, blast_pct=?, blast_notes=?
            WHERE esv_id=? AND assay=?
        """, (best_genus, best_species, best_pct, notes, esv_id, assay))
        conn.commit()

        results.append({
            'group': group, 'esv_id': esv_id, 'cls': cls or '?',
            'jv': jv_id, 'reads': reads, 'sites': n_sites,
            'blast': best_species or '(no hit)', 'pct': best_pct,
            'title': best_title, 'notes': notes,
        })

        if best_genus:
            mismatch = ' *** MISMATCH' if 'MISMATCH' in notes else ''
            print(f'{best_pct:.1f}%  {best_species}{mismatch}')
        else:
            print('no hit')

    except Exception as e:
        msg = str(e)
        print(f'ERROR: {msg[:80]}')
        conn.execute("""
            UPDATE esvs SET blast_notes=? WHERE esv_id=? AND assay=?
        """, (f'BLAST error: {msg[:200]}', esv_id, assay))
        conn.commit()
        results.append({'group': group, 'esv_id': esv_id, 'jv': jv_id,
                        'reads': reads, 'error': msg})

    time.sleep(5)

# ── 4. Final report ──────────────────────────────────────────────────────────

print('\n' + '='*80)
print('BLAST CORPUS RESULTS')
print('='*80)

# Group by outcome
confirmed  = [r for r in results if 'error' not in r and r.get('notes') == 'confirmed']
mismatches = [r for r in results if 'MISMATCH' in r.get('notes', '')]
resolved   = [r for r in results if 'error' not in r and r.get('notes') == 'newly resolved']
no_hits    = [r for r in results if 'error' not in r and r.get('blast') == '(no hit)']
errors     = [r for r in results if 'error' in r]

print(f'\nConfirmed (JV=BLAST):  {len(confirmed)}')
print(f'Mismatches:            {len(mismatches)}')
print(f'Newly resolved:        {len(resolved)}')
print(f'No hits:               {len(no_hits)}')
print(f'Errors:                {len(errors)}')

if mismatches:
    print('\n*** MISMATCHES — JV identification vs BLAST differ ***')
    for r in mismatches:
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['sites']}s  {r['notes']}")
        print(f"    BLAST: {r['pct']}%  {r['blast']}")

if resolved:
    print('\n--- Newly resolved (no JV species) ---')
    for r in resolved:
        print(f"  {r['esv_id']:12}  {r['reads']:>8,}r  {r['sites']}s  cls={r['cls']:20}  BLAST: {r['pct']}%  {r['blast']}")

print('\n--- All results ---')
for r in [x for x in results if 'error' not in x]:
    print(f"  [{r['group']:10}]  {r['esv_id']:12}  {r['reads']:>8,}r  JV={r['jv'][:30]:30}  BLAST={r['pct'] or '?'}%  {r['blast'][:50]}")

conn.close()
print('\nDone.')
