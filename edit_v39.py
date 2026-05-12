"""
v39 — Apply tracked changes from Narraguagus_Deblois_eDNA_v7.docx (Geoffrey Day edits).

Changes applied:
- Shannon Diversity paragraph: replaced with formal definition + qualifying sentence
- Read counts paragraph: deleted (REMOVE PARAGRAPH)
- Section heading: "Narraguagus Watershed" → "Narraguagus Watershed — Overview"
- Introduction: add BT/salmon summary sentence; simplify "all five sites" sentence
- Status header: simplified to "Brook Trout status: Detected. Atlantic Salmon status: Detected."
- Site sections reordered to match summary table: Rt 193, West Branch, Crotch Camp, UNT, McCoy
- "Brook Trout: Present/Absent" labels added to all site headers
- McCoy Brook: add Note paragraph on extreme pH; soften Worcester Peat attribution to "presumably"
- Crotch Camp: "Trout sp." → "Brook Trout"; Salvelinus disambiguation moved to footnote
- West Branch: "Trout sp." → "Brook Trout" in sentinel and narrative
- Maine Summary table: "Trout sp." → "Brook Trout"
"""

import subprocess, os

SRC    = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v7.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v9.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v9.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── 1. Shannon Diversity paragraph ────────────────────────────────────────────
text = text.replace(
    '**Shannon Diversity** is used throughout: **H(f)** for fish, **H(a)** for algae. '
    'The formula −Σ p·ln p sums, for each species, its proportional abundance (p) '
    'multiplied by its natural log — so a community with many species each contributing '
    'similar read counts scores higher than one dominated by a single species. A higher '
    'value means more even distribution of reads across species — a proxy for ecological '
    'complexity and environmental quality.',

    '**Shannon diversity** was calculated separately for fish communities, **H(f)**, and '
    'algal communities, **H(a)**, using the Shannon index: H = −Σ pᵢ ln(pᵢ), where pᵢ is '
    'the proportion of total accepted reads assigned to taxon i within a sample. The index '
    'increases when more taxa are detected and when read counts are more evenly distributed '
    'among taxa. In this eDNA context, Shannon diversity should be interpreted as a '
    'standardized measure of detected community diversity based on relative read '
    'representation, not as a direct census of organism abundance. Higher values may '
    'indicate a more diverse and evenly represented biological signal, but interpretation '
    'as environmental quality requires comparison among sites, seasons, controls, and '
    'supporting ecological evidence. Shannon diversity is a widely used community-diversity '
    'metric that can support ecological interpretation when compared across samples and '
    'paired with other evidence.'
)

# ── 2. Remove Read counts paragraph ──────────────────────────────────────────
text = text.replace(
    '\n**Read counts** are proportional, not absolute — they are literal counts of '
    'distinct DNA molecules in the sample. A species at 1% with 10,000 total reads '
    '(100 reads) is more reliable than a species at 1% with 500 total reads (5 reads).\n',
    '\n'
)

# ── 3. Section heading ────────────────────────────────────────────────────────
text = text.replace(
    '# 1. Maine — Narraguagus Watershed\n',
    '# 1. Maine — Narraguagus Watershed — Overview\n'
)

# ── 4. Introduction paragraph ─────────────────────────────────────────────────
text = text.replace(
    'it supports wild Brook Trout in its cold headwater tributaries. '
    'All five sites carry both fish (MiFish 12S) and algal (23S rRNA) data — '
    'the most complete ecological dataset in the study.',

    'it supports wild Brook Trout in its cold headwater tributaries. '
    'Here, two out of five locations have brook trout DNA and salmon DNA is found '
    'in one location. All five sites are analyzed using both fish (MiFish 12S) and '
    'algal (23S rRNA).'
)

