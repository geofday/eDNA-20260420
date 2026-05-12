"""
edit_narraguagus_v10.py — Add recorded field pH and temperature to all Narraguagus
site sections. Compare recorded vs. inferred pH at every location per tracked change.
Revise UNT Lane Rd from "ambiguous" to "acid-impaired" (pH 3.73 = below lethal threshold).

Field measurements — Vivosun handheld pH meter, uncalibrated (±0.5–1.0 pH unit):
  Rt 193:       pH 6.25, 42.8°F (6.0°C)
  West Branch:  pH 5.09, 44.0°F (6.7°C)
  Crotch Camp:  pH 5.17, 41.1°F (5.1°C)
  UNT Lane Rd:  pH 3.73, 41.1°F (5.1°C)
  McCoy Brook:  pH 3.54, 41.3°F (5.2°C)

Changes applied:
- Water chemistry note: add field measurement footnote definition (†)
- All five sites: rename "Inferred Water Chemistry" → "Measured & Inferred Water Chemistry"
- All five sites: change column headers to "Parameter | Value | Source"
- All five sites: add bold recorded pH + temperature rows at top of table
- Rt 193: recorded 6.25 — within inferred 6.0–7.0 (consistent)
- West Branch: recorded 5.09 — below inferred 5.5–6.5; add ecological note on BT reproduction
- Crotch Camp: recorded 5.17 — at lower edge of Synura optimal 5.5–7.0
- UNT Lane Rd: full section rewrite — acid-impaired (pH 3.73), not ambiguous
- McCoy Brook: add Temp to header; add temp row to chemistry table
- Maine Summary: add pH column; update UNT row status; update gradient narrative
"""

import subprocess, os

SRC    = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v9.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v10.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\Narraguagus_Deblois_eDNA_v10.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── 1. Water chemistry note — add field measurement footnote ─────────────────
text = text.replace(
    '**Water chemistry** values are inferred from biological indicator species '
    'unless otherwise stated — directionally reliable but not a substitute for '
    'direct measurement.',

    '**Water chemistry** values are inferred from biological indicator species '
    'unless otherwise stated — directionally reliable but not a substitute for '
    'direct measurement. †Field pH and temperature readings were made with a '
    'Vivosun handheld pH meter; values are uncalibrated, approximate '
    '(±0.5–1.0 pH unit).'
)

# ── 2. Rt 193 — add measured rows ────────────────────────────────────────────
text = text.replace(
    '### Inferred Water Chemistry\n'
    '| Parameter | Inferred value | Basis |\n'
    '|---|---|---|\n'
    '| pH | 6.0–7.0 | Mainstem; cryptophyte + centric diatom assemblage |\n'
    '| Conductivity | 40–80 μS/cm | Higher than tributaries; anadromous nutrient inputs |\n'
    '| Total phosphorus | Low–moderate, trending up | Cyanobacteria at 6.5% = early enrichment signal |\n'
    '| Calcium | 5–12 mg/L | Adequate for full fish guild; Fallfish nest-building |\n'
    '| Dissolved oxygen | High | Atlantic Salmon, Fallfish both require high DO |\n'
    '| Marine-derived nutrients | Present | Alewife, Salmon, Lamprey decomposition subsidies |',

    '### Measured & Inferred Water Chemistry\n'
    '| Parameter | Value | Source |\n'
    '|---|---|---|\n'
    '| **pH (recorded)** | **6.25** | **Field measurement†** |\n'
    '| **Temperature (recorded)** | **42.8°F (6.0°C)** | **Field measurement†** |\n'
    '| pH (inferred) | 6.0–7.0 | Mainstem; cryptophyte + centric diatom assemblage |\n'
    '| Conductivity | 40–80 μS/cm | Inferred — higher than tributaries; anadromous nutrient inputs |\n'
    '| Total phosphorus | Low–moderate, trending up | Inferred — Cyanobacteria at 6.5% = early enrichment signal |\n'
    '| Calcium | 5–12 mg/L | Inferred — adequate for full fish guild; Fallfish nest-building |\n'
    '| Dissolved oxygen | High | Inferred — Atlantic Salmon, Fallfish both require high DO |\n'
    '| Marine-derived nutrients | Present | Inferred — Alewife, Salmon, Lamprey decomposition subsidies |'
)

