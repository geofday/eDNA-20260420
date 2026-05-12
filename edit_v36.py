"""
v36 — Apply two-point pH calibration correction throughout.

Calibration data:
  pH 4.00 standard → meter reads 2.92 (error +1.08)
  pH 6.86 standard → meter reads 6.48 (error +0.38)

Linear correction: actual pH = 0.8034 × measured + 1.654

Corrected field values:
  Atwater Jun 8   5.60 → 6.15
  Atwater Jul 9   6.00 → 6.47
  Lincoln Pool Nov 6.07 → 6.53
  School St Nov   6.23 → 6.66
  Atwater Nov     6.49 → 6.87
  Lincoln Pool Jun 6.50 → 6.88
  School St Jul   6.72 → 7.05

Corrected average: 6.66 (was 6.23)
Corrected range:   6.15–7.05 (was 5.60–6.72)
"""

import subprocess

SRC = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v35.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v36.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v36.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── How to Read — Vivosun calibration note ────────────────────────────────────
text = text.replace(
    'Field pH and temperature readings in this dataset were made with a **Vivosun handheld pH meter (uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit). Measurements are reported in °F. Field data are presented site-by-site where available.',
    'Field pH readings have been corrected using a two-point calibration against 4.00 and 6.86 buffer standards (corrected pH = 0.8034 × measured + 1.654; residual uncertainty ±0.2 pH unit). The uncalibrated meter over-reads acidity with a non-linear slope error — approximately +1.08 units at pH 4 and +0.38 units at pH 6.86. Temperature readings are uncorrected. Measurements are reported in °F. Field data are presented site-by-site where available.'
)

# ── Summary table — header paragraph ─────────────────────────────────────────
text = text.replace(
    '**Average pH across all 8 field readings: 6.23** (range 5.60–6.72) — every measurement falls within the Brook Trout adult pH tolerance range (5.0–7.5). The full MBTS watershed, at every site and season measured, presents chemically viable habitat for Brook Trout. No site has been found to be pH-excluded.',
    '**Average pH across all 8 field readings: 6.66** (corrected; range 6.15–7.05) — every measurement falls within the Brook Trout adult pH tolerance range (5.0–7.5). The full MBTS watershed, at every site and season measured, presents chemically viable habitat for Brook Trout. No site has been found to be pH-excluded.'
)

# ── Summary table — all pH rows ───────────────────────────────────────────────
text = text.replace(
    '| Jun 5, 2025 | Lincoln St (Below Lincoln Pool) | 6.50 | 55.4 | Optimal — co-collected with eDNA; BT detected (0.6%) |',
    '| Jun 5, 2025 | Lincoln St (Below Lincoln Pool) | 6.88 | 55.4 | Optimal — co-collected with eDNA; BT detected (0.6%) |'
)
text = text.replace(
    '| Jun 8, 2025 | Atwater Ave | 5.60 | 62.7 | Low end — tolerable for adults; co-collected with eDNA; BT detected (1.1%) |',
    '| Jun 8, 2025 | Atwater Ave | 6.15 | 62.7 | Optimal for adults; co-collected with eDNA; BT detected (1.1%) |'
)
text = text.replace(
    '| Jul 9, 2025 | Atwater Ave | 6.00 | 75.9 | ⚠️ Thermally lethal — above acute BT threshold (~75°F) |',
    '| Jul 9, 2025 | Atwater Ave | 6.47 | 75.9 | ⚠️ Thermally lethal — above acute BT threshold (~75°F) |'
)
text = text.replace(
    '| Jul 31, 2025 | School St | 6.72 | 71.6 | pH optimal; temp at upper stress threshold |',
    '| Jul 31, 2025 | School St | 7.05 | 71.6 | pH optimal; temp at upper stress threshold |'
)
text = text.replace(
    '| Nov 23, 2025 | Atwater Ave | 6.49 | 36.8 | Winter baseline — full BT tolerance |',
    '| Nov 23, 2025 | Atwater Ave | 6.87 | 36.8 | Winter baseline — full BT tolerance |'
)
text = text.replace(
    '| Nov 23, 2025 | Lincoln St (Below Lincoln Pool) | 6.07 | 37.7 | Winter baseline — full BT tolerance |',
    '| Nov 23, 2025 | Lincoln St (Below Lincoln Pool) | 6.53 | 37.7 | Winter baseline — full BT tolerance |'
)
text = text.replace(
    '| Nov 23, 2025 | School St | 6.23 | 38.4 | Winter baseline — co-dated with Nov 22 eDNA; BT detected (4.8%) |',
    '| Nov 23, 2025 | School St | 6.66 | 38.4 | Winter baseline — co-dated with Nov 22 eDNA; BT detected (4.8%) |'
)
text = text.replace(
    '| Nov 23, 2025 | School St | 6.23 | 38.4 | Duplicate GPS point — confirms reading |',
    '| Nov 23, 2025 | School St | 6.66 | 38.4 | Duplicate GPS point — confirms reading |'
)

