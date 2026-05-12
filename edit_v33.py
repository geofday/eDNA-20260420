"""
v33 comprehensive edit pass:
1. Add School St Vivosun field measurements (Jul 31 + Nov 23, 2025)
2. Remove surviving deleted "Note: Sawmill Brook..." text
3. Restructure How to Read (fish first, algae second)
4. Fix Brook Trout confirmed sites to include Nov 2025 data
5. Add <!-- PENDING --> markers for footnotes and outstanding items
6. Remove correction-type language
7. Remove lat/lon references
8. Apply remaining GPD editorial insertions
"""

import re, subprocess

SRC = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v32.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v33.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v33.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── 1. Remove the surviving "Note: Sawmill Brook is on the North Shore" deletion ──
text = re.sub(
    r'\*\*Note:\*\* Sawmill Brook is in Manchester-by-the-Sea on the North Shore[^\n]*\n',
    '', text
)
text = re.sub(
    r'> \*\*Note:\*\* Sawmill Brook is in Manchester-by-the-Sea on the North Shore[^\n]*\n',
    '', text
)
# Also the plain text version
text = text.replace(
    '**Note:** Sawmill Brook is in Manchester-by-the-Sea on the North Shore — not Cape Cod. Three sites provide a longitudinal transect: Sawmill Swamp (headwaters, cold groundwater source) → Below School St (mid-reach) → Fire Station (tidal limit).',
    'Three sites provide a longitudinal transect: Sawmill Swamp (headwaters, cold groundwater source) → Below School St (mid-reach) → Fire Station (tidal limit).'
)

# ── 2. Restructure How to Read (fish first, algae second) ─────────────────────
old_how_to = """## How to Read This Report

Algae are the base of the food web. They respond within days to light, temperature, pH, nutrients, and dissolved minerals. Fish integrate conditions over years — they reflect whether the habitat has been livable long enough to support recruitment, growth, and community assembly. Together, algae and fish tell a story neither can tell alone."""

new_how_to = """## How to Read This Report

**Fish eDNA is the center of this report.** Fish integrate conditions over years — their presence or absence at a site reflects whether the habitat has been livable long enough to support recruitment, growth, and community assembly. Brook Trout (*Salvelinus fontinalis*) is the primary sentinel: cold, clean, well-oxygenated water. Where Brook Trout are found, the watershed is working. Where they are absent, the report asks why.

Algal reports deepen this focus and add an additional layer of insight. Key species that mark clean, high-quality water further illustrate Brook Trout-friendly conditions. Algal reports can also shed light when fish DNA is not found — either due to sample failure or low winter fish movements. Algae are the base of the food web, responding within days to light, temperature, pH, and nutrients. Together, fish and algae tell a story neither can tell alone."""

text = text.replace(old_how_to, new_how_to)

# ── 3. Add complexity / Shannon diversity context ────────────────────────────
old_shannon_note = '**Read counts** are proportional, not absolute.'
new_shannon_note = '''**Ecological complexity** is highly favorable to healthy ecosystems. Complex systems are more robust, more durable, more adaptable to environmental change, and more capable of supporting migration and reproduction. Shannon diversity (H) captures this: higher values mean more species contributing meaningfully to the community — not one dominant species and noise.

**Read counts** are proportional, not absolute — they are literal counts of distinct DNA molecules. A species at 1% with 10,000 total reads (100 reads) is more reliable than a species at 1% with 500 total reads (5 reads). <!-- PENDING: Add footnote on read count thresholds and reliability -->'''

text = text.replace(
    '**Read counts** are proportional, not absolute. A species at 1% with 10,000 total reads (100 reads) is more reliable than a species at 1% with 500 total reads (5 reads). Read count footnotes are provided where this distinction matters.',
    new_shannon_note
)