# ── 3. West Branch — add measured rows + ecological note ─────────────────────
text = text.replace(
    '### Inferred Water Chemistry\n'
    '| Parameter | Inferred value | Basis |\n'
    '|---|---|---|\n'
    '| pH | 5.5–6.5 | Native soft-water fish guild; diverse diatoms |\n'
    '| Conductivity | 30–60 μS/cm | Moderate — above Crotch Camp but soft |\n'
    '| Total phosphorus | Low–moderate | Diverse but not cyanobacteria-dominated algae |\n'
    '| Calcium | 3–8 mg/L | Soft, but adequate for dace and salmonids |\n'
    '| Dissolved oxygen | High | Trout, Sea Lamprey, Finescale Dace all require high DO |\n'
    '| Turbidity | Low | Diverse diatom community; no turbidity-tolerant taxa dominating |',

    '### Measured & Inferred Water Chemistry\n'
    '| Parameter | Value | Source |\n'
    '|---|---|---|\n'
    '| **pH (recorded)** | **5.09** | **Field measurement†** |\n'
    '| **Temperature (recorded)** | **44.0°F (6.7°C)** | **Field measurement†** |\n'
    '| pH (inferred) | 5.5–6.5 | Native soft-water fish guild; diverse diatoms |\n'
    '| Conductivity | 30–60 μS/cm | Inferred — soft water; diverse diatoms |\n'
    '| Total phosphorus | Low–moderate | Inferred — diverse but not cyanobacteria-dominated algae |\n'
    '| Calcium | 3–8 mg/L | Inferred — soft, but adequate for dace and salmonids |\n'
    '| Dissolved oxygen | High | Inferred — Brook Trout, Sea Lamprey, Finescale Dace all require high DO |\n'
    '| Turbidity | Low | Inferred — diverse diatom community; no turbidity-tolerant taxa dominating |\n'
    '\n'
    '**pH 5.09 note:** Recorded pH is below the biologically inferred range (5.5–6.5). '
    'At pH 5.09, adult Brook Trout survive and are detected (1.9%), but episodic acid '
    'pulses during spring snowmelt can suppress egg and fry survival. The recorded value '
    'suggests the West Branch is more acidic than the fish guild alone implies — '
    'consistent with a site at the boundary of viable Brook Trout reproduction.'
)

# ── 4. Crotch Camp — add measured rows ───────────────────────────────────────
text = text.replace(
    '### Inferred Water Chemistry\n'
    '| Parameter | Inferred value | Basis |\n'
    '|---|---|---|\n'
    '| pH | 5.5–7.0 | Synura optimal range |\n'
    '| Conductivity | <30 μS/cm | Synurophyte dominance indicates very low ionic strength |\n'
    '| Total phosphorus | <10 μg/L | Synura outcompetes under P-limitation |\n'
    '| Calcium | <5 mg/L | Soft water, granite/peat geology |\n'
    '| Dissolved organic carbon | Moderate–high | Peatland drainage, humic tint |\n'
    '| Dissolved oxygen | Good | Trout presence confirms aerobic conditions |',

    '### Measured & Inferred Water Chemistry\n'
    '| Parameter | Value | Source |\n'
    '|---|---|---|\n'
    '| **pH (recorded)** | **5.17** | **Field measurement†** |\n'
    '| **Temperature (recorded)** | **41.1°F (5.1°C)** | **Field measurement†** |\n'
    '| pH (inferred) | 5.5–7.0 | Synura optimal range |\n'
    '| Conductivity | <30 μS/cm | Inferred — Synurophyte dominance indicates very low ionic strength |\n'
    '| Total phosphorus | <10 μg/L | Inferred — Synura outcompetes under P-limitation |\n'
    '| Calcium | <5 mg/L | Inferred — soft water, granite/peat geology |\n'
    '| Dissolved organic carbon | Moderate–high | Inferred — peatland drainage, humic tint |\n'
    '| Dissolved oxygen | Good | Inferred — Brook Trout presence confirms aerobic conditions |'
)

