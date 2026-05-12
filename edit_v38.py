"""
v38 — Accept all tracked changes from v36.docx (Geoffrey Day, 2026-04-28).

Changes applied:
- A Note on Interpretation: expanded eDNA science caveat; added statistical
  likelihood context; "detected (no matter how absurd), or not detected"
- About This Report: Proctor Point sentence reworded; sampling network sentence
  reordered; new paragraph on algae/conductivity/future studies; "possible
  anadromy" added; "fresh-to-salt water continuum" replaces "watershed"
- How to Read: "Shannon Diversity" capitalised; formula explanation added;
  "and environmental quality" added; BT Shannon range corrected (was flagged
  "(IS THIS TRUE??)" — Cat Brook H=0.65 is low, not mid-to-high; corrected to
  accurate range 0.65–1.40); ecological complexity sentence extended; [T8] kept
- Water chemistry note: calibration methodology removed per "Report ONLY
  calibrated numbers with NO reference to corrections!!" instruction
- pH table footnote: simplified to calibrated only
- Methods: "recommended field-sterile"; "Fish samples"; trailing "for analysis"
"""

import subprocess
import os

SRC      = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v36.md'
OUT_MD   = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v38.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v38.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── A Note on Interpretation ──────────────────────────────────────────────────
text = text.replace(
    '**This report states only what the data shows.** It does not hedge, model, '
    'estimate, or speculate beyond the evidence. If a species is not detected, '
    'that is what is written. If a reading is ambiguous, the ambiguity is named '
    'and the most likely interpretation is stated directly. Unsupported '
    'qualifications are not a substitute for data.',

    '**This report states only what the data shows.** It does not hedge, model, '
    'estimate, or speculate beyond the evidence. eDNA is an emerging science and '
    'while this is a best-effort analysis there may be mistakes; this preliminary '
    'report is shared for feedback more than as established fact. If a species is '
    'detected (no matter how unexpected), or not detected, that is what is written. '
    'The core of eDNA science is statistical likelihood drawn from billions of '
    'complete and fragmented DNA strands — results represent a percentage of '
    'detection probability more than a census of individuals, though relative '
    'abundance is a natural inference. If a reading is ambiguous, the ambiguity '
    'is named and the most likely interpretation is stated directly. Unsupported '
    'qualifications are not a substitute for data.'
)

# ── About This Report — Proctor Point sentence ────────────────────────────────
text = text.replace(
    'It also includes one marine sample at Proctor Point Dock '
    '(Manchester Harbor, June 2025), which provides ecological context '
    "for the watershed's coastal outlet.",

    'It also includes one marine sample at Proctor Point Dock '
    '(Manchester Harbor, June 2025), into which Sawmill Brook empties — '
    "providing ecological context for the watershed's coastal outlet."
)

# ── About This Report — sampling network sentence reordered ───────────────────
text = text.replace(
    'The sampling network covers the full longitudinal gradient: from Second Pond '
    'and Cat Brook headwaters through the main stem, past the tidal limit at '
    'Fire Station, to the estuarine School Street reach. ',

    'The sampling network covers the full longitudinal gradient: from Second Pond '
    'and Cat Brook headwaters through the main stem, from the estuarine School '
    'Street reach to the tidal limit at Fire Station.\n\n'
    'Algae predicts specific conductivity, which serves as a proxy for salinity. '
    'Future studies should include more thorough direct measurement of pH, '
    'salinity, and other water chemistry parameters.\n\n'
)

# ── About This Report — "possible anadromy" + "fresh-to-salt water continuum" ─
text = text.replace(
    'Their presence or absence at each site tells a story about water quality, '
    'thermal conditions, and habitat connectivity.',
    'Their presence or absence at each site tells a story about possible '
    'anadromy, water quality, thermal conditions, and habitat connectivity.'
)

text = text.replace(
    'is this watershed livable for Brook Trout',
    'is this fresh-to-salt water continuum livable for Brook Trout'
)

