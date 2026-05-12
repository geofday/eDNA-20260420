# eDNA Ecological Narrative — Batch JVB5776
**23S rRNA (Algae) + MiFish 12S rRNA (Fish) | November 2025**

---

## How to Read This

Algae are the base of the food web. They respond within days to light, temperature, pH, nutrients, and dissolved minerals. Fish integrate conditions over years — they reflect whether the habitat has been livable long enough to support recruitment, growth, and community assembly. Together, algae and fish tell a story neither can tell alone: algae describe the water chemistry and productivity; fish describe whether that chemistry is compatible with vertebrate life and whether the system is connected to a broader landscape.

Shannon diversity is used throughout: **H(f)** for fish, **H(a)** for algae. Both use the same formula (−Σ p·ln p); the subscripts distinguish which community is being described. A higher value means more even distribution of reads across species — a proxy for ecological complexity.

| H value | Interpretation |
|---|---|
| 0.00 | Single species / monoculture |
| 0.01 – 0.30 | Near-monoculture (>90% one species) |
| 0.30 – 0.80 | Low diversity (2–3 species dominant) |
| 0.80 – 1.40 | Moderate diversity (4–6 species) |
| 1.40 – 2.00 | Good diversity (6–10 species) |
| 2.00 – 2.50 | High diversity (10–15+ species) |
| 2.50+ | Very high diversity (richest communities) |

**ESV (Exact Sequence Variant)** — each site header reports the number of ESVs detected (e.g., "91 ESVs"). An ESV is one unique DNA sequence recovered from the water sample, after error-correction. It is not the same as a species count: a single species can generate several ESVs (different individuals, haplotypes, or gene copies), and closely related species can share ESVs. Think of ESV count as raw genetic diversity — a high number means many distinct sequences were found, but species richness (the count of taxonomically assigned organisms) will always be lower. ESV count combined with Shannon diversity gives a more complete picture than either alone.

Water chemistry values below are **inferred** from biological indicator species — not directly measured (except where pH is noted as recorded). Biological inference is directionally reliable but not a substitute for chemical sampling.

> **pH measurement note — Deblois / Narraguagus is the only site in this dataset with field-measured pH values.** All other sites in this study rely solely on algal biological indicators to infer pH; no field pH measurements were taken. The readings here are the only directly observed pH numbers in the entire eDNA dataset. They were made with a **Vivosun handheld pH meter (uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit) rather than laboratory-grade measurements. The directional interpretation remains valid — pH 3.73 is acidic and ecologically significant regardless of precise value — but specific thresholds (e.g., "Brook Trout egg survival impaired below 5.5") should be understood as approximations given measurement uncertainty.
>
> **† Field measurement** = Vivosun handheld pH meter (uncalibrated), ±0.5–1.0 pH unit. Used wherever pH appears as "Field measurement†" in the water chemistry tables below.

**A critical note on native vs. non-native species.** Native status is not a minor qualifier — it is a fundamental ecological distinction. A native fish community represents thousands of years of co-evolution with local water chemistry, hydrology, prey, and competitors. A non-native species disrupts that balance, often catastrophically. The presence of an intact native community is therefore as important a finding as species richness or Shannon diversity. The absence of common invasive species is a positive result, not a neutral one — it means the community has not yet been restructured by invasion pressure. This dataset is read with that lens throughout.

---

---

## Sentinel Species Reference

Certain species — alone or in simple combinations — compress the complex story of a site into a single readable signal. These are the sentinels: biological shorthand for water chemistry, connectivity, and ecological health. The table below is a guide for reading the site narratives that follow.

### Diadromous Species: The Ocean-Watershed Bridge

Diadromous fish migrate between freshwater and saltwater as a fundamental part of their life cycle. They are not just fish — they are ecological connectors, carrying energy and nutrients between the ocean and the continental interior. Their presence in eDNA is one of the most information-rich signals in the dataset.

**Anadromous** species are born in freshwater, migrate to the ocean to grow, and return to freshwater to spawn. **Catadromous** species do the reverse — born at sea, they live in freshwater and return to the ocean to spawn. Both types depend on unobstructed migratory corridors, which means their detection is simultaneously a water quality signal and a connectivity signal.

| Species | Migration type | Ecological role | Detection in this dataset |
|---|---|---|---|
| **Atlantic Salmon** (*Salmo salar*) | Anadromous | Federally endangered US population; returns marine P and N to watershed; requires cold, clean, gravel-bed streams | Narraguagus Rt 193 (trace) |
| **Alewife** (*Alosa pseudoharengus*) | Anadromous | Spring spawning runs deliver massive marine nutrient subsidy; forage base for many predators | Narraguagus Rt 193 (dominant, 26.3%) |
| **Sea Lamprey** (*Petromyzon marinus*) | Anadromous | Native Atlantic coast species; larvae filter-feed in stream sediment for 3–7 years; adults parasitic at sea; ancient ecosystem link | West Branch + Narraguagus Rt 193 (trace) |
| **Rainbow Smelt** (*Osmerus mordax*) | Anadromous | Spring spawning runs; critical forage fish for striped bass, salmon, and herons | Golf Course/Sawmill MA (trace) |
| **American Eel** (*Anguilla rostrata*) | Catadromous | Born in the Sargasso Sea; lives 10–30+ years in freshwater; returns to ocean to spawn once; wide habitat tolerance | 6 of 8 sites |
| **Atlantic Tomcod** (*Microgadus tomcod*) | Amphidromous | Moves seasonally between fresh and salt; estuarine spawner | MA sites |

**What diadromous fish bring to these watersheds.** When anadromous fish die after spawning, their marine-derived bodies decompose in the freshwater system. Every carcass is a nutrient packet — marine phosphorus, nitrogen, and carbon imported from the ocean and deposited in a stream that is otherwise phosphorus-limited. A strong Alewife run can measurably elevate stream phosphorus for weeks. Atlantic Salmon carcasses have been shown to fertilize streamside vegetation, increase insect emergence, and elevate fish growth rates for miles downstream. Sea Lamprey, despite their parasitic ocean phase, contribute the same carcass subsidy on return. The Cyanobacteria signal at Narraguagus Rt 193 — the site with the strongest anadromous fish community — is consistent with exactly this: a natural, cyclical phosphorus pulse from marine-origin biomass. The eel, as the only catadromous species, moves in the reverse direction — exporting freshwater biomass to the ocean when it finally migrates to spawn, contributing to the marine food web instead.

**What diadromous presence requires.** Detection of any of these species demands: (1) no impassable barriers between this site and tidal water; (2) water chemistry adequate for migration (pH >5.5, dissolved oxygen adequate, no acute toxicity); (3) functioning spawning habitat somewhere in the connected system. Their eDNA in November does not necessarily mean they were present in November — anadromous residual DNA can persist weeks to months in cool water. But it does confirm that the corridor is open and the habitat has been used.

### Fish Sentinels

| Species | What it signals | Chemistry inferred |
|---|---|---|
| **Atlantic Salmon** | Pristine cold water, functioning ocean corridor, federally listed | pH 6.0–7.5, high dissolved oxygen, low P, no upstream barriers |
| **Finescale Dace** | Highest-quality soft-water habitat in ME; brook trout associate | pH 5.5–6.5, low conductivity, clean fine substrate |
| **Fallfish** | Clean, well-oxygenated gravel streams; builds large nest mounds | pH 6.0–7.5, low turbidity, stable flow |
| **Alewife** | Open anadromous corridor to Gulf of Maine; marine P and N carrier | pH >5.5, no impassable barriers, tidal connectivity |
| **Sea Lamprey** | Functioning migratory corridor; larval habitat = clean stream sediment | pH >5.5, connected to ocean, clean fine gravel/sand |
| **Rainbow Smelt** | Anadromous coastal connectivity; forage fish signal | pH >6.0, tidal access, cool water |
| **Creek Chub (sole species)** | Acute acid stress; threshold sentinel — if alone, pH likely <5 | pH <5.0, depleted calcium, elevated aluminum |
| **American Eel** | Ocean connectivity present; catadromous, wide tolerance | pH 5–8, survives low DO and wide salinity range |
| **Mummichog** | Tidal/salt marsh; salinity-tolerant generalist | 0–30 ppt, tidal dynamics, periodic low oxygen |
| **Fourspine Stickleback** | Brackish-water specialist; tidal transition indicator | 0.5–15 ppt, estuarine or tidal freshwater |