# ── 4. Add School St Vivosun field measurements ───────────────────────────────
# These go into the Aug 2024 Below School St section, which is the most complete
SCHOOL_ST_VIVOSUN = """
### Field Measurements — Below School St / School St Reach (Vivosun pH meter†)

| Date | pH | Temp °F | Note |
|---|---|---|---|
| Jul 31, 2025 | 6.72 | 71.6 | Summer — pH circumneutral; temp at upper Brook Trout stress threshold |
| Nov 23, 2025 | 6.23 | 38.4 | Winter baseline — co-dated with Nov 22, 2025 eDNA event |

pH 6.72 and 71.6°F on July 31 place this site at the edge of Brook Trout thermal comfort: 71.6°F exceeds the sustained-stress threshold (~68°F) and approaches the short-term lethal range (~75°F). Brook Trout detected at this site in November but not confirmed in summer eDNA sampling — the July temperature reading is consistent with seasonal exclusion during peak summer. November pH of 6.23 at 38.4°F is within full Brook Trout tolerance; the November eDNA detection of Brook Trout at 4.8% is consistent with these conditions.

† pH values approximate (±0.5–1.0 pH unit); temperature in °F.

"""

# Insert after the Aug 2024 Below School St narrative section
target = '### Sawmill Brook — Fire Station | JVB3787'
text = text.replace(target, SCHOOL_ST_VIVOSUN + target, 1)

# ── 5. Fix Key Findings — Brook Trout table (add Nov 2025 detection) ─────────
text = text.replace(
    '| **Brook Trout confirmed — 4 sites** | Golf Course (Nov 2023), Below School St (Nov 2023 + Aug 2024), Atwater (Jun 2025), Below Lincoln Pool (Jun 2025) | Persistent multi-site presence across two years |',
    '| **Brook Trout confirmed — 5 events, 4 sites** | Golf Course (Nov 2023), Below School St (Nov 2023, Aug 2024, Nov 2025), Atwater (Jun 2025), Below Lincoln Pool (Jun 2025) | Persistent multi-site presence across two years including spawning season |'
)

# ── 6. Remove "correction-type" language ─────────────────────────────────────
# Per user direction: no "correction" or "corrected" language
text = text.replace('*(corrected — includes all genus-level ESVs; see QC note on cormorant fecal eDNA)*',
                    '*(includes all genus-level ESVs; see cormorant QC note)*')
text = text.replace('Corrected community:', 'Fish community:')
text = text.replace('corrected fish community', 'authenticated fish community')

# ── 7. Remove lat/lon references ─────────────────────────────────────────────
# User: "lat/lon everywhere or nowhere — inaccurate so nowhere"
text = re.sub(r'\([\d°\'"\.]+[NS],?\s*-?[\d°\'"\.]+[EW]\)', '', text)
text = re.sub(r'lat\.?\s*[\d°\'"\.]+,?\s*lon\.?\s*-?[\d°\'"\.]+', '', text)
text = re.sub(r'\d{2}\.\d+°[NS],?\s*-?\d{2,3}\.\d+°[EW]', '', text)

# ── 8. Esox row in Sentinel Species table — fix per ESV finding ───────────────
text = text.replace(
    '| ***Esox* spp.** | Native pickerel likely; Northern Pike possible but unconfirmed | Database anomaly — verify by electrofishing |',
    '| ***Esox* spp.** (*niger*/*americanus*) | Native pickerel — 100% ESV match | Chain Pickerel or Redfin Pickerel; MiFish 12S cannot distinguish the two<!-- PENDING: ESV footnote - ESV_010000 100% native pickerel across all batches; E. lucius assignment is database artifact --> |'
)

# ── 9. Charophyte invasive note ────────────────────────────────────────────────
text = text.replace(
    'The genus was not resolved in the 23S rRNA data, and in-situ verification is required before species identity and invasive status can be confirmed (see note below).',
    'The genus was not resolved in the 23S rRNA data. The top database hit is *Nitellopsis obtusa* (starry stonewort, a regulated invasive), but at 95.8% identity — below the species-level threshold of 97%. The margin over native *Chara*/*Nitella* is only 0.3%. Field verification is required before invasive status can be confirmed. Anecdotal reports from local ecologists and phycologists note that *Nitellopsis obtusa* has not been reported in Massachusetts.<!-- PENDING: Footnote — cite local ecologist/phycologist communications if available -->'
)

