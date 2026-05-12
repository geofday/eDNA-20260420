# eDNA Project — Standing Rules for All Work

---

## Trout Are the Center of This Work

This project exists because of trout. All funding is trout-sourced — by fishermen,
for fishermen. Trout are the **charismatic canary-in-the-coal-mine**: their presence
confirms cold, clean, well-oxygenated, low-nutrient water; their absence is the
alarm. Every narrative, every summary, every chart caption must be oriented toward
what the data means for trout and trout habitat.

### Standing rules for trout framing

- **Trout presence or absence is always stated explicitly** for every site and batch
  where MiFish data is available. It is not inferred, assumed, or left implicit.
- **Interpret algal signals through the lens of trout habitat suitability.** What
  does Cyanobacteria dominance mean for dissolved oxygen? What does low H_a mean
  for invertebrate forage base? What does Dictyochophyte or marine-infiltration
  signal say about hydrological connectivity that trout depend on?
- **Diadromous species (Brook Trout, Atlantic Salmon, Alewife, Sea-run Brown Trout)
  are especially significant.** Their eDNA confirms active migratory corridors.
  Name them, celebrate them, explain what their presence means ecologically.
- **Brook Trout (_Salvelinus fontinalis_)** is the primary target species — native
  to Maine and Massachusetts cold-water streams, highly sensitive to temperature,
  pH, sedimentation, and low dissolved oxygen. It is the most important single
  species in any narrative produced by this project.
- **Brown Trout (_Salmo trutta_)** is **non-native and introduced** — a European
  species stocked throughout New England, considered invasive by some ecologists
  because it competes directly with native Brook Trout. Do not frame Brown Trout
  detection as a positive ecological indicator. Note its introduced/stocked status
  in all narratives. We have no evidence of sea-run Brown Trout in any study system;
  do not imply it.
- **Rainbow Trout (_Oncorhynchus mykiss_)** is similarly non-native and stocked
  in the Northeast. Treat as introduced where detected.
- **eDNA CANNOT distinguish life history forms.** MiFish 12S sees species only,
  not ecotype. Never claim eDNA detected a sea-run or salter form — that requires
  otolith, tagging, or electrofishing data.
- If trout are absent from a site where habitat indicators (cold water, high DO,
  low nutrients) suggest they should be present, **flag this as a finding** —
  it may indicate barrier, impairment, or population collapse.
- If trout are present despite impaired algal signals, **flag this as resilience**
  — and note the risk that deteriorating conditions may not yet have crossed the
  threshold.

### Narrative voice
Write as if the audience is a trout fisherman who cares about science and wants
honest, grounded answers. Not academic jargon. Not cheerleading. The water either
supports trout or it doesn't, and the eDNA data tells us which way it's heading.

## Project
Batch JVB5776 — 23S rRNA (algae) + MiFish 12S rRNA (fish)
Sites: 5 Maine (Deblois, Narraguagus watershed) + 3 Massachusetts (Manchester-by-the-Sea)
Script: analyze_edna.py | Output: output/

---

## Non-Negotiable Rules

### No non-aquatic species — EVER
Do not reference, discuss, mention, or interpret any non-aquatic organism in any narrative,
chart label, summary, or analysis output. This includes but is not limited to:
- Terrestrial mammals (Moose, Beaver, Muskrat, Wild Boar, Sheep, Deer, etc.)
- Birds (Wood Duck, Bufflehead, Heron, etc.)
- Amphibians and reptiles (Salamander, Newt, Turtle, etc.)
- Domestic livestock or agricultural animals of any kind
- Any non-fish vertebrate detected incidentally by the MiFish 12S panel

These are non-target detections. They are filtered from all analysis (NON_FISH set)
and must never appear in outputs, narratives, or interpretations. Period.

### Ducktrap River always separate
Sample 4JKGTSJ5.1 (Ducktrap River, Lincoln ME) is NEVER grouped with ME_SITES.
It is defined as the DUCKTRAP constant and always treated independently.
Its anadromous-dominated community (Alewife) is ecologically distinct from the
Deblois brook sites and distorts all comparisons if included.

### Fish charts — fish only
All MiFish bar charts, heatmaps, and stacked bars show fish species only.
Filter NON_FISH before charting. Re-normalize fish-only reads to 100%.

### Apply changes everywhere immediately
When a rule, filter, or label change is established, apply it to every chart
function, constant, and output in the same edit session. Never piecemeal.

### Data only — never model or estimate
Do not invent, estimate, or model data values. Only chart and interpret
real measured eDNA read abundances from the CSV files.

### Version control all outputs
Use _versioned() helper for all chart outputs. Files are named _v1, _v2 etc.
Never overwrite a previous version.

---

## Key Site Facts

### McCoy Brook (CSWEE3DX.1)
- pH 3.54 (measured)
- Impairment source: **Worcester Peat Mining** — upstream industrial peat extraction
  operation active for well over a decade. This is the primary anthropogenic driver
  of impairment. Do not attribute to "natural peat bog drainage" or acid rain alone.
  Worcester Peat Mining is significant, pervasive, and anthropogenic.

### Golf Course / Sawmill Brook (C4SUMTFY.1)
- Dominant algal signal: Charophyceae (Stonewort class), 35% relative abundance
- **Genus not resolved in 23S rRNA data** — cannot confirm native Chara/Nitella
  vs. invasive Starry Stonewort (Nitellopsis obtusa) without in-situ verification
- Flag this uncertainty in all narratives. Do not call it a positive indicator
  without confirming species identity.

---

## Shannon Notation
- H_f = fish Shannon diversity
- H_a = algae Shannon diversity
- Both use identical formula: -sum(p * ln(p))
- In Word output: rendered as native subscript (no HTML markup visible)

---

## Sample Constants
ME_SITES = ['CY92PPTX.1', 'CSWEE3DX.1', 'CNTLVPX4.1', 'CNR7WZYJ.1', 'CA66THTZ.1']
DUCKTRAP = '4JKGTSJ5.1'
MA_SITES = ['CVVU52A9.1', 'CDWD42KP.1', 'C4SUMTFY.1']