All fish species detected in this dataset are **native** to their respective regions with one practical caveat: Largemouth Bass, Sunfish spp., and Bullhead spp. in the MA sites are native to eastern North America but are routinely stocked in Massachusetts ponds — their presence at Upper Sawmill may reflect stocking rather than natural recruitment.

### Algae Sentinels

| Group / Species | What it signals | Chemistry inferred |
|---|---|---|
| **Stoneworts** (*Chara*, *Nitella*) | Clean, calcium-rich, clear, unimpaired | pH 6.5–8.0, Ca²⁺ >15 mg/L, low turbidity, low nutrients |
| **Synura** (Colonial Synurophyte) | Soft, oligotrophic, slightly acidic; dominance = nutrient floor | pH 5.5–7.0, conductivity <30 μS/cm, total P <10 μg/L |
| **Eunotia / Pinnularia** (Pennate Diatoms) | Acidic, mineral-poor water; acid-specialist guild | pH <6.0, low Ca, low conductivity |
| **Euglena** | Organic enrichment + acid tolerance; persists where others cannot | pH 4.0–6.0, elevated organic matter |
| **Cryptophytes** (*Cryptomonas*, *Geminigera*) | Humic, soft water, moderate productivity; stratification-tolerant | pH 5.5–7.0, moderate DOC, low–moderate nutrients |
| **Centric Diatoms** | Nutrients and silica available; productive, open-water conditions | pH 6.0–8.0, moderate P and N, adequate silica |
| **Cyanobacteria** | Early nutrient enrichment warning — not alarming at low levels, but a flag | pH >6.5, elevated N and/or P, warmer conditions |
| **Mallomonas** (Scaled Synurophyte) | Soft, slightly acidic, oligotrophic — same guild as Synura | pH 5.0–7.0, low conductivity, low nutrients |

**Reading sentinel combinations:** A site showing Creek Chub alone + Eunotia/Pennate Diatoms + Euglena is a three-independent-line acid impairment signal. A site showing Atlantic Salmon + Fallfish + Finescale Dace is a three-independent-line reference condition signal. These combinations are more meaningful than any single indicator.

---

---

# MAINE — Deblois, ME | November 11, 2025

All five Maine sites drain into or near the Narraguagus River watershed in Washington County — a landscape of granite bedrock, spruce-fir forest, and peatland. The geology produces naturally soft, low-mineral, humic water. This is the background condition. Departures from it — in either direction — are the story.

---

## McCoy Brook | JVB5776 / CSWEE3DX.1
**Fish: 1 species, H(f) = 0.00 | Algae: 91 ESVs, H(a) = 3.28 | Recorded pH: 3.54**

### Sentinel Signal
Creek Chub alone + Eunotia/Pinnularia Pennate Diatoms + Euglena = **three-line acid impairment signal**. Each indicator independently points to the same conclusion.

### Inferred Water Chemistry
| Parameter | Inferred value | Basis |
|---|---|---|
| **pH** | **3.54** | **Field measurement†** |
| **Temperature** | **41.3°F (5.2°C)** | **Field measurement** |
| Calcium | <2 mg/L | Acid mobilization depletes Ca²⁺ |
| Conductivity | <30 μS/cm | Low ionic strength, acid system |
| Total phosphorus | Low | Acid systems retain P in sediment |
| Dissolved aluminum | Elevated | Mobilized from soils by acid pH |
| Dissolved organic carbon | Moderate–high | Peatland and forest drainage |

### Narrative
At pH 3.54, the water is more acidic than black coffee. Fish gills cannot regulate ions across such a gradient. Most freshwater fish experience acute physiological stress below pH 5.0 and lethal conditions below pH 4.5. pH 3.54 is well below both thresholds.

The fish community confirms it: only Creek Chub detected, at 100% relative abundance. Creek Chub are among the most acid-tolerant freshwater fish in the Northeast — a native species with wide physiological tolerance — yet even their signal is singular. No salmonids, no dace, no sucker. These are all native Maine brook fish that should occupy this habitat type; their complete absence is the impairment signal.

The algae tell the same story independently. Pennate diatoms dominate (35.4%) — genera like *Eunotia* and *Pinnularia* are classic acid-indicator taxa, well-documented as preferring pH below 6. Carteria green alga (17.4%) and *Chlamydomonas nivalis* (5.9%) are acid-tolerant flagellates that persist where most phytoplankton cannot compete. Euglena (3.5%) — an organic-enrichment tolerant and low-pH survivor — rounds out what ecologists call the acid-specialist guild. This is the community that remains after acidic filtering has removed more sensitive taxa.

That H(a) = 3.28 still registers meaningful algal diversity reflects the higher physiological tolerance of algae compared to vertebrates. At pH 3.54, algae survived the filter that eliminated the fish.

### Native vs. Non-Native
Creek Chub (*Semotilus atromaculatus*) is fully native to Maine. Its sole presence is not a stocking artifact — it is a natural acid-tolerance winner in a chemically hostile environment. All the absent species (Brook Trout, Blacknose Dace, White Sucker) are also native; their absence is the impairment story.

**The source of impairment at McCoy Brook is identified: Worcester Peat Mining.**

An active industrial peat extraction operation upstream — Worcester Peat Mining — has been operating for well over a decade and is the primary anthropogenic driver of the pH 3.54 condition documented here. This is not a speculative attribution. Peat mining directly exposes and destabilizes deep peat deposits, releasing sulfuric compounds, organic acids (fulvic and humic acid), and iron-sulfide oxidation products into drainage water. When disturbed peat is exposed to oxygen, pyrite (FeS₂) within the peat oxidizes to sulfuric acid — a process that continues for years and is extremely difficult to arrest once initiated. The resulting drainage is strongly acidic, metal-laden, and persistent.

The scale and duration of the operation — significant, pervasive, and active for more than a decade — means this is not a transitional or reversible condition under current management. The biological community at McCoy Brook reflects chronic, ongoing chemical impairment from an identified point-adjacent source, not background natural peat acidity or recoverable atmospheric acid deposition legacy.

**This distinction matters enormously for restoration.** A stream impaired by legacy acid rain soil depletion can recover passively over decades as acid deposition declines and soils slowly recharge. A stream receiving active drainage from an operating peat mining operation cannot recover until the source is managed or remediated. The Creek Chub at McCoy Brook is not holding a position that will be reclaimed by Brook Trout and Blacknose Dace on its own — it is occupying a stream that is being continuously re-impaired by upstream industrial activity.

The acid rain context remains relevant as a background amplifier: Washington County's granite-bedrock soils have low natural buffering capacity, and decades of mid-20th century acid deposition further depleted their base-cation reserves (calcium, magnesium). This means even moderate peat mining drainage — which might be partially buffered in a limestone-watershed stream — passes through McCoy Brook's watershed with minimal attenuation, reaching the stream at near-raw acidity. The two stressors compound each other. But Worcester Peat Mining is the active, manageable driver. It is the appropriate focus of any remediation or regulatory response.

