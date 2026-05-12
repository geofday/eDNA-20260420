"""
Assemble Sawmill Brook / Cat Brook / Manchester-by-the-Sea focused eDNA report.
Extracts relevant sections from v20 and writes a standalone document.
"""

import re

SRC = r'C:\repos\eDNA-20270420\output\eDNA_Reports_by_Location_v30.md'
OUT = r'C:\repos\eDNA-20270420\output\Sawmill_CatBrook_eDNA_Report_v1.md'

with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_lines(start, end):
    """Return lines[start-1:end-1] (1-indexed, inclusive)."""
    return lines[start-1:end-1]

def strip_leading_hr(block):
    """Remove leading --- lines and blank lines from a block."""
    result = list(block)
    while result and result[0].strip() in ('', '---'):
        result.pop(0)
    return result

def strip_trailing_hr(block):
    """Remove trailing --- lines and blank lines from a block."""
    result = list(block)
    while result and result[-1].strip() in ('', '---'):
        result.pop()
    return result

def clean_block(block):
    return strip_trailing_hr(strip_leading_hr(block))

# --- CUSTOM INTRO ---
intro = """\
# eDNA Ecological Report — Sawmill Brook / Cat Brook Watershed
## Manchester-by-the-Sea Brook Trout Monitoring Program (MBTS)
### Manchester-by-the-Sea, MA · November 2023 – June 2025

---

## A Note on Interpretation

**This report states only what the data shows.** It does not hedge, model, estimate, or speculate beyond the evidence. If a species is not detected, that is what is written. If a reading is ambiguous, the ambiguity is named and the most likely interpretation is stated directly. Unsupported qualifications are not a substitute for data.

---

## About This Report

This report covers **17 water samples** across 12 distinct sites in and around the Sawmill Brook / Cat Brook watershed in Manchester-by-the-Sea, MA, spanning November 2023 through June 2025. It also includes one marine sample at Proctor Point Dock (Manchester Harbor, June 2025), which provides ecological context for the watershed's coastal outlet.

The Manchester-by-the-Sea Brook Trout Monitoring Program (MBTS) tracks ecological recovery of Sawmill Brook — a small suburban coastal stream that drains southwest into Manchester Harbor. The sampling network covers the full longitudinal gradient: from Second Pond and Cat Brook headwaters through the main stem, past the tidal limit at Fire Station, to the estuarine School Street reach. Three Fresh Brook samples (a tributary flowing separately to Manchester Harbor) are included.

Brook Trout (*Salvelinus fontinalis*) are the primary monitoring target. Their presence or absence at each site tells a story about water quality, thermal conditions, and habitat connectivity. All other species detected — from Golden Shiner to Mummichog to *Esox* spp. — are interpreted in relation to that central question: is this watershed livable for Brook Trout, and what is limiting or sustaining their population?

---

## How to Read This Report

Algae are the base of the food web. They respond within days to light, temperature, pH, nutrients, and dissolved minerals. Fish integrate conditions over years — they reflect whether the habitat has been livable long enough to support recruitment, growth, and community assembly. Together, algae and fish tell a story neither can tell alone.

**Shannon diversity** is used throughout: **H(f)** for fish, **H(a)** for algae (formula: −Σ p·ln p). A higher value means more even distribution of reads across species — a proxy for ecological complexity.

| H value | Interpretation |
|---|---|
| 0.00 | Single species / monoculture |
| 0.01 – 0.30 | Near-monoculture (>90% one species) |
| 0.30 – 0.80 | Low diversity (2–3 species dominant) |
| 0.80 – 1.40 | Moderate diversity (4–6 species) |
| 1.40 – 2.00 | Good diversity (6–10 species) |
| 2.00 – 2.50 | High diversity (10–15+ species) |
| 2.50+ | Very high diversity (richest communities) |

**Read counts** are proportional, not absolute. A species at 1% with 10,000 total reads (100 reads) is more reliable than a species at 1% with 500 total reads (5 reads). Read count footnotes are provided where this distinction matters.

Water chemistry values are **inferred** from biological indicator species unless otherwise stated — directionally reliable but not a substitute for direct measurement. All field pH readings in this dataset were made with a **Vivosun handheld pH meter (uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit).

**Site order:** Sites are presented upstream-to-downstream where possible, followed by Fresh Brook, then Proctor Point marine reference.

---

## Key Findings — Sawmill / Cat Brook System

| Finding | Site | Significance |
|---|---|---|
| **Brook Trout confirmed — 4 sites** | Golf Course (Nov 2023), Below School St (Nov 2023 + Aug 2024), Atwater (Jun 2025), Below Lincoln Pool (Jun 2025) | Persistent multi-site presence across two years |
| ***Esox* spp. (db: *Esox lucius*) detected** | Second Pond (Oct 2024) | Likely native pickerel (Chain or Redfin); Northern Pike assignment anomalous — verify by electrofishing before acting |
| **Alewife at 63% — Second Pond only** | Second Pond (Oct 2024) | Only Alewife in entire watershed; possible landlocked population — fishway status critical |
| **Sculpin confirmed** | Atwater Site (Jun 2025) | Cold benthic indicator = high-quality cold-water habitat |
| **Cormorant dietary eDNA** | Atwater Site (Jun 2025) | Menhaden + Xiphister prove bird fecal input — Alewife at this site = artifact, not live fish |
| **Stoneworts (Charophyceae) at 35%** | Golf Course / Sawmill Brook (Nov 2023) | Ca-rich groundwater signal — native vs. invasive (*Nitellopsis obtusa*) requires field verification |
| **Tidal-freshwater algal gradient** | School St vs. Elm St (Mar 2025) | Sharpest within-system contrast in dataset — marine algae below tidal limit, cold chrysophytes above |
| **16-species marine assemblage** | Proctor Point Dock (Jun 2025) | Richest single-sample community in dataset — Herring, Mackerel, Hickory Shad, Striped Bass |

---

## Sentinel Species — Sawmill/Cat Brook Context

| Species | What it signals | Notes |
|---|---|---|
| **Brook Trout** (*Salvelinus* spp.) | Cold, clean, well-oxygenated water | Native; primary monitoring target |
| **Sculpin** (Cottidae) | Cold benthic habitat; structurally complex substrate | Same requirements as Brook Trout |
| **American Eel** | Catadromous connectivity — ocean to headwaters | Wide tolerance; confirms no impassable barriers |
| **Mummichog** | Tidal/estuarine influence | Marks tidal penetration limit |
| **Fourspine Stickleback** | Brackish-water; tidal transition | Confirms estuarine zone |
| **Golden Shiner** (dominant) | Slow warm water; may be from upstream pond | Common in lentic/semi-lentic reaches |
| ***Esox* spp.** | Native pickerel likely; Northern Pike possible but unconfirmed | Database anomaly — verify by electrofishing |
| **Alewife** | Anadromous connectivity; landlocked if no downstream signal | Only at Second Pond — fishway investigation required |
| ***Synura* / Chrysophytes** | Cold, clean, phosphorus-limited soft water | Indicates high-quality coldwater headwater conditions |
| **Charophytes (Stoneworts)** | Calcium-rich, clear, low-turbidity groundwater input | Cannot distinguish native *Chara/Nitella* from invasive *Nitellopsis* without field ID |
| **Marine estuarine diatoms** | Tidal penetration | At School St = normal; further upstream = anomalous |

---

"""