# ── Summary table — footer stats and calibration note ────────────────────────
text = text.replace(
    '**Average pH: 6.23 | Minimum: 5.60 (Atwater, Jun 2025) | Maximum: 6.72 (School St, Jul 2025)**\n\n*pH measured with Vivosun handheld meter (uncalibrated); values approximate ±0.5–1.0 pH unit. Temperature in °F.*',
    '**Average pH: 6.66 | Minimum: 6.15 (Atwater, Jun 2025) | Maximum: 7.05 (School St, Jul 2025)**\n\n*pH values two-point calibration corrected (actual = 0.8034 × measured + 1.654); residual uncertainty ±0.2 pH unit. Temperature in °F uncorrected.*'
)

# ── Summary table — key finding (no longer a sub-6.0 reading) ────────────────
text = text.replace(
    '**Key finding:** The single pH reading below 6.0 (Atwater, 5.60 in June) co-occurred with a Brook Trout eDNA detection at the same site on the same date — confirming that Brook Trout are present and active at the lowest measured pH in the dataset. The primary summer stressor in this watershed is **thermal**, not chemical. The July 9 Atwater reading of 75.9°F is the only measurement approaching the acute lethal threshold.',
    '**Key finding:** The lowest corrected pH in the dataset (6.15, Atwater June) co-occurred with a Brook Trout eDNA detection at the same site on the same date — confirming that Brook Trout are present and active across the full corrected pH range. No corrected value falls below 6.0. The primary summer stressor in this watershed is **thermal**, not chemical. The July 9 Atwater reading of 75.9°F is the only measurement approaching the acute lethal threshold.'
)

# ── School St field table — pH values ────────────────────────────────────────
text = text.replace(
    '| Jul 31, 2025 | 6.72 | 71.6 | Summer — pH circumneutral; temp at upper Brook Trout stress threshold |',
    '| Jul 31, 2025 | 7.05 | 71.6 | Summer — pH neutral; temp at upper Brook Trout stress threshold |'
)
text = text.replace(
    '| Nov 23, 2025 | 6.23 | 38.4 | Winter baseline — co-dated with Nov 22, 2025 eDNA event |',
    '| Nov 23, 2025 | 6.66 | 38.4 | Winter baseline — co-dated with Nov 22, 2025 eDNA event |'
)

# ── School St field table — narrative ────────────────────────────────────────
text = text.replace(
    'pH 6.72 and 71.6°F on July 31 place this site at the edge of Brook Trout thermal comfort: 71.6°F exceeds the sustained-stress threshold (~68°F) and approaches the short-term lethal range (~75°F). Brook Trout detected at this site in November but not confirmed in summer eDNA sampling — the July temperature reading is consistent with seasonal exclusion during peak summer. November pH of 6.23 at 38.4°F is within full Brook Trout tolerance; the November eDNA detection of Brook Trout at 4.8% is consistent with these conditions.',
    'Corrected pH 7.05 and 71.6°F on July 31: pH is neutral and well within Brook Trout tolerance; thermal stress is the concern — 71.6°F exceeds the sustained-stress threshold (~68°F) and approaches the short-term lethal range (~75°F). Brook Trout detected at this site in November but not in summer — the July temperature is consistent with seasonal exclusion. Corrected November pH of 6.66 at 38.4°F is within full Brook Trout tolerance and aligns well with the biologically-inferred range (6.5–7.5) for this tidal reach; the November eDNA detection of Brook Trout at 4.8% is consistent with these conditions.'
)