---

## Crotch Camp Brook | JVB5776 / CNTLVPX4.1
**Fish: 9 species, H(f) = 1.69 | Algae: 76 ESVs, H(a) = 2.30**

### Sentinel Signal
*Synura* spp. at 75.9% dominance + *Salvelinus* spp. (Brook Trout) present = **phosphorus-limited oligotrophic soft-water system, not impaired but at the nutrient floor**. The Synura says dissolved phosphorus is near or below 10 μg/L and the water is clean and lean; the trout says it is still livable. Of 19 Synura ESVs detected, one resolves to species level: ***Synura truttae*** — a colonial chrysophyte named for *Salmo trutta* (Brown Trout), first described from cold Scottish trout streams. Its presence here alongside Brook Trout at pH 5.17 is ecologically coherent and taxonomically notable.

### Measured & Inferred Water Chemistry
| Parameter | Value | Source |
|---|---|---|
| **pH** | **5.17** | **Field measurement†** |
| **Temperature** | **41.1°F (5.1°C)** | **Field measurement** |
| Conductivity | <30 μS/cm | Inferred — Synurophyte dominance indicates very low ionic strength |
| Total phosphorus | <10 μg/L | Inferred — Synura outcompetes under P-limitation |
| Calcium | <5 mg/L | Inferred — soft water, granite/peat geology |
| Dissolved organic carbon | Moderate–high | Inferred — peatland drainage, humic tint |
| Dissolved oxygen | Good | Inferred — Brook Trout presence confirms aerobic conditions |

**pH 5.17 ecological significance:** Below the approximate threshold (≈5.5) where Brook Trout egg and fry survival becomes impaired. Adult Brook Trout are detected at 16.9% — they persist in this water — but successful in-stream reproduction at this pH is uncertain. The population may be sustained by adults moving in from less acidic reaches rather than by resident spawning. The measured pH is consistent with *Synura*-dominated soft water (optimal range 5.0–7.0) and confirms the biologically inferred character of the system.

### Narrative
The algal signal is the most ecologically diagnostic in the Maine dataset: *Synura* spp. (Colonial Synurophyte) accounts for 75.9% of all algal reads across 19 ESVs. Synurophytes are golden-brown flagellates that thrive in soft, slightly acidic water, low conductivity, and very low phosphorus. Their mass dominance here does not indicate impairment — it indicates a system at the extreme low end of phosphorus and nitrogen availability. Synurophytes are competitively dominant specifically when total dissolved phosphorus (TP) is below approximately 10 μg/L and dissolved inorganic nitrogen (DIN) is below 0.1–0.2 mg/L — concentrations too low to sustain fast-growing green algae or diatoms. The water is probably clear but humic-tinted, with conductivity near the detection limit of most field meters. H(a) = 2.30 is second-lowest in the dataset, not because conditions are toxic, but because *Synura* has outcompeted everything else in this phosphorus- and nitrogen-starved niche.

Of the 19 Synura ESVs detected at this site, only one resolves to species level: ***Synura truttae*** (591 reads, 1.46% of total library). This species was first described from oligotrophic, slightly acidic Scottish streams where *Salmo trutta* (Brown Trout) is the defining vertebrate — its specific epithet literally means "of the trout." Its occurrence here at pH 5.17 alongside *Salvelinus fontinalis* (Brook Trout) is exactly the ecological context for which the species was named. *Synura truttae* is diagnostic of clean, cold, soft, low-phosphorus water — its presence is a molecular confirmation of what the field pH and the fish community already indicate. The remaining 18 Synura ESVs resolve only to genus level (*Synura* spp.), but the community as a whole tells the same story.

The fish community is moderate and ecologically coherent for this habitat type: Ninespine Stickleback (35.2%), Creek Chub (25.0%), *Salvelinus* spp. — Brook Trout (16.9%), Redbreast Sunfish (9.9%). Brook Trout presence is the key signal — salmonids require cool, well-oxygenated, clean water. Their detection here confirms the system is not lethal; it is simply lean. H(f) = 1.69 with 9 species is consistent with a small, phosphorus-limited woodland brook: when TP is at or below 10 μg/L, algal growth is slow, invertebrate biomass is low, and the fish community supported above it is correspondingly modest in size and diversity.

### Native vs. Non-Native
All detected fish are native to Maine. Finescale Dace and Ninespine Stickleback, though not detected here at high abundance, are native soft-water specialists. The *Salvelinus* spp. signal reflects wild Brook Trout (*Salvelinus fontinalis*) — Maine's native salmonid — rather than stocked fish, given the remote, soft-water character of the site.

Combined: Crotch Camp Brook is not impaired. It is at the productive floor of what Maine geology naturally allows. The trout are there; they are just working hard for relatively little food.

---

## UNT Lane Rd | JVB5776 / CNR7WZYJ.1
**Fish: 1 species, H(f) = 0.00 | Algae: 77 ESVs, H(a) = 3.16**

### Sentinel Signal
American Eel alone + **measured pH 3.73** = **acute acid exclusion of fish community**. The single-species result is not a sampling artifact — it is a direct consequence of water chemistry that is lethal or excludes all fish except the most acid-tolerant. This site requires investigation for acidification source.

### Measured & Inferred Water Chemistry
| Parameter | Value | Source |
|---|---|---|
| **pH** | **3.73** | **Field measurement†** |
| **Temperature** | **41.1°F (5.1°C)** | **Field measurement** |
| Conductivity | 20–50 μS/cm | Inferred — soft, low-ionic water |
| Dissolved organic carbon | High | Inferred — humic acids consistent with bog/peatland drainage |
| Dissolved oxygen | Adequate for eel | Inferred — American Eel present |

### Narrative
pH 3.73 is at or below the threshold where most freshwater fish cannot survive: Brook Trout are excluded below approximately pH 4.5–5.0, most cyprinids below pH 5.5–6.0. (McCoy Brook, at pH 3.54, is more acidic still — the lowest field measurement in this dataset — but both sites sit well inside the zone of acute fish exclusion.) The single-species result at UNT (American Eel at 100%) is fully explained by chemistry: *Anguilla rostrata* is among the most acid-tolerant vertebrates in the northeastern freshwater system, capable of persisting in waters approaching pH 4.0 where all other species have been eliminated.

This pH is consistent with bog or ombrotrophic peatland drainage — ombrotrophic bogs in Maine commonly reach pH 3.5–4.5 from organic acid (humic/fulvic acid) accumulation. If UNT Lane Rd drains directly through or adjacent to a sphagnum bog, pH 3.73 could be entirely natural. However, acid atmospheric deposition (historical sulfur and nitrogen deposition) has permanently lowered baseline pH in some Washington County watersheds, and the interaction of naturally soft, low-buffering capacity water with decades of acid rain can produce chronic pH this low.

*Halamphora coffeaeformis* (14.9% of algal reads) is a database-assigned marine/brackish taxon that at this site almost certainly represents an acid-tolerant freshwater *Halamphora* species misassigned by the reference database — consistent with the inland location memory note. Acid-tolerant diatoms, Cryptophytes, and Chromulina can persist at pH 3.5–4.5, which explains why the algal community appears moderately diverse (H(a) = 3.16, 77 ESVs) despite chemistry that excludes virtually all fish. Algae are far more acid-tolerant than fish.