# ── 5. Status header ──────────────────────────────────────────────────────────
text = text.replace(
    '**Brook Trout status: Detected (Crotch Camp Brook, West Branch Narraguagus).** '
    '**Atlantic Salmon status: Detected (Narraguagus Rt 193, 110 reads, 100% match — '
    'Gulf of Maine DPS, federally endangered).**',

    '**Brook Trout status: Detected. Atlantic Salmon status: Detected.**'
)

# ── 6. Crotch Camp — "Trout sp." → "Brook Trout" ────────────────────────────
text = text.replace(
    'Synura at 74% dominance + Trout sp. present = **phosphorus-limited',
    'Synura at 74% dominance + Brook Trout present = **phosphorus-limited'
)
text = text.replace(
    'Creek Chub (25.0%), Trout sp. (16.9%), Redbreast Sunfish',
    'Creek Chub (25.0%), Brook Trout (16.9%), Redbreast Sunfish'
)
text = text.replace(
    'The Trout sp. signal reflects *Salvelinus* spp. at 100% match — the MiFish 12S '
    'locus does not distinguish Brook Trout (*S. fontinalis*) from Lake Trout '
    '(*S. namaycush*) or Arctic Char (*S. alpinus*) at this resolution. Geographic '
    'context — small, cold, phosphorus-limited headwater tributary in Washington County, '
    'Maine — strongly supports Brook Trout. Lake Trout prefer deep lakes; Arctic Char '
    'is documented in only a handful of Maine coldwater ponds. Reported throughout as Trout sp.',

    'Brook Trout eDNA confirmed (*Salvelinus* spp., 100% match).'
    '^[MiFish 12S cannot distinguish Brook Trout (*S. fontinalis*), Lake Trout '
    '(*S. namaycush*), or Arctic Char (*S. alpinus*) at this locus. Geographic context '
    '— small, cold, phosphorus-limited headwater tributary in Washington County, ME — '
    'strongly favors Brook Trout. Lake Trout prefer deep lakes; Arctic Char is documented '
    'in only a handful of Maine coldwater ponds.]'
)

# ── 7. West Branch — "Trout sp." → "Brook Trout" ────────────────────────────
text = text.replace(
    'Finescale Dace + Trout sp. + Sea Lamprey + diverse diatom matrix',
    'Finescale Dace + Brook Trout + Sea Lamprey + diverse diatom matrix'
)
text = text.replace(
    'Sea Lamprey (0.3%) and Trout sp. (1.9%) confirm the site has ecological connectivity',
    'Sea Lamprey (0.3%) and Brook Trout (1.9%) confirm the site has ecological connectivity'
)

# ── 8. Maine Summary table ────────────────────────────────────────────────────
text = text.replace(
    '| Crotch Camp Brook | 9 | 1.69 | 76 | 2.30 | Synura 74% + Trout sp. |',
    '| Crotch Camp Brook | 9 | 1.69 | 76 | 2.30 | Synura 74% + Brook Trout |'
)

# ── 9. Worcester Peat — soften attribution ────────────────────────────────────
text = text.replace(
    '**The source of impairment at McCoy Brook is identified: Worcester Peat Mining.**',
    '**The source of impairment at McCoy Brook is presumably the Worcester Peat Mine operation.**'
)
text = text.replace(
    'has been operating for well over a decade and is the primary anthropogenic driver',
    'has been operating for well over a decade and is presumably the primary anthropogenic driver'
)

# ── 10. Reorder site sections + add BT labels ─────────────────────────────────
# Extract the five site section blocks from the text.
# Each site section is delimited by "\n---\n\n## " at the start and ends at the
# next "\n\n---\n" (which precedes either the next site or the Maine Summary).

import re

# Marker strings unique to the start of each section header
SITE_MARKERS = {
    'mccoy':   '## McCoy Brook | CSWEE3DX.1',
    'crotch':  '## Crotch Camp Brook | CNTLVPX4.1',
    'unt':     '## UNT Lane Rd | CNR7WZYJ.1',
    'west':    '## West Branch Narraguagus River @ Sprague\'s Falls | CY92PPTX.1',
    'rt193':   '## Narraguagus Rt 193 | CA66THTZ.1',
    'summary': '## Maine Summary',
}