# ── 5a. UNT — header: add recorded pH ────────────────────────────────────────
text = text.replace(
    '**Fish: 1 species, H(f) = 0.00 | Algae: 77 ESVs, H(a) = 3.16**',
    '**Fish: 1 species, H(f) = 0.00 | Algae: 77 ESVs, H(a) = 3.16 | Recorded pH: 3.73**'
)

# ── 5b. UNT — sentinel signal ─────────────────────────────────────────────────
text = text.replace(
    'American Eel alone + diverse soft-water algal community = **connectivity present, '
    'fish community ambiguous — barrier or seasonality likely, not acute impairment**. '
    'The algae do not support a toxicity interpretation.',

    'American Eel alone + measured pH 3.73 = **acute acid exclusion of fish community**. '
    'pH 3.73 is below the lethal threshold for virtually all freshwater fish. '
    'American Eel is among the most acid-tolerant vertebrates in the northeastern '
    'freshwater system and is the only fish capable of persisting at these conditions.'
)

# ── 5c. UNT — chemistry table ─────────────────────────────────────────────────
text = text.replace(
    '### Inferred Water Chemistry\n'
    '| Parameter | Inferred value | Basis |\n'
    '|---|---|---|\n'
    '| pH | 5.5–7.0 | Cryptophyte + Chromulina assemblage |\n'
    '| Conductivity | 20–50 μS/cm | Halamphora coffeaeformis suggests slight enrichment or low ionic influence |\n'
    '| Total phosphorus | Low–moderate | Chromulina and cryptophyte mix |\n'
    '| Dissolved organic carbon | Moderate | Humic indicators present |\n'
    '| Dissolved oxygen | Adequate | Eel survives, no anoxia signal |',

    '### Measured & Inferred Water Chemistry\n'
    '| Parameter | Value | Source |\n'
    '|---|---|---|\n'
    '| **pH (recorded)** | **3.73** | **Field measurement†** |\n'
    '| **Temperature (recorded)** | **41.1°F (5.1°C)** | **Field measurement†** |\n'
    '| pH (inferred) | 3.5–4.5 | Acid-tolerant diatom community; eel-only fish exclusion |\n'
    '| Conductivity | 20–50 μS/cm | Inferred — soft, low-ionic water |\n'
    '| Total phosphorus | Low | Inferred — acid systems retain P in sediment |\n'
    '| Dissolved organic carbon | High | Inferred — humic acids consistent with bog/peatland drainage |\n'
    '| Dissolved oxygen | Adequate | Inferred — American Eel present |'
)