**Topographic analysis (10m NED DEM, Nov 2025):** UNT Lane Rd (44.740°N, -68.019°W, 55.2m elev.) lies on a continuous downhill slope from the Worcester Peat Mine direction to the northwest (74.7m). No ridge or drainage divide was identified between the mine area and UNT on this transect — water from the mine area is not topographically blocked from reaching UNT's drainage. However, McCoy Brook likely crosses the same slope between the mine and UNT; if McCoy's channel captures the mine drainage before it reaches UNT, UNT's acidity may instead reflect a natural ombrotrophic bog directly upstream. The pH values (McCoy 3.54, UNT 3.73) are similar enough to be consistent with either a shared influence or two independent bog-drainage systems. **Definitive source attribution requires field tracing (dye test or upstream chemistry transect at finer spatial resolution) — the topographic evidence is permissive but not conclusive.**

**Conservation significance:** Whether natural or mine-influenced, pH 3.73 is a permanent barrier to Brook Trout at this reach under current conditions. If mine-influenced: source management at Worcester Peat could improve conditions. If naturally acidic bog drainage: conditions are self-sustaining and Brook Trout recolonization of this specific reach is not achievable without active liming.

### Native vs. Non-Native
American Eel is fully native. Its catadromous life history and exceptional acid tolerance make it the last fish standing in severely acidified streams. Its detection here confirms open ocean connectivity but does not imply functional Brook Trout habitat.

---

## West Branch Narraguagus River @ Sprague's Falls | JVB5776 / CY92PPTX.1
**Fish: 14 species, H(f) = 1.94 | Algae: 201 ESVs, H(a) = 4.55 (highest in dataset)**

### Sentinel Signal
Finescale Dace + *Salvelinus* spp. (Brook Trout) + Sea Lamprey + diverse diatom matrix = **multi-line reference condition signal**. Each indicator independently confirms high-quality, connected, soft-water habitat functioning at full ecological complexity.

### Measured & Inferred Water Chemistry
| Parameter | Value | Source |
|---|---|---|
| **pH** | **5.09** | **Field measurement†** |
| **Temperature** | **44°F (6.7°C)** | **Field measurement** |
| Conductivity | 30–60 μS/cm | Inferred — soft-water fish guild; diverse diatoms |
| Total phosphorus | Low–moderate | Inferred — diverse but not cyanobacteria-dominated algae |
| Calcium | 3–8 mg/L | Inferred — soft, but adequate for dace and salmonids |
| Dissolved oxygen | High | Inferred — Brook Trout, Sea Lamprey, Finescale Dace all require high DO |
| Turbidity | Low | Inferred — diverse diatom community; no turbidity-tolerant taxa dominating |

**pH 5.09 ecological significance:** This is below the threshold (≈5.5) where Brook Trout reproductive success becomes impaired — eggs and fry are more sensitive than adults to low pH. Adults survive and are detected at 1.9%, but episodic acid pulses (spring snowmelt) can suppress recruitment. The measured pH is more acidic than the biologically inferred range of 5.5–6.5, suggesting either the November sampling date captured a low-pH pulse or the West Branch is chronically more acidic than the fish guild alone implies.

### Narrative
This is the reference condition for the watershed — the benchmark against which the other Maine sites should be read.

The algal community is the most diverse in the entire dataset: 201 distinct ESVs, H(a) = 4.55. This is not driven by a single dominant group but by a broad, even distribution across taxa — Halamphora diatom (11%), Pennate Diatoms (8.7%), Araphid Diatoms (8%), Monomastix (7.7%), Synurophytes (4.4%), and many more. A diverse, evenly distributed algal matrix indicates physical and chemical heterogeneity: riffles, pools, varying light, stable moderate nutrients, intact riparian cover. This is a complex, functioning aquatic ecosystem.

The fish community reflects that complexity: 14 species, H(f) = 1.94. Redbreast Sunfish (30.8%), a benthic omnivore requiring clean stable substrate. White Sucker (19.6%), a tolerant generalist indicating a system large enough to support body-mass fish. Ninespine Stickleback (10.2%) and Finescale Dace (7.3%), both characteristic of high-quality, slightly acidic, cool Maine streams. Sea Lamprey (0.3%) and *Salvelinus* spp. — Brook Trout (1.9%) confirm the site has ecological connectivity and thermal refugia.

Finescale Dace (*Chrosomus neogaeus*) deserve particular emphasis — they are considered sentinel indicators of pristine, soft-water habitat in Maine, strongly associated with wild Brook Trout streams. Their presence here is a quality endorsement independent of all other indicators.

### Native vs. Non-Native
All 14 detected fish species are native to Maine and to the Narraguagus watershed. Sea Lamprey, though often maligned for its role in the Great Lakes (where it is invasive), is fully native to the Atlantic coast of North America and an ecologically integral part of the Narraguagus system. Its detection confirms functioning migratory connectivity.

West Branch Narraguagus is what a healthy Maine woodland stream looks like. This is the ceiling — not an idealized target but an actually observed condition.

---

## Narraguagus Rt 193 / Jewett Landing | JVB5776 / CA66THTZ.1
**Fish: 19 species, H(f) = 2.16 (highest in ME) | Algae: 117 ESVs, H(a) = 3.86**

### Sentinel Signal
Alewife + Atlantic Salmon + Sea Lamprey + Fallfish = **four-line anadromous hub signal**: ocean connectivity confirmed, clean gravel confirmed, federally listed species present, marine nutrient subsidy active. The Cyanobacteria (6.5%) = **early nutrient enrichment watch flag** — not alarming, but noted.

### Measured & Inferred Water Chemistry
| Parameter | Value | Source |
|---|---|---|
| **pH** | **6.25** | **Field measurement†** |
| **Temperature** | **42.8°F (6.0°C)** | **Field measurement** |
| Conductivity | 40–80 μS/cm | Inferred — higher than tributaries; anadromous nutrient inputs |
| Total phosphorus | Low–moderate, trending up | Inferred — Cyanobacteria at 6.5% = early enrichment signal |
| Calcium | 5–12 mg/L | Inferred — adequate for full fish guild; Fallfish nest-building |
| Dissolved oxygen | High | Inferred — Atlantic Salmon, Fallfish both require high DO |
| Marine-derived nutrients | Present | Inferred — Alewife, Salmon, Lamprey decomposition subsidies |

### Narrative
This is the ecological hub of the Maine dataset — the most diverse fish community, the strongest anadromous signal, and the connecting node between the Gulf of Maine and the interior watershed.

The fish community tells the story immediately. Alewife (26.3%) is the dominant taxon — ocean fish that ascend rivers in spring to spawn. Their eDNA in November reflects residual signal from the spring migration or from juveniles still present. Either way, this is direct evidence of open corridor to the Gulf of Maine. Fallfish (22.2%) — the largest native minnow in the Northeast — require clean, gravel-bottomed streams for their distinctive large nest mounds. A strong Fallfish signal is a meaningful water quality indicator independent of any chemical measurement.

Atlantic Salmon (0.3%) and Sea Lamprey (0.3%) complete the anadromous sentinel suite. Trace levels, but ecologically significant: the Narraguagus supports one of the few remaining wild Atlantic Salmon populations in the United States, a federally endangered stock. Detection here is not incidental — it is confirmation that this stretch of river is part of an active salmon watershed.

The supporting cast — Redbreast Sunfish (12.7%), White Sucker (8.5%), Shiner sp. (5.1%), Pickerel/Pike sp. (3.6%), 19 species total — reflects a complete, multi-guild community from benthic feeders to apex predators. H(f) = 2.16 is the highest fish Shannon index in the Maine dataset.

The algae show a functional but different community from West Branch: Cryptophytes dominate (24.3%), indicating humic, moderately productive water. Centric Diatoms (10.7%) signal nutrient and silica availability appropriate for a mainstem or lower-gradient reach. Cyanobacteria at 6.5% — at this level, they are not alarming, but they are a flag. Cyanobacteria are favored by elevated nitrogen and phosphorus; their appearance here may reflect marine-derived nutrient subsidy from decomposing anadromous fish, which is natural and cyclical, but warrants monitoring to distinguish natural subsidies from anthropogenic enrichment.