# Split the document at the first site section
split_at = '\n---\n\n' + SITE_MARKERS['mccoy']
preamble, rest = text.split(split_at, 1)

# Now split rest into individual site blocks + summary/table tail
# Reassemble rest with the leading '## McCoy Brook...' marker
rest = SITE_MARKERS['mccoy'] + rest

# Use regex to split on section boundaries
section_pattern = re.compile(
    r'\n---\n\n(?=## (?:McCoy Brook|Crotch Camp Brook|UNT Lane Rd|West Branch Narraguagus|Narraguagus Rt 193|Maine Summary|Detailed Species))'
)
parts = section_pattern.split(rest)
# parts[0] = first site section text (starts with "## McCoy Brook...")
# remaining parts = subsequent sections

# Build a dict of site key → section text
sections = {}
tail_parts = []  # summary and table go to tail

for part in parts:
    if part.startswith(SITE_MARKERS['mccoy']):
        sections['mccoy'] = part.rstrip('\n')
    elif part.startswith(SITE_MARKERS['crotch']):
        sections['crotch'] = part.rstrip('\n')
    elif part.startswith(SITE_MARKERS['unt']):
        sections['unt'] = part.rstrip('\n')
    elif part.startswith(SITE_MARKERS['west']):
        sections['west'] = part.rstrip('\n')
    elif part.startswith(SITE_MARKERS['rt193']):
        sections['rt193'] = part.rstrip('\n')
    else:
        tail_parts.append(part.rstrip('\n'))

# Add BT labels to each section's stats header
def add_bt_label(section_text, label):
    """Insert 'Brook Trout: Present/Absent' after the bold stats line."""
    # The stats line starts with **Fish: and ends with **
    lines = section_text.split('\n')
    result = []
    inserted = False
    for i, line in enumerate(lines):
        result.append(line)
        if not inserted and line.startswith('**Fish:') and line.endswith('**'):
            result.append('')
            result.append(f'**Brook Trout: {label}**')
            inserted = True
    return '\n'.join(result)

sections['mccoy']  = add_bt_label(sections['mccoy'],  'Absent')
sections['crotch'] = add_bt_label(sections['crotch'], 'Present')
sections['unt']    = add_bt_label(sections['unt'],     'Absent')
sections['west']   = add_bt_label(sections['west'],    'Present')
sections['rt193']  = add_bt_label(sections['rt193'],   'Absent')

# Add McCoy Brook note paragraph (after BT label, before Sentinel Signal)
# Insert after the "Brook Trout: Absent" line
mccoy = sections['mccoy']
mccoy = mccoy.replace(
    '**Brook Trout: Absent**\n\n### Sentinel Signal',
    '**Brook Trout: Absent**\n\n'
    '**Note:** pH 3.54 is the most acidic sample in this study — it may also be among '
    'the most acidic waters in the state.\n\n'
    '### Sentinel Signal'
)
sections['mccoy'] = mccoy

# Reassemble in new order: Rt 193, West Branch, Crotch Camp, UNT, McCoy
ORDER = ['rt193', 'west', 'crotch', 'unt', 'mccoy']
site_block = '\n\n---\n\n'.join(sections[k] for k in ORDER)

tail = '\n\n---\n\n'.join(tail_parts)

new_text = preamble + '\n---\n\n' + site_block + '\n\n---\n\n' + tail

# ── Write output ──────────────────────────────────────────────────────────────
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write(new_text)

n_lines = new_text.count('\n')
n_words = len(new_text.split())
print(f'Written: {OUT_MD}  ({n_lines} lines, {n_words} words)')

result = subprocess.run(
    ['pandoc', OUT_MD, '-o', OUT_DOCX, '--from', 'markdown', '--to', 'docx'],
    capture_output=True, text=True
)
if result.returncode == 0:
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024} KB)')
else:
    print(f'pandoc error: {result.stderr}')
