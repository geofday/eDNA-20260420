"""
Apply all GPD edits from the v31 reviewed docx to produce v32.

Changes applied:
1. Remove all Fresh Brook content (3 sections)
2. Remove Appendix B (Non-Aquatic)
3. Remove Maine-only algal summaries (JVB5403, JVB3988+JVB4678)
4. Change all Celsius to Fahrenheit throughout
5. Remove Esox row from Key Findings table
6. Fix About intro (remove Fresh Brook refs, fix count, remove 'recovery')
7. Fix site order sentence
8. Add Methods paragraph
9. Remove Temp °C column from field measurement tables
"""

import re, subprocess

SRC = r'C:\repos\eDNA-20270420\output\Sawmill_CatBrook_eDNA_Report_v1.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v32.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v32.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── 1. About This Report ──────────────────────────────────────────────────────

# Remove Fresh Brook sentence from About
text = text.replace(
    'Three Fresh Brook samples (a tributary flowing separately to Manchester Harbor) are included.',
    ''
)

# Fix sample count and date range in About (remove specific numbers that are now wrong)
text = text.replace(
    'This report covers **17 water samples** across 12 distinct sites in and around the Sawmill Brook / Cat Brook watershed in Manchester-by-the-Sea, MA, spanning November 2023 through June 2025. It also includes one marine sample at Proctor Point Dock (Manchester Harbor, June 2025), which provides ecological context for the watershed\'s coastal outlet.',
    'This report covers water samples from 12 distinct sites in and around the Sawmill Brook / Cat Brook watershed in Manchester-by-the-Sea, MA, spanning November 2023 through November 2025. It also includes one marine sample at Proctor Point Dock (Manchester Harbor, June 2025), which provides ecological context for the watershed\'s coastal outlet.'
)

# Remove "recovery" from "tracks ecological recovery of Sawmill Brook"
text = text.replace(
    'tracks ecological recovery of Sawmill Brook',
    'tracks the health and status of Sawmill Brook'
)

# Remove Esox from species list in Brook Trout paragraph
text = text.replace(
    'from Golden Shiner to Mummichog to *Esox* spp. —',
    'from Golden Shiner to Mummichog —'
)

# ── 2. Key Findings Table ─────────────────────────────────────────────────────

# Remove Esox row
text = text.replace(
    '| ***Esox* spp. (db: *Esox lucius*) detected** | Second Pond (Oct 2024) | Likely native pickerel (Chain or Redfin); Northern Pike assignment anomalous — verify by electrofishing before acting |\n',
    ''
)

# ── 3. Site order sentence ────────────────────────────────────────────────────

text = text.replace(
    '**Site order:** Sites are presented upstream-to-downstream where possible, followed by Fresh Brook, then Proctor Point marine reference.',
    '**Site order:** Sites are presented upstream-to-downstream where possible, followed by Proctor Point marine reference.'
)

# ── 4. Add Methods paragraph after site order ─────────────────────────────────

METHODS = """
**Methods:** All samples were collected using Jonah Ventures (JV) eDNA field kits following field-sterile procedures. All samples were mailed to JV for processing. Most samples were analyzed using the MiFish 12S rRNA barcode (fish); several were also analyzed for algae using the 23S rRNA barcode. Results were processed in MS Excel and later using Artificial Intelligence (Claude / OpenAI).

"""

text = text.replace(
    '**Site order:** Sites are presented upstream-to-downstream where possible, followed by Proctor Point marine reference.\n\n---',
    '**Site order:** Sites are presented upstream-to-downstream where possible, followed by Proctor Point marine reference.\n' + METHODS + '---'
)

# ── 5. Celsius → Fahrenheit in narrative text ─────────────────────────────────

# Inline °C conversions (narrative, not tables)
c_to_f = {
    '8°C': '46°F',
    '13.0°C': '55.4°F',
    '12–16°C': '54–61°F',
    '12–14°C': '54–57°F',
    '23–24°C': '73–75°F',
    '24.4°C': '75.9°F',
    '23°C': '73°F',
    '24°C': '75°F',
    '20.3°C': '68.5°F',
    '23.9°C': '75.0°F',
    '17.1°C': '62.7°F',
    '2.7°C': '37°F',
    '3.2°C': '38°F',
}
for c, f in c_to_f.items():
    text = text.replace(c, f)

# ── 6. Remove Temp °C column from field measurement tables ───────────────────
# Pattern: table rows with 5 columns where col 4 is the °C value (already shown as °F in col 3)