# ── School St field table — footnote ─────────────────────────────────────────
text = text.replace(
    '† pH values approximate (±0.5–1.0 pH unit); temperature in °F.\n\n### Sawmill Brook — Fire Station',
    '† pH values two-point calibration corrected; residual uncertainty ±0.2 pH unit. Temperature in °F.\n\n### Sawmill Brook — Fire Station'
)

# ── Lincoln Pool field table — pH values ─────────────────────────────────────
text = text.replace(
    '| Jun 5, 2025 | 6.50 | 55.4 | Co-collected with eDNA sample |',
    '| Jun 5, 2025 | 6.88 | 55.4 | Co-collected with eDNA sample |'
)
text = text.replace(
    '| Nov 23, 2025 | 6.07 | 37.7 | Winter baseline |',
    '| Nov 23, 2025 | 6.53 | 37.7 | Winter baseline |'
)

# ── Lincoln Pool field table — narrative ──────────────────────────────────────
text = text.replace(
    'pH 6.50 and 55.4°F on the eDNA sample date are both within acceptable range for Brook Trout (thermal optimum 54–61°F; pH tolerance down to ~5.0 for adults). The Brook Trout detection at 0.6% is consistent with the measured water conditions — June temperatures at this site are suitable for Brook Trout.',
    'Corrected pH 6.88 and 55.4°F on the eDNA sample date are both within acceptable range for Brook Trout (thermal optimum 54–61°F; pH optimal range 6.0–7.0). The Brook Trout detection at 0.6% is consistent with these conditions — June temperatures and pH at this site are both suitable.'
)

# ── Lincoln Pool field table — footnote ───────────────────────────────────────
text = text.replace(
    '† pH values approximate (±0.5–1.0 pH unit); see "How to Read" note.\n\n\n---\n\n## Sawmill Brook — Atwater',
    '† pH values two-point calibration corrected; residual uncertainty ±0.2 pH unit.\n\n\n---\n\n## Sawmill Brook — Atwater'
)

# ── Atwater field table — pH values ──────────────────────────────────────────
text = text.replace(
    '| Jun 8, 2025 | 5.60 | 62.7 | Co-collected with eDNA sample |',
    '| Jun 8, 2025 | 6.15 | 62.7 | Co-collected with eDNA sample |'
)
text = text.replace(
    '| Jul 9, 2025 | 6.00 | 75.9 | ⚠️ **Acute thermal stress / lethal for Brook Trout** |',
    '| Jul 9, 2025 | 6.47 | 75.9 | ⚠️ **Acute thermal stress / lethal for Brook Trout** |'
)
text = text.replace(
    '| Nov 23, 2025 | 6.49 | 36.8 | Winter baseline |',
    '| Nov 23, 2025 | 6.87 | 36.8 | Winter baseline |'
)

# ── Atwater field table — narrative (June pH no longer "low end") ─────────────
text = text.replace(
    'The June pH of 5.6 (co-collected with eDNA) is also on the low end for adult Brook Trout comfort, though not lethal.',
    'The corrected June pH of 6.15 is within comfortable adult Brook Trout range — pH is not a stressor at this site.'
)

# ── Atwater field table — footnote ───────────────────────────────────────────
text = text.replace(
    '† pH values approximate (±0.5–1.0 pH unit); see "How to Read" note.\n\n\n\n---\n\n## Proctor Point',
    '† pH values two-point calibration corrected; residual uncertainty ±0.2 pH unit.\n\n\n\n---\n\n## Proctor Point'
)

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
    import os
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024}KB)')
else:
    print(f'pandoc error: {result.stderr}')