### Native vs. Non-Native
All 19 fish species are native to their respective ecological roles in this watershed. Alewife, Atlantic Salmon, Sea Lamprey, and American Eel are all native anadromous or catadromous species with evolutionary relationships to this river system. There is no detectable non-native fish signal in the Maine dataset.

Narraguagus Rt 193 is functioning as a mainstem ecosystem hub. It is the healthiest and most connected site in the Maine sample.

---

## Maine Summary

| Site | Fish spp. | H(f) | Algae ESVs | H(a) | Key Sentinel Complex | Status |
|---|---|---|---|---|---|---|
| Narraguagus Rt 193 | 19 | 2.16 | 117 | 3.86 | Alewife + Atlantic Salmon + Fallfish | **Healthy — anadromous hub** |
| West Branch Narraguagus | 14 | 1.94 | 201 | 4.55 | Finescale Dace + Sea Lamprey + diverse diatoms | **Healthy — reference condition** |
| Crotch Camp Brook | 9 | 1.69 | 76 | 2.30 | Synura 74% + Trout sp. | Functional — phosphorus-limited oligotrophic floor |
| UNT Lane Rd | 1 | 0.00 | 77 | 3.16 | Eel only + adequate algae | Ambiguous — resample needed |
| McCoy Brook | 1 | 0.00 | 91 | 3.28 | Creek Chub + Eunotia + Euglena | **Impaired — pH 3.54 — Worcester Peat Mining** |

The Maine gradient runs from active impairment (McCoy Brook, pH 3.54) through oligotrophic soft-water limitation (Crotch Camp Brook) to full ecological function with anadromous connectivity (Narraguagus Rt 193, West Branch). Acidification is the primary stressor. All detected fish are native. Where chemistry is adequate and ocean connectivity is intact, the system assembles a complete, multi-guild native fish community on a complex algal foundation.

---

---

# MASSACHUSETTS — Manchester-by-the-Sea, MA | November 22, 2025

Manchester-by-the-Sea sits on the Essex County coast, underlain by glacial till over granite and gneiss. Proximity to the ocean, coastal vegetation, and groundwater from glacially deposited material mean water chemistry here can be harder, more mineral-rich, and more alkaline than the Deblois sites. All three MA sites drain into or near the tidal estuary of Sawmill Brook and Manchester Harbor. Tidal influence is the defining ecological force of this dataset.

---

## Upper Sawmill | JVB5776 / CVVU52A9.1
**Fish: 5 species, H(f) = 0.87 | Algae: 151 ESVs, H(a) = 4.20 | Date: unknown**

### Sentinel Signal
Golden Shiner + Sunfish sp. dominant + Cryptomonas + Mallomonas = **pond/impoundment signal, soft water, slightly acid to neutral, no tidal influence, no impairment**. Low fish H(f) reflects habitat type, not stress.

### Inferred Water Chemistry
| Parameter | Inferred value | Basis |
|---|---|---|
| pH | 5.5–6.5 | Cryptomonas + Mallomonas assemblage |
| Conductivity | 20–50 μS/cm | Soft water, cryptophyte/synurophyte indicators |
| Total phosphorus | Low–moderate | Productive enough for 151 ESVs, not eutrophic |
| Dissolved organic carbon | Moderate–high | Humic signal from cryptophytes and Mallomonas |
| Stratification | Likely seasonal | Cryptomonas competitive under stratified conditions |
| Salinity | Freshwater | No estuarine species in fish community |

### Narrative
The fish community — Golden Shiner (58.3%), Sunfish sp. (36.8%), Bass sp. (2.1%), American Eel (2.6%), Bullhead sp. (0.2%) — is definitively a warm-water, still-water assemblage. Golden Shiner and Sunfish are pond and backwater specialists. Their dominance indicates a lentic environment: a pond, reservoir, or slow-moving impoundment upstream of tidal influence. No estuarine species. No anadromous species except Eel. H(f) = 0.87 reflects the naturally limited fish diversity of a small pond, not chemical impairment.

The algal community is ecologically informative: H(a) = 4.20, 151 ESVs. Cryptomonas (26.1%) and *Cryptomonas obovoidea* (8.7%) — cryptophytes competitive in stratified, humic, slightly acidic conditions. Mallomonas (9.7%) — a scaled synurophyte indicating soft, slightly acidic, oligotrophic water. This is the algal community of a small softwater pond: productive enough to support 151 ESVs, but chemically soft and likely seasonally stratified.

### Native vs. Non-Native
American Eel is native. Golden Shiner (*Notemigonus crysoleucas*) is native to eastern North America but is a common pond-stocking species in Massachusetts — its dominance here may reflect artificial introduction rather than natural recruitment. Sunfish sp. and Bass sp. detections (likely Pumpkinseed or Bluegill; Largemouth Bass) are native to eastern NA but are routinely stocked in MA ponds. Bullhead sp. (likely Brown Bullhead, *Ameiurus nebulosus*) is native. The Eel's presence confirms that some downstream connectivity to tidal water exists even from this pond habitat.

---

## Below School St | JVB5776 / CDWD42KP.1
**Fish: 9 species, H(f) = 1.40 | Algae: 178 ESVs, H(a) = 4.43 (second highest in dataset)**

### Sentinel Signal
Mummichog + Fourspine Stickleback + American Eel + estuarine diatoms = **tidal freshwater-to-oligohaline transition, fully functional, native coastal assemblage**. This two-species sentinel pair (Mummichog + Fourspine Stickleback) alone defines the habitat type unambiguously.

### Inferred Water Chemistry
| Parameter | Inferred value | Basis |
|---|---|---|
| pH | 6.5–7.5 | Tidal influence; diatom-rich community |
| Salinity | 0.5–5 ppt (tidal cycles) | Mummichog + Fourspine Stickleback co-dominance |
| Conductivity | 100–500 μS/cm (variable) | Tidal mixing with marine water |
| Total phosphorus | Moderate | Tidal nutrient flux; high diatom diversity |
| Silica | Moderate–high | Diatoms 23% of algal community |
| Dissolved oxygen | Variable but adequate | Tidal mixing maintains oxygenation |
| Turbidity | Moderate | Tidal resuspension; cryptophytes competitive |

### Narrative
The fish community names this site's character plainly: Mummichog (42.1%), Fourspine Stickleback (31.6%), American Eel (15.6%).

Mummichog (*Fundulus heteroclitus*) is the quintessential salt marsh and tidal creek fish of the northeast coast — native, tolerant of salinity from fresh to full seawater, and adapted to the biological extremes of tidal dynamics. Fourspine Stickleback (*Apeltes quadracus*) is a brackish-water specialist found throughout coastal New England tidal creeks. These two species together define the tidal freshwater-to-oligohaline transition zone with a specificity that no chemical measurement could better. American Eel confirms ocean connectivity. White Perch (5.3%) — a euryhaline native of coastal New England — reinforces the estuarine character.

The algal community is the second most diverse in the entire dataset: 178 ESVs, H(a) = 4.43. Tidal systems receive regular nutrient pulses from marine water, decomposing organic matter, and sediment resuspension — conditions that support high algal diversity. Diatoms (23.1%) are classic estuarine primary producers, renewed by tidal flux of silica, nitrogen, and phosphorus. Cryptomonas (22.0%) is competitive in the low-light, mixed-salinity conditions of a tidal fringe.

### Native vs. Non-Native
All detected fish are native to the coastal New England estuarine environment. Mummichog, Fourspine Stickleback, White Perch, and American Eel are among the most characteristic native species of this habitat type. There is no non-native fish signal at this site.