# Below Lincoln Pool table header and rows
text = text.replace(
    '| Date | pH | Temp °F | Temp °C | Note |\n|---|---|---|---|---|\n| Jun 5, 2025 | 6.50 | 55.4 | 13.0 | Co-collected with eDNA sample |\n| Nov 23, 2025 | 6.07 | 37.7 | 3.2 | Winter baseline |',
    '| Date | pH | Temp °F | Note |\n|---|---|---|---|\n| Jun 5, 2025 | 6.50 | 55.4 | Co-collected with eDNA sample |\n| Nov 23, 2025 | 6.07 | 37.7 | Winter baseline |'
)

# Atwater Site table header and rows
text = text.replace(
    '| Date | pH | Temp °F | Temp °C | Note |\n|---|---|---|---|---|\n| Jun 8, 2025 | 5.60 | 62.7 | 17.1 | Co-collected with eDNA sample |\n| Jul 9, 2025 | 6.00 | 75.9 | **24.4** | ⚠️ **Acute thermal stress / lethal for Brook Trout** |\n| Nov 23, 2025 | 6.49 | 36.8 | 2.7 | Winter baseline |',
    '| Date | pH | Temp °F | Note |\n|---|---|---|---|\n| Jun 8, 2025 | 5.60 | 62.7 | Co-collected with eDNA sample |\n| Jul 9, 2025 | 6.00 | 75.9 | ⚠️ **Acute thermal stress / lethal for Brook Trout** |\n| Nov 23, 2025 | 6.49 | 36.8 | Winter baseline |'
)

# Fix narrative references that still say °C after table removal
text = text.replace(
    'At 75.9°F (24.4°C), Atwater Ave water temperature is at or beyond the acute lethal threshold for Brook Trout (death commonly reported above 23–24°C).',
    'At 75.9°F, Atwater Ave water temperature is at or beyond the acute lethal threshold for Brook Trout (death commonly reported above 73–75°F).'
)

# ── 7. Remove Fresh Brook sections ────────────────────────────────────────────
# Find the separator before Fresh Brook Route 6 and cut through end of Raccoon section
# Fresh Brook Route 6 starts: "## Fresh Brook, Route 6"
# Proctor Point starts: "## Proctor Point Dock"

fb_start = text.find('\n## Fresh Brook, Route 6')
pp_start = text.find('\n## Proctor Point Dock')

if fb_start != -1 and pp_start != -1:
    # Also remove the preceding --- separator
    sep_start = text.rfind('\n---\n', 0, fb_start)
    text = text[:sep_start] + '\n\n---\n\n' + text[pp_start+1:]
    print(f'Removed Fresh Brook sections ({pp_start - fb_start} chars)')
else:
    print(f'WARNING: Fresh Brook markers not found: fb={fb_start}, pp={pp_start}')

# ── 8. Remove Appendix B ──────────────────────────────────────────────────────
app_b_start = text.find('\n# Appendix B')
nov_section = text.find('\n## November 22, 2025 Sampling Batch')
jvb5403 = text.find('\n## JVB5403 Algal Summary')

# Determine what to delete: Appendix B through start of Nov 2025 section
# Between Appendix B and Nov 2025 we have: JVB5403 Algal Summary + JVB3988+JVB4678
if app_b_start != -1 and nov_section != -1:
    text = text[:app_b_start] + text[nov_section:]
    print(f'Removed Appendix B + Maine algal summaries')
elif app_b_start != -1 and jvb5403 != -1:
    # If no Nov section yet, remove Appendix B through end
    text = text[:app_b_start]
    print(f'Removed Appendix B through end')
else:
    print(f'WARNING: Appendix B marker not found: app_b={app_b_start}')

# ── 9. Fix note about Vivosun pH data ─────────────────────────────────────────
# Update the note in "How to Read" to note pH data is available site-by-site
text = text.replace(
    'All field pH readings in this dataset were made with a **Vivosun handheld pH meter (uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit).',
    'Field pH and temperature readings in this dataset were made with a **Vivosun handheld pH meter (uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit). Measurements are reported in °F. Field data are presented site-by-site where available.'
)

# ── 10. Fix the About note about "North Shore not Cape Cod" ──────────────────
text = text.replace(
    '\n> **Note: Sawmill Brook is in Manchester-by-the-Sea on the North Shore — not Cape Cod',
    ''
)

# Also clean up any orphaned > block quote fragments of that note
text = re.sub(r'> \*\*Note: Sawmill Brook[^\n]*\n', '', text)

# ── Write output ──────────────────────────────────────────────────────────────
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write(text)

n_lines = text.count('\n')
n_words = len(text.split())
print(f'Written: {OUT_MD}  ({n_lines} lines, {n_words} words)')

# Convert to docx
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