# --- SECTION EXTRACTOR ---
# Sections to pull from v29 (start_line, end_line)
# All line numbers are 1-indexed from v29
sections = [
    # MBTS intro block (paragraphs before Upper Sawmill)
    (1668, 1684),
    # Upper Sawmill
    (1686, 1711),
    # Below School St (Nov 2023 — JVB5776)
    (1715, 1745),
    # Lower Golf Course / Sawmill Brook + MA Summary
    (1749, 1811),
    # Massachusetts Summary table (inside above range — deduplicated below)
    (1795, 1811),
    # Three Sawmill Sites header + Aug 2024 batch (Swamp, Below School St, Fire Station)
    (1812, 1917),
    # Cat Brook / Forest Landing
    (1921, 1976),
    # Second Pond
    (2171, 2229),
    # School St (Mar 2025)
    (2117, 2167),
    # Elm Street (Mar 2025)
    (2233, 2289),
    # MBTS #3
    (1980, 2013),
    # Below Lincoln Pool
    (2017, 2048),
    # Atwater Site (full — includes cormorant QC + field measurements)
    (2052, 2113),
    # Fresh Brook Route 6 (Low Tide)
    (2419, 2464),
    # Fresh Brook Impoundment (includes July 2024 field measurements)
    (2468, 2523),
    # Fresh Brook Raccoon Feces
    (2765, 2808),
    # Proctor Point Dock
    (2991, 3040),
]