Below School St is a functioning tidal transition ecosystem. This is what a healthy coastal tidal reach looks like in late November.

---

## Lower Golf Course / Sawmill Brook | JVB5776 / C4SUMTFY.1
**Fish: 9 species, H(f) = 1.62 | Algae: 140 ESVs, H(a) = 3.57**

### Sentinel Signal
Charophytes (Stonewort class) at 35% + Mummichog/Fourspine Stickleback + Golden Shiner/Sunfish = **ecotone signal: calcium-rich clean groundwater input meeting tidal backwater**. The Charophyte signal is ecologically significant — but **genus was not resolved in the 23S rRNA data**, and in-situ verification is required before species identity and invasive status can be confirmed (see note below).

### Inferred Water Chemistry
| Parameter | Inferred value | Basis |
|---|---|---|
| pH | 6.5–8.0 | Stonewort optimal range; alkaline to neutral |
| Calcium | >15–20 mg/L | Stoneworts require Ca²⁺ for cell wall calcification |
| Conductivity | 80–200 μS/cm | Harder than ME sites; groundwater + tidal mix |
| Total phosphorus | Low–moderate | Stoneworts outcompeted by phytoplankton above ~20 μg/L TP |
| Turbidity | Low | Stoneworts cannot photosynthesize in turbid water |
| Salinity | 0–5 ppt (variable) | Estuarine fish present; freshwater lens from groundwater |
| Groundwater input | Significant | Only explanation for Ca-rich signal at tidal interface |

### Narrative
This is the most ecologically complex and most ecologically hopeful site in the Massachusetts dataset.

The fish community straddles two worlds: Fourspine Stickleback (32.4%) and Mummichog (8.5%) signal tidal/estuarine influence; Golden Shiner (14.9%) and Sunfish sp. (24.5%) are freshwater warm-water taxa. American Eel (17.3%) bridges both. Rainbow Smelt (0.2%) and Yellow Perch (1.4%) add coastal connectivity and tolerant generalist presence. This is a mixing zone — freshwater meeting tidal backwater — and the fish community reflects that ecotone exactly. Ecotones are often biodiversity hotspots precisely because they receive inputs from both adjacent systems simultaneously. H(f) = 1.62 is the highest in the Massachusetts dataset.

The algal signal here is the most striking in the Massachusetts data, and arguably the most important single finding in the batch: **Charophytes (Stoneworts) at 35.0%**.

Stoneworts (*Chara*, *Nitella*, and related genera) are macrophytic charophytes — structurally complex plants that anchor to the substrate in shallow, clear, well-lit water. They are exquisitely sensitive to conditions:

- **Water clarity**: Stoneworts cannot photosynthesize in turbid water. Their dominance means low suspended sediment and good light penetration to the substrate.
- **Calcium**: Stoneworts require calcium to build their calcareous cell walls and encrustations. Their 35% dominance at this site signals Ca²⁺ concentrations well above what the granite-derived Maine sites could support — almost certainly a groundwater or spring input.
- **pH**: Stoneworts grow optimally between pH 6.5 and 8.0. This is alkaline relative to the Maine watershed and to the MA soft-water pond site upstream.
- **Nutrient status**: Stoneworts are outcompeted by filamentous algae and cyanobacteria under nutrient-enriched conditions. Their dominance here indicates oligotrophic to mesotrophic, unimpaired water quality.
- **Habitat value**: Stonewort beds are structural aquatic habitat — fish and invertebrates use them for cover, spawning substrate, and foraging.

A 35% Charophyte signal at a tidal interface site in a developed coastal town is ecologically significant regardless of species identity — it confirms calcium-rich, clear, low-turbidity groundwater input that is maintaining conditions suitable for a sensitive, structurally complex aquatic macrophyte against the backdrop of development pressure and tidal dynamics.

**Critical caveat — invasive species risk.** The 23S rRNA data resolved this signal to class (Charophyceae) but not to genus. Native *Chara* and *Nitella* — clean-water indicators — and **Starry Stonewort (*Nitellopsis obtusa*)** — an invasive charophyte spreading rapidly through the northeastern US from Great Lakes origin — are **both Charophyceae and cannot be distinguished in this dataset**. Starry Stonewort thrives in exactly these conditions: calcium-rich, clear, hard water. It is now documented in Vermont and New York and is actively expanding toward Massachusetts. The conditions at Golf Course/Sawmill Brook are permissive for both the native and the invasive. **In-situ morphological identification or targeted species-specific PCR is required before this signal can be confidently interpreted as native or invasive.** This is not a minor footnote — if *Nitellopsis obtusa* is established here, it is a management priority, not a positive indicator.

### Native vs. Non-Native
All detected fish species are native to eastern North America in this habitat type. Golden Shiner and Sunfish spp. may reflect upstream pond stocking, but they are native species. Fourspine Stickleback, Mummichog, American Eel, Rainbow Smelt, and Yellow Perch are all wild, native coastal New England fish. No non-native fish signal detected.

Lower Golf Course / Sawmill Brook sits at the intersection of productive tidal ecology and a clean, calcium-rich freshwater input. The Charophyte signal is the most ecologically complex finding in the Massachusetts dataset — and its true character (native indicator vs. invasive alert) is the most important unanswered question in the batch. It warrants immediate field verification.

---

## Massachusetts Summary

| Site | Fish spp. | H(f) | Algae ESVs | H(a) | Key Sentinel Complex | Character |
|---|---|---|---|---|---|---|
| Lower Golf Course / Sawmill | 9 | 1.62 | 140 | 3.57 | Stoneworts 35% + estuarine-freshwater ecotone fish | **Ecotone — Ca-rich groundwater meets tidal** |
| Below School St | 9 | 1.40 | 178 | 4.43 | Mummichog + Fourspine Stickleback + estuarine diatoms | **Tidal transition — fully functional** |
| Upper Sawmill | 5 | 0.87 | 151 | 4.20 | Golden Shiner + Cryptomonas + Mallomonas | Pond habitat — soft water, not impaired |

No impairment signals in Manchester-by-the-Sea. The three sites represent a downstream gradient from soft-water pond to tidal transition, with the ecotone at Golf Course/Sawmill Brook the most ecologically complex and most conservation-valuable of the three.

---

---

# The Combined Story: What Algae and Fish Together Tell Us

## 1. Water Chemistry Written in Biology

The Maine sites are soft, acidic, low-mineral systems — a product of granite bedrock, peat drainage, and low atmospheric buffering capacity. The algal indicators confirm this across every site: Synura dominance at Crotch Camp Brook (soft oligotrophic floor), acid-specialist Eunotia/Pennate Diatom/Euglena guild at McCoy Brook (acid impairment), Cryptophyte/Chrysophyte assemblages at UNT Lane Rd and Narraguagus (moderate humic soft water). Where pH collapses to 3.54, the fish community collapses to one species and the algal community reorganizes around acid-tolerant survivors. Where pH is more moderate — even in soft, mineral-poor water — salmonids, native dace, and sticklebacks assemble above a diverse algal base.

The Massachusetts sites show harder, more alkaline, more mineral-rich conditions. The difference between soft-water Upper Sawmill (Cryptophyte-dominated) and groundwater-influenced Golf Course/Sawmill (Stonewort-dominated) is the difference between water that has moved through glacial till and water that has moved through calcium-bearing glacial deposits — a mineralogical distinction captured precisely in the algal community.

## 2. Sentinel Pairs and Triplets: The Compressed Story

The most powerful ecological statements in this dataset are made by combinations of two or three independent indicators pointing to the same conclusion:

- **McCoy Brook**: Creek Chub only + Eunotia/Pennate Diatoms + Euglena = acid impairment, three independent lines
- **West Branch Narraguagus**: Finescale Dace + Sea Lamprey + diverse diatom matrix = reference condition, three independent lines
- **Narraguagus Rt 193**: Alewife + Atlantic Salmon + Fallfish + Cyanobacteria flag = functional anadromous hub with early nutrient watch, four lines
- **Golf Course/Sawmill**: Stoneworts (35%) + Mummichog/Stickleback + Golden Shiner = Ca-rich groundwater ecotone, three independent lines
- **Below School St**: Mummichog + Fourspine Stickleback + estuarine diatoms = tidal transition, unambiguous

These combinations are more reliable than any single indicator. Each sentinel adds a statistically independent line of evidence converging on the same ecological conclusion.

## 3. The Mineral Story: Calcium, Aluminum, Silica, and Phosphorus

Minerals are the language the algae speak most directly. Where the fish tell us whether a system is livable, the algal community tells us what the water is made of — what dissolved ions are present, what is limiting, and what is harmful. Across this dataset, four elements do most of the ecological work.

**Calcium (Ca²⁺) — the architect mineral.** Calcium is required for cell wall construction, osmoregulation, nerve function, and shell and scale formation. In soft-water Maine systems, calcium is naturally low — typically 1–8 mg/L — and everything is adapted to scarcity. The ecological gradient from Maine to Massachusetts is partly a calcium gradient: the Narraguagus granite watershed delivers almost none; the glacial till of Manchester-by-the-Sea delivers more; the groundwater feeding Golf Course/Sawmill Brook delivers enough to support Stoneworts, which require >15 mg/L Ca²⁺ to build their calcareous cell walls. Stonewort presence is therefore a direct biological calcium measurement — more reliable in some ways than a spot chemical sample.

At McCoy Brook (pH 3.54), calcium has been stripped from the water column by the acid itself — at pH <4, Ca²⁺ is driven out of solution and aluminum replaces it as the dominant cation. Fish exposed to this water cannot regulate calcium across their gill membranes. This is one of several mechanisms by which acid pH kills fish; it is not simply that the water is "acidic" — it is that the ionic environment required to maintain fish physiology has been chemically dismantled.

**Aluminum (Al³⁺) — the acid-mobilized toxin.** Aluminum is the most abundant metal in the earth's crust, locked harmlessly in silicate minerals under neutral conditions. Below pH 5.0, aluminum is mobilized into solution in its toxic ionic form (Al³⁺). At pH 3.54, dissolved aluminum concentrations at McCoy Brook are almost certainly elevated — potentially in the range of hundreds of μg/L, well above the chronic toxicity threshold for fish gills (~50–100 μg/L). Aluminum precipitates as Al(OH)₃ on gill surfaces at the mixing zone between acid stream water and the circumneutral blood pH of a fish, physically clogging gas exchange. Creek Chub's survival at this site likely reflects a combination of behavioural avoidance and moderate physiological tolerance — but aluminum toxicity, not just pH per se, is part of why the community collapsed to a single species.

**Silica (SiO₂) — the diatom currency.** Diatoms build their intricate glass frustules (cell walls) from dissolved silica. Their abundance in the algal community is therefore partly a proxy for silica availability — which tracks nutrient dynamics and water source. The diverse diatom communities at West Branch Narraguagus (Pennate + Araphid types, 8.7–11% of reads), Narraguagus Rt 193 (Centric Diatoms 10.7%), and Below School St (Diatoms 23.1%) all signal adequate silica delivery — either from mineral weathering in the watershed or from tidal marine flux. At McCoy Brook, even though diatoms are present (Pennate Diatoms 35.4%), the community is acid-specialist genera only (*Eunotia*, *Pinnularia*) rather than the diverse, productive diatom matrix seen at reference sites. Silica is not limiting at McCoy Brook — but everything else is.

**Phosphorus (P) — the primary limiting nutrient, and why it becomes limiting.** Phosphorus is the nutrient that limits algal growth in virtually all freshwater systems — not because it is rare on Earth, but because it has no atmospheric reservoir. Nitrogen is abundant in the air (78% of the atmosphere) and reaches watersheds continuously via rainfall, nitrogen fixation, and decomposition. Phosphorus does not. It enters water only by the slow chemical weathering of phosphate minerals in bedrock and soil, or from decomposition of organic matter, agricultural runoff, or wastewater. In the Narraguagus watershed — granite and peat, thinly soiled, heavily leached — there are almost no phosphate minerals to weather, and acid rain has further stripped the soil's ability to retain and cycle nutrients. The result is that dissolved phosphorus in the water is chronically scarce. When algae consume available P and it is not replenished, growth stops. The community that persists under those conditions — Synura at Crotch Camp Brook — is the one that evolved to compete for P at concentrations too low for faster-growing competitors. This is not artificial scarcity; it is the natural condition of granite soft-water watersheds in the Northeast.

The Synura-dominated community at Crotch Camp Brook signals total dissolved phosphorus likely below 10 μg/L. The cryptophyte-dominated MA pond sites signal slightly higher P — enough to support 150+ ESVs but not enough to trigger cyanobacteria blooms. The Cyanobacteria signal at Narraguagus Rt 193 (6.5%) is the one site where P may be trending upward — from marine-derived nutrient subsidy from decomposing anadromous fish carcasses, which is natural and cyclical, but worth monitoring if it increases with changing land use. Stonewort dominance at Golf Course/Sawmill Brook signals P low enough that Stoneworts can outcompete phytoplankton for substrate and light — estimated <20 μg/L TP, consistent with clean groundwater input.

**The mineral hierarchy across sites:**

| Site | Ca²⁺ signal | Al³⁺ risk | Silica | Phosphorus |
|---|---|---|---|---|
| McCoy Brook | Depleted by acid | High (pH 3.54) | Present but acid-filtered | Low |
| Crotch Camp Brook | Very low (<5 mg/L) | Low | Present | Very low (<10 μg/L) |
| UNT Lane Rd | Low | Low | Present | Low–moderate |
| West Branch Narraguagus | Low–moderate | Negligible | Adequate | Low–moderate |
| Narraguagus Rt 193 | Moderate | Negligible | Adequate | Low–moderate; trending (Cyano flag) |
| Upper Sawmill MA | Low | Negligible | Present | Low–moderate |
| Below School St MA | Moderate (tidal) | Negligible | High (tidal flux) | Moderate |
| Golf Course/Sawmill MA | High (>15 mg/L est.) | Negligible | Moderate | Low (<20 μg/L est.) |

The single most important mineral story in this dataset is the **calcium gradient from McCoy Brook (Ca stripped by acid, Al toxic) to Golf Course/Sawmill (Ca-rich, clean groundwater, Stoneworts thriving)**. That gradient, inferred entirely from biology, spans what would require a full suite of chemical analyses to measure directly.

---

## 4. Algae Drive the System

Primary production sets the ceiling on everything above it. Phosphorus-limited (TP <10 μg/L), Synura-dominated Crotch Camp Brook supports moderate fish diversity at best — with dissolved P near the biological minimum, primary production is too slow to fuel the invertebrate biomass a richer fish community would require. Algal-rich, ESV-diverse West Branch Narraguagus supports 14 fish species. Tidal-nutrient-subsidized Below School St generates 178 algal ESVs and a structurally complete coastal fish community.

The relationship is not coincidental. Algal diversity → invertebrate diversity → food web complexity → fish diversity. The eDNA is capturing the base and the apex simultaneously, and they tell coherent, consistent stories.

## 4. Native Species Integrity — The Most Important Finding Nobody Mentions