# ── How to Read — Shannon Diversity capitalised + formula explained ────────────
text = text.replace(
    '**Shannon diversity** is used throughout: **H(f)** for fish, **H(a)** for '
    'algae (formula: −Σ p·ln p). A higher value means more even distribution of '
    'reads across species — a proxy for ecological complexity.',

    '**Shannon Diversity** is used throughout: **H(f)** for fish, **H(a)** for '
    'algae. The formula −Σ p·ln p sums, for each species, its proportional '
    'abundance (p) multiplied by its natural log — so a community with many '
    'species each contributing similar read counts scores higher than one '
    'dominated by a single species. A higher value means more even distribution '
    'of reads across species — a proxy for ecological complexity and environmental '
    'quality. Brook Trout is detected across H(f) = 0.65–1.40 — the '
    'low-moderate to good diversity range in this dataset.'
)

# ── How to Read — ecological complexity sentence extended ─────────────────────
text = text.replace(
    '**Ecological complexity** is highly favorable to healthy ecosystems. '
    'Complex systems are more robust, more durable, more adaptable to '
    'environmental change, and more capable of supporting migration and '
    'reproduction. Shannon diversity (H) captures this: higher values mean '
    'more species contributing meaningfully to the community — not one '
    'dominant species and noise.',

    '**Ecological complexity** is highly favorable to healthy ecosystems. '
    'Complex systems are more robust, more durable, more adaptable to '
    'environmental change, and more capable of supporting migration and '
    'reproduction — and rich sources of food at all trophic levels. '
    'Shannon Diversity (H) captures this: higher values mean more species '
    'contributing meaningfully to the community — not one dominant species '
    'and noise.'
)

# ── Water chemistry note — remove calibration methodology ─────────────────────
text = text.replace(
    'Water chemistry values are **inferred** from biological indicator species '
    'unless otherwise stated — directionally reliable but not a substitute for '
    'direct measurement. Field pH readings have been corrected using a two-point '
    'calibration against 4.00 and 6.86 buffer standards (corrected pH = 0.8034 '
    '× measured + 1.654; residual uncertainty ±0.2 pH unit). The uncalibrated '
    'meter over-reads acidity with a non-linear slope error — approximately '
    '+1.08 units at pH 4 and +0.38 units at pH 6.86. Temperature readings are '
    'uncorrected. Measurements are reported in °F. Field data are presented '
    'site-by-site where available.',

    'Water chemistry values are **inferred** from biological indicator species '
    'unless otherwise stated — directionally reliable but not a substitute for '
    'direct measurement. pH values are calibrated; residual uncertainty ±0.2 pH '
    'unit. Temperature readings are reported in °F. Field data are presented '
    'site-by-site where available.'
)

# ── pH table footnote — simplified ───────────────────────────────────────────
text = text.replace(
    '*pH values two-point calibration corrected (actual = 0.8034 × measured + '
    '1.654); residual uncertainty ±0.2 pH unit. Temperature in °F uncorrected.*',
    '*pH values calibrated; residual uncertainty ±0.2 pH unit. Temperature in °F.*'
)

# ── Methods — "recommended field-sterile"; "Fish samples"; trailing phrase ─────
text = text.replace(
    'All samples were collected using Jonah Ventures (JV) eDNA field kits '
    'following field-sterile procedures. All samples were mailed to JV for '
    'processing. Most samples were analyzed using the MiFish 12S rRNA barcode '
    '(fish); several were also analyzed for algae using the 23S rRNA barcode. '
    'Results were processed in MS Excel and later using Artificial Intelligence '
    '(Claude / OpenAI).',

    'All samples were collected using Jonah Ventures (JV) eDNA field kits '
    'following recommended field-sterile procedures. All samples were mailed to '
    'JV for processing. Fish samples were analyzed using the MiFish 12S rRNA '
    'barcode; several samples were also analyzed for algae using the 23S rRNA '
    'barcode. Results were processed in MS Excel and later using Artificial '
    'Intelligence (Claude / OpenAI) for analysis.'
)

# ── Sentinel species table — Brook Trout row note (minor wording) ─────────────
# (No tracked change here — leave as is)

# ── Write output ──────────────────────────────────────────────────────────────
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
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024} KB)')
else:
    print(f'pandoc error: {result.stderr}')