# ── 10. Bass/Brook Trout competition ecological note ──────────────────────────
# Add to Cat Brook section
text = text.replace(
    'Cat Brook / Forest Landing occupies one of the two critical chokepoints in the MBTS watershed',
    'Cat Brook is a major tributary to Sawmill Brook. This location marks one of two man-made impoundments bounded by an impassable barrier. Bass and Sunfish are classic indicator species for warm-water habitat: where bass dominate, Brook Trout are rarely found. Bass tolerate higher temperatures and lower dissolved oxygen than salmonids. Cat Brook / Forest Landing occupies one of the two critical chokepoints in the MBTS watershed'
)

# ── 11. Golf Course — sampling purpose note ───────────────────────────────────
text = text.replace(
    '## Lower Golf Course / Sawmill Brook | JVB5776 / C4SUMTFY.1',
    '## Lower Golf Course / Sawmill Brook | JVB5776 / C4SUMTFY.1\n\n*This site was selected to determine whether Brook Trout were accessing the Golf Course reach during fall spawning season (November 2023).*'
)

# ── 12. Rainbow Smelt at Golf Course — "maybe" qualifier ─────────────────────
text = text.replace(
    'Rainbow Smelt (0.2%) and Yellow Perch (1.4%) add coastal connectivity and tolerant generalist presence.',
    'Yellow Perch (1.4%) adds tolerant generalist presence. Rainbow Smelt (0.2%) is an anomalous detection — Rainbow Smelt are not documented in Sawmill Brook or Cat Brook and are not expected in a suburban coastal stream in November; this is best treated as a possible hit, not a confirmed detection.<!-- PENDING: Check ESV for Rainbow Smelt at this site -->'
)

# ── 13. Tidal eDNA degradation note at Below School St ───────────────────────
text = text.replace(
    'Below School St is a functioning tidal transition ecosystem. This is what a healthy coastal tidal reach looks like in late November.',
    'Below School St is a functioning tidal transition ecosystem. Brook Trout consistently detected at this site indicate upstream refugia in the watershed. Note that eDNA degrades more rapidly in tidal/saline water than in freshwater<!-- PENDING: Footnote — cite eDNA degradation study if available -->; the true Brook Trout signal from upstream reaches may be understated at this tidal sampling point. Moving the sampling location further upstream is worth considering.'
)

# ── 14. MBTS intro — remove "ecological recovery" (second instance if any) ───
text = text.replace('tracks ecological recovery of a historically impacted suburban stream',
                    'tracks the health and status of a suburban coastal stream')

# ── 15. Add PENDING markers for missing data / footnotes ──────────────────────
# Vivosun pH data for Golf Course, Cedar Swamp, Fire Station, Second Pond, MBTS #3
for site in ['Lower Golf Course', 'Cedar Swamp', 'Fire Station', 'Second Pond', 'MBTS #3']:
    marker = f'<!-- PENDING: Add Vivosun field pH/temp measurements for {site} when available -->\n\n'
    # Insert before the section heading
    text = text.replace(f'## {site}', marker + f'## {site}', 1)

# ── 16. Write output ──────────────────────────────────────────────────────────
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write(text)

n_lines = text.count('\n')
n_words = len(text.split())
print(f'Written: {OUT_MD}  ({n_lines} lines, {n_words} words)')

result = subprocess.run(
    ['pandoc', OUT_MD, '-o', OUT_DOCX, '--from', 'markdown', '--to', 'docx'],
    capture_output=True, text=True
)
if result.returncode == 0:
    import os
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024}KB)')
else:
    print(f'pandoc error: {result.stderr}')