In degraded freshwater systems across the Northeast, the usual story is: native species reduced or gone, replaced by tolerant generalists or outright invasives — Brown Trout stocked over Brook Trout habitat, Largemouth Bass established in warmwater ponds over native Pickerel, Common Carp restructuring benthic ecology, Green Crab dismantling tidal invertebrate communities, Phragmites filling salt marsh. That is the baseline expectation for developed landscapes in 2025.

This dataset tells a different story. **Every fish detected in the Maine sites is native to the Narraguagus watershed.** Every fish detected in the Massachusetts tidal sites is native to coastal New England estuaries. The ecological framework — the community structure that took thousands of years to assemble — is still in place.

This is not a given. It is a finding.

### What was detected, and what it means

**Common invasive fish not detected in Maine:**
| Species | Why it matters if absent |
|---|---|
| Brown Trout (*Salmo trutta*) | European; heavily stocked in ME; outcompetes and hybridizes with native Brook Trout (*Salvelinus fontinalis*) |
| Rainbow Trout (*Oncorhynchus mykiss*) | Pacific; stocked across ME; cannot reproduce in most ME streams but competes seasonally |
| Smallmouth Bass (*Micropterus dolomieu*) | Native to interior NA but introduced to ME lake systems; predator of native juvenile salmon and trout |
| Common Carp (*Cyprinus carpio*) | European; root-feeding restructures benthic habitat; elevates turbidity; absent here |
| Chain Pickerel (*Esox niger*) | Native, but its detection would flag warmwater pond conditions in cold-water stream sites |

None of these appear in the Maine eDNA signal. The Trout sp. detection at Crotch Camp Brook and West Branch Narraguagus most likely reflects wild native Brook Trout — the species that belongs there — rather than hatchery stock, based on the remote, soft-water, cold character of those sites.

**Common invasive fish not detected in MA tidal sites:**
| Species | Why it matters if absent |
|---|---|
| Common Carp (*Cyprinus carpio*) | Absent from tidal sites despite heavy presence in many MA coastal impoundments |
| Green Sunfish (*Lepomis cyanellus*) | Aggressive invasive in MA warmwater systems; not detected |
| Northern Snakehead (*Channa argus*) | Expanding in MA and CT; not detected |
| Rusty Crayfish | Not a fish but restructures benthic invertebrate communities; no signal |

Non-aquatic incidental detections in the raw 12S panel are filtered from all analysis and are not discussed here.

### The Native Species Significance, Site by Site

**Maine:**
- **McCoy Brook**: The *only* fish detected is Creek Chub — native. The species that is absent (Brook Trout, Blacknose Dace, White Sucker) are also all native. The impairment is chemical, not biological restructuring by invasives. The community could recover if the chemistry is addressed. An invasive-restructured community would be far harder to restore.
- **Crotch Camp Brook**: All 9 species native. Trout sp. likely wild Brook Trout in a remote, phosphorus-limited system — not stocked, not invasive. This is a native cold-water fish community operating below its potential due to natural nutrient limitation, not human-caused biological disruption.
- **West Branch Narraguagus**: All 14 species native. Finescale Dace — a species that co-evolved with Brook Trout in Maine's acidic soft-water landscape — is present. Sea Lamprey — native to the Atlantic coast, ecologically integral to this watershed system — confirmed. This is a reference-condition native community.
- **Narraguagus Rt 193**: All 19 species native, including three federally significant anadromous species (Atlantic Salmon, Alewife, Sea Lamprey). The Narraguagus is one of the last watersheds in the US supporting a wild Atlantic Salmon population. The eDNA confirms the biological infrastructure of that population — the run corridor — is functioning.

**Massachusetts:**
- **Upper Sawmill**: The warmwater pond fish (Golden Shiner, Sunfish, Bass, Bullhead) are native to eastern North America but are routinely stocked in Massachusetts ponds. **Their presence here may reflect stocking, not natural wild recruitment.** This is the one site where native status is nuanced — the species are native, but their origin at this specific location may be artificial. Importantly, there is no signal of truly invasive non-native species (Carp, Snakehead, Green Sunfish). The ecological disruption, if any, is from stocking of native species outside their naturally colonized range — a subtle but real distinction.
- **Below School St**: All detected species (Mummichog, Fourspine Stickleback, American Eel, White Perch) are wild native coastal species. This is the fish community that should be at a functioning tidal transition site in coastal New England. No invasive signal.
- **Golf Course/Sawmill Brook**: The freshwater component (Golden Shiner, Sunfish) may include stocked fish as at Upper Sawmill, but the tidal component (Mummichog, Fourspine Stickleback, American Eel, Rainbow Smelt) is entirely native wild species. The Stonewort algal community is likewise native — *Chara* and *Nitella* are indigenous to northeastern North America and are sensitive enough that invasive Phragmites or cyanobacterial blooms would displace them. Their dominance at 35% is therefore a double signal: not only is the water chemistry good, but the biological community has not been restructured by invasion.

### What Native Integrity Tells Us About These Systems

A fully native fish community means the ecological relationships — predator-prey, competition, spawning habitat use, invertebrate food web — are still assembled as they were before European settlement modified the landscape. The system can self-organize. It has the biological memory of how to function.

When impairment is present (McCoy Brook) but the cause is chemical rather than biological invasion, restoration is conceptually straightforward: address the pH source, and the native community has the potential to recolonize from connected upstream and downstream refugia. The biological template still exists in the watershed.

When non-native species dominate — as in many New England warmwater ponds and coastal wetlands — restoration requires not just chemistry correction but active removal of established invaders and reintroduction of native species from remnant populations. That is orders of magnitude harder.

The native integrity documented here is one of the most conservation-relevant findings in the dataset. It should be protected explicitly — through barrier removal to support diadromous species, through monitoring for invasive introduction, and through land-use management that maintains the water chemistry conditions native species require.

## 5. Connectivity Is the Wild Card

American Eel detected at six of eight sites confirms ocean connectivity runs through most of this landscape. On the Narraguagus, Alewife, Atlantic Salmon, and Sea Lamprey amplify that signal dramatically. Anadromous fish carry marine-derived nutrients into freshwater when they spawn and decompose — a subsidy from the ocean to the watershed, measurable in the Cyanobacteria signal at Narraguagus Rt 193. Sites with strong anadromous signals tend to support richer fish communities; this dataset supports that pattern.

## 6. The Impairment Signal and What Could Be

McCoy Brook stands alone. pH 3.54 is not a background condition and it is not ambiguous in its source — **Worcester Peat Mining**, an active upstream industrial peat extraction operation running for more than a decade, is the identified driver. This is an anthropogenic impairment with a known, specific, manageable cause. The biological evidence — Creek Chub sole survivor, Eunotia/Pennate Diatom acid guild, Euglena — is unambiguous and triply confirmed. The stream that should support Brook Trout, Blacknose Dace, and White Sucker cannot do so while the upstream drainage continues unchecked.

UNT Lane Rd warrants follow-up. The eel-only fish signal with adequate algal diversity does not fit either the impairment pattern or the reference condition pattern. Seasonal resampling in spring or early summer would resolve the question.

The Narraguagus watershed at its best — Rt 193 and West Branch — shows what these systems are capable of when chemistry is adequate and ocean connectivity is intact: 14–19 native fish species, traces of wild Atlantic Salmon and Sea Lamprey, the most complex algal communities in the dataset. Manchester-by-the-Sea shows a tidal system under moderate development pressure that still supports Stoneworts, Mummichog, Fourspine Stickleback, and 150+ algal ESVs at each site.

The ecological architecture is intact. It is worth protecting.

---

*Batch JVB5776 | 23S rRNA (algae) + MiFish 12S rRNA (fish) | Analyzed April 2027*
*Data only. All interpretations are based solely on measured eDNA read abundances in this dataset. Inferred water chemistry parameters are biological estimates, not direct measurements.*