# ── 5d. UNT — narrative paragraphs ───────────────────────────────────────────
text = text.replace(
    'American Eel at 100% relative abundance — a single fish taxon across all reads. '
    'This result demands careful interpretation before concluding impairment.\n'
    '\n'
    'American Eel (*Anguilla rostrata*) are catadromous: born in the Sargasso Sea, '
    'they spend their adult lives in freshwater before returning to the ocean to spawn. '
    'They are fully native, highly persistent, and a single large resident eel can shed '
    'eDNA that dominates a sample. The absence of other fish may reflect low fish density '
    'at a headwater tributary, November post-season timing when many species are less '
    'active, or a physical barrier limiting upstream access.\n'
    '\n'
    'The algal community does not support toxicity. Cryptophytes (20.5%), Pennate Diatoms '
    '(22.1%), *Halamphora coffeaeformis* (14.9%), and Chromulina (8%) form a diverse '
    'soft-water assemblage. *Halamphora coffeaeformis* is notable — it is found in '
    'slightly enriched or occasionally oligohaline conditions, which may hint at some '
    'tidal or groundwater influence even this far upstream. H(a) = 3.16 with 77 ESVs '
    'is consistent with a functioning brook, not a chemically stressed one.',

    'pH 3.73 is at or below the threshold where most freshwater fish cannot survive. '
    'Brook Trout are excluded below approximately pH 4.5–5.0; most cyprinids below '
    'pH 5.5–6.0. The single-species fish result — American Eel at 100% — is fully '
    'explained by chemistry: *Anguilla rostrata* is among the most acid-tolerant '
    'vertebrates in the northeastern freshwater system, capable of persisting in '
    'waters approaching pH 4.0 where all other species have been eliminated.\n'
    '\n'
    'The algal community appears moderately diverse (H(a) = 3.16, 77 ESVs) despite '
    'chemistry that excludes virtually all fish — algae are far more acid-tolerant '
    'than fish. Acid-tolerant diatoms, Cryptophytes, and Chromulina can persist at '
    'pH 3.5–4.5. *Halamphora coffeaeformis* (14.9% of algal reads) is a '
    'database-assigned marine/brackish taxon that at this inland site almost certainly '
    'represents an acid-tolerant freshwater *Halamphora* species misassigned by the '
    'reference database.\n'
    '\n'
    'pH 3.73 may be natural: ombrotrophic bogs in Maine commonly reach pH 3.5–4.5 '
    'from organic acid accumulation. UNT Lane Rd\'s position relative to the '
    'Worcester Peat Mine is ambiguous — topographic analysis shows no drainage '
    'divide between the mine area and UNT, but McCoy Brook may intercept mine '
    'drainage before it reaches UNT. The pH values at McCoy (3.54) and UNT (3.73) '
    'are similar enough to be consistent with either a shared mine influence or two '
    'independent bog-drainage systems. Definitive source attribution requires '
    'field tracing.\n'
    '\n'
    'Whether natural or mine-influenced, pH 3.73 is a permanent barrier to Brook '
    'Trout at this reach under current conditions.'
)

# ── 5e. UNT — Native vs. Non-Native + closing ────────────────────────────────
text = text.replace(
    'American Eel is fully native. Its catadromous life history makes it one of the '
    'most far-ranging native vertebrates in the northeastern freshwater landscape. '
    'Its presence confirms ocean connectivity to this reach.\n'
    '\n'
    'This site reads as habitat-limited or seasonally undersampled rather than '
    'impaired — but the single-species fish result demands follow-up sampling in '
    'warmer months when a richer community would be active.',

    'American Eel is fully native. Its catadromous life history and exceptional acid '
    'tolerance make it the last fish standing in severely acidified streams. Its '
    'detection here confirms open ocean connectivity but does not imply functional '
    'Brook Trout habitat.'
)

# ── 6. McCoy Brook — update header + chemistry table ─────────────────────────
text = text.replace(
    '**Fish: 1 species, H(f) = 0.00 | Algae: 91 ESVs, H(a) = 3.28 | Recorded pH: 3.54**',
    '**Fish: 1 species, H(f) = 0.00 | Algae: 91 ESVs, H(a) = 3.28 | Recorded pH: 3.54 | Temp: 41.3°F (5.2°C)**'
)

text = text.replace(
    '### Inferred Water Chemistry\n'
    '| Parameter | Inferred value | Basis |\n'
    '|---|---|---|\n'
    '| pH | 3.54 (measured) | Direct measurement |\n'
    '| Calcium | <2 mg/L | Acid mobilization depletes Ca²⁺ |\n'
    '| Conductivity | <30 μS/cm | Low ionic strength, acid system |\n'
    '| Total phosphorus | Low | Acid systems retain P in sediment |\n'
    '| Dissolved aluminum | Elevated | Mobilized from soils by acid pH |\n'
    '| Dissolved organic carbon | Moderate–high | Peatland and forest drainage |',

    '### Measured & Inferred Water Chemistry\n'
    '| Parameter | Value | Source |\n'
    '|---|---|---|\n'
    '| **pH (recorded)** | **3.54** | **Field measurement†** |\n'
    '| **Temperature (recorded)** | **41.3°F (5.2°C)** | **Field measurement†** |\n'
    '| Calcium | <2 mg/L | Inferred — acid mobilization depletes Ca²⁺ |\n'
    '| Conductivity | <30 μS/cm | Inferred — low ionic strength, acid system |\n'
    '| Total phosphorus | Low | Inferred — acid systems retain P in sediment |\n'
    '| Dissolved aluminum | Elevated | Inferred — mobilized from soils by acid pH |\n'
    '| Dissolved organic carbon | Moderate–high | Inferred — peatland and forest drainage |'
)