# --- BROOK TROUT CROSS-BATCH MBTS SUMMARY ---
# Pull the Brook Trout summary table rows relevant to MBTS
bt_header = get_lines(3044, 3066)  # cross-batch Brook Trout section header + table

# Filter Brook Trout table to MBTS sites only
mbts_keywords = ['Sawmill', 'School St', 'Golf Course', 'Atwater', 'Lincoln Pool',
                  'MBTS', 'Manchester', 'Cat Brook', 'Elm St', 'Upper Sawmill',
                  'Below School']

def filter_bt_table(block_lines):
    """Keep table header rows and only MBTS-relevant data rows."""
    out = []
    in_table = False
    header_rows = 0
    for line in block_lines:
        stripped = line.strip()
        if stripped.startswith('|') and '---|' in stripped:
            in_table = True
            out.append(line)
            continue
        if stripped.startswith('|') and in_table:
            # Keep if it's a header row or contains MBTS keyword
            if header_rows < 1:
                out.append(line)
                header_rows += 1
            elif any(kw.lower() in line.lower() for kw in mbts_keywords):
                out.append(line)
        elif stripped.startswith('|'):
            out.append(line)
        elif not stripped.startswith('|') and in_table and stripped:
            in_table = False
            out.append(line)
        else:
            out.append(line)
    return out

# --- APPENDIX: Non-aquatic eDNA + Cormorant ---
appendix_nonaquatic = get_lines(3138, 3230)  # Non-aquatic + cormorant section

# --- ASSEMBLE ---
output_parts = [intro]

# Deduplicate: Massachusetts Summary table appears in two ranges, only include once
seen_ranges = set()
unique_sections = []
for s, e in sections:
    key = (s, e)
    if key not in seen_ranges:
        # Skip the duplicate MA Summary (1792-1805) since it's inside 1746-1803
        if s == 1795:
            continue
        seen_ranges.add(key)
        unique_sections.append((s, e))

for start, end in unique_sections:
    block = get_lines(start, end)
    cleaned = clean_block(block)
    if cleaned:
        output_parts.append('\n\n---\n\n')
        output_parts.append(''.join(cleaned))

# Brook Trout cross-batch appendix (MBTS filter)
output_parts.append('\n\n---\n\n')
output_parts.append('# Appendix A — Brook Trout Detections: Sawmill / Cat Brook Sites\n\n')
bt_full = get_lines(3044, 3131)
output_parts.append(''.join(filter_bt_table(bt_full)))

# Non-aquatic + cormorant appendix
output_parts.append('\n\n---\n\n')
output_parts.append('# Appendix B — Non-Aquatic eDNA & Cormorant Dietary Artifacts\n\n')
output_parts.append(''.join(appendix_nonaquatic))

final = ''.join(output_parts)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(final)

# Count lines and words
n_lines = final.count('\n')
n_words = len(final.split())
print(f'Written: {OUT}')
print(f'Lines: {n_lines}  Words: {n_words}')