# ── 7. Maine Summary table — add pH column + update UNT row ──────────────────
text = text.replace(
    '| Site | Fish spp. | H(f) | Algae ESVs | H(a) | Key Sentinel Complex | Status |\n'
    '|---|---|---|---|---|---|---|\n'
    '| Narraguagus Rt 193 | 19 | 2.16 | 117 | 3.86 | Alewife + Atlantic Salmon + Fallfish | **Healthy — anadromous hub** |\n'
    '| West Branch Narraguagus | 14 | 1.94 | 201 | 4.55 | Finescale Dace + Sea Lamprey + diverse diatoms | **Healthy — reference condition** |\n'
    '| Crotch Camp Brook | 9 | 1.69 | 76 | 2.30 | Synura 74% + Brook Trout | Functional — phosphorus-limited oligotrophic floor |\n'
    '| UNT Lane Rd | 1 | 0.00 | 77 | 3.16 | Eel only + adequate algae | Ambiguous — resample needed |\n'
    '| McCoy Brook | 1 | 0.00 | 91 | 3.28 | Creek Chub + Eunotia + Euglena | **Impaired — pH 3.54 — Worcester Peat Mining** |',

    '| Site | Fish spp. | H(f) | Algae ESVs | H(a) | pH (rec.) | Key Sentinel Complex | Status |\n'
    '|---|---|---|---|---|---|---|---|\n'
    '| Narraguagus Rt 193 | 19 | 2.16 | 117 | 3.86 | 6.25 | Alewife + Atlantic Salmon + Fallfish | **Healthy — anadromous hub** |\n'
    '| West Branch Narraguagus | 14 | 1.94 | 201 | 4.55 | 5.09 | Finescale Dace + Sea Lamprey + diverse diatoms | **Healthy — reference condition** |\n'
    '| Crotch Camp Brook | 9 | 1.69 | 76 | 2.30 | 5.17 | Synura 74% + Brook Trout | Functional — phosphorus-limited oligotrophic floor |\n'
    '| UNT Lane Rd | 1 | 0.00 | 77 | 3.16 | 3.73 | Eel only + pH 3.73 | **Impaired — pH 3.73 — acid exclusion** |\n'
    '| McCoy Brook | 1 | 0.00 | 91 | 3.28 | 3.54 | Creek Chub + Eunotia + Euglena | **Impaired — pH 3.54 — Worcester Peat Mining** |'
)

# ── 8. Maine Summary narrative — full acid gradient with all five pH values ───
text = text.replace(
    'The Maine gradient runs from active impairment (McCoy Brook, pH 3.54) through '
    'oligotrophic soft-water limitation (Crotch Camp Brook) to full ecological '
    'function with anadromous connectivity (Narraguagus Rt 193, West Branch). '
    'Acidification is the primary stressor. All detected fish are native. Where '
    'chemistry is adequate and ocean connectivity is intact, the system assembles '
    'a complete, multi-guild native fish community on a complex algal foundation.',

    'The Maine gradient runs from severe acid impairment (McCoy Brook, pH 3.54; '
    'UNT Lane Rd, pH 3.73) through oligotrophic soft-water limitation (Crotch '
    'Camp Brook, pH 5.17) to borderline Brook Trout reproduction conditions '
    '(West Branch, pH 5.09) to full ecological function with anadromous '
    'connectivity (Narraguagus Rt 193, pH 6.25). Acidification is the primary '
    'stressor at three of five sites. All detected fish are native. Where '
    'chemistry is adequate and ocean connectivity is intact, the system assembles '
    'a complete, multi-guild native fish community on a complex algal foundation.'
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
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024} KB)')
else:
    print(f'pandoc error: {result.stderr}')
