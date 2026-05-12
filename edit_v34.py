"""
v34 — Move all taxonomic and QC hand-waving to a proper Taxonomic & QC Notes appendix.

[T1] MiFish 12S barcode limits (genus-level ceiling)
[T2] Esox spp. / Esox lucius database artifact
[T3] Longear Sunfish database artifact
[T4] Fundulus parvipinnis database artifact
[T5] Cormorant fecal eDNA
[T6] Charophyte / Nitellopsis invasive uncertainty
[T7] eDNA tidal degradation
[T8] Read count reliability
[T9] Rainbow Smelt Golf Course anomaly
"""

import re, subprocess

SRC = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v33.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v34.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v34.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# ── T8 — Read count reliability ───────────────────────────────────────────────
text = text.replace(
    '**Read counts** are proportional, not absolute — they are literal counts of distinct DNA molecules. A species at 1% with 10,000 total reads (100 reads) is more reliable than a species at 1% with 500 total reads (5 reads). <!-- PENDING: Add footnote on read count thresholds and reliability -->',
    '**Read counts** are proportional, not absolute [T8].'
)

# ── T2 — Esox: Sentinel Species table ────────────────────────────────────────
text = text.replace(
    '| ***Esox* spp.** (*niger*/*americanus*) | Native pickerel — 100% ESV match | Chain Pickerel or Redfin Pickerel; MiFish 12S cannot distinguish the two<!-- PENDING: ESV footnote - ESV_010000 100% native pickerel across all batches; E. lucius assignment is database artifact --> |',
    '| ***Esox* spp.** | Native pickerel — 100% ESV match | *E. niger* or *E. americanus*; species-level unresolvable from this barcode [T2] |'
)

# ── T6 — Charophyte: Sentinel Species table ───────────────────────────────────
text = text.replace(
    '| **Charophytes (Stoneworts)** | Calcium-rich, clear, low-turbidity groundwater input | Cannot distinguish native *Chara/Nitella* from invasive *Nitellopsis* without field ID |',
    '| **Charophytes (Stoneworts)** | Calcium-rich, clear, low-turbidity groundwater input | Field ID required — invasive *Nitellopsis obtusa* cannot be ruled out [T6] |'
)

# ── T2 — Esox: MBTS intro paragraph ──────────────────────────────────────────
text = text.replace(
    '***Esox* spp. (database: *Esox lucius*) detected at Second Pond (October 2024) — QC flag: likely native Chain or Redfin Pickerel; MiFish 12S cannot reliably distinguish *Esox lucius* from native pickerel. Verify by electrofishing before reporting as illegal stocking.**',
    '***Esox* spp. detected at Second Pond (October 2024) — native pickerel; *Esox lucius* database assignment is an artifact [T2].**'
)

# ── T7 — Tidal eDNA degradation ───────────────────────────────────────────────
text = text.replace(
    'Note that eDNA degrades more rapidly in tidal/saline water than in freshwater<!-- PENDING: Footnote — cite eDNA degradation study if available -->; the true Brook Trout signal from upstream reaches may be understated at this tidal sampling point.',
    'eDNA degrades faster in saline water than in freshwater [T7]; the true Brook Trout signal from upstream reaches may be understated at this tidal sampling point.'
)

# ── T9 — Rainbow Smelt Golf Course ───────────────────────────────────────────
text = text.replace(
    'Rainbow Smelt (0.2%) is an anomalous detection — Rainbow Smelt are not documented in Sawmill Brook or Cat Brook and are not expected in a suburban coastal stream in November; this is best treated as a possible hit, not a confirmed detection.<!-- PENDING: Check ESV for Rainbow Smelt at this site -->',
    'Rainbow Smelt (0.2%) is an anomalous detection — not documented in this system; unconfirmed pending ESV review [T9].'
)

# ── T6 — Charophyte invasive caveat block ────────────────────────────────────
text = text.replace(
    '**Critical caveat — invasive species risk.** The 23S rRNA data resolved this signal to class (Charophyceae) but not to genus. Native *Chara* and *Nitella* — clean-water indicators — and **Starry Stonewort (*Nitellopsis obtusa*)** — an invasive charophyte spreading rapidly through the northeastern US from Great Lakes origin — are **both Charophyceae and cannot be distinguished in this dataset**. Starry Stonewort thrives in exactly these conditions: calcium-rich, clear, hard water. It is now documented in Vermont and New York and is actively expanding toward Massachusetts. The conditions at Golf Course/Sawmill Brook are permissive for both the native and the invasive. **In-situ morphological identification or targeted species-specific PCR is required before this signal can be confidently interpreted as native or invasive.** This is not a minor footnote — if *Nitellopsis obtusa* is established here, it is a management priority, not a positive indicator.',
    '**Invasive species flag [T6].** The 23S rRNA resolves this signal to class (Charophyceae) only — native *Chara*/*Nitella* and invasive *Nitellopsis obtusa* (Starry Stonewort) cannot be distinguished from this data. Field morphological identification or species-specific PCR is required before this signal can be interpreted as native or invasive. Do not treat as a confirmed positive indicator until field-verified.'
)

# ── T2 — Esox: Second Pond header ────────────────────────────────────────────
text = text.replace(
    '**Fish:** H(f) = 1.23 · 5 species · 9,311 reads · ***Esox* spp. detected (db: *Esox lucius* — likely native pickerel; QC flag)**',
    '**Fish:** H(f) = 1.23 · 5 species · 9,311 reads · ***Esox* spp. detected [T2]**'
)

# ── T2 — Esox: Second Pond Sentinel Signal ───────────────────────────────────
text = text.replace(
    '***Esox* spp. (database assignment: *Esox lucius*) detected at 1.5% — species-level call considered anomalous; see fish community QC note.**',
    '***Esox* spp. detected at 1.5% — native pickerel [T2].**'
)

# ── T2 — Esox: Second Pond fish table Note ───────────────────────────────────
text = text.replace(
    '| *Esox* spp. (db: *Esox lucius*) | **1.5%** | **QC flag — likely Chain or Redfin Pickerel (native); *Esox lucius* assignment anomalous for this habitat; verify by electrofishing before reporting** |',
    '| *Esox* spp. | **1.5%** | **Native pickerel [T2]** |'
)

# ── T2 — Esox: Second Pond narrative paragraph ───────────────────────────────
text = text.replace(
    'The *Esox* spp. detection (1.5%, database-assigned to *Esox lucius*) is treated as a QC flag — MiFish 12S resolution within the *Esox* genus does not reliably distinguish Northern Pike from Chain Pickerel (*Esox niger*) or Redfin Pickerel (*Esox americanus*), both of which are native to coastal Massachusetts pond systems. The species-level assignment to *Esox lucius* (Northern Pike) is anomalous for this habitat and should not be acted upon without verification by electrofishing or species-specific PCR.',
    '*Esox* spp. at 1.5% is native pickerel [T2].'
)

# ── T2 — Esox: Second Pond Native vs. Non-Native ─────────────────────────────
text = text.replace(
    '*Esox* spp. — likely native pickerel (Chain or Redfin); Northern Pike (*Esox lucius*) cannot be confirmed from this barcode alone. Do not report as non-native without electrofishing verification.',
    '*Esox* spp. — native pickerel [T2].'
)

# ── T1 — Genus-level: MBTS #3 Salmo table ────────────────────────────────────
text = text.replace(
    '| *Salmo* spp. | 1.2% | Genus-level only — Brown Trout (*S. trutta*, stocked) or Atlantic Salmon; cannot distinguish |',
    '| *Salmo* spp. | 1.2% | Genus-level only [T1] |'
)

# ── T1 — Salmo: MBTS #3 Sentinel Signal ──────────────────────────────────────
text = text.replace(
    '*Salmo* spp. 1.2% = genus-level only; could represent stocked Brown Trout from adjacent freshwater habitat.',
    '*Salmo* spp. 1.2% = genus-level only [T1].'
)

# ── T1 — Salmo: MBTS #3 narrative ────────────────────────────────────────────
text = text.replace(
    '*Salmo* spp. at 1.2% cannot be assigned to species — it represents either stocked Brown Trout (*S. trutta*, non-native) that have moved down from the freshwater Sawmill Brook system, or a low-level Atlantic Salmon detection; without species-level resolution this cannot be parsed ecologically.',
    '*Salmo* spp. at 1.2% is genus-level only — Brown Trout or Atlantic Salmon cannot be distinguished from this barcode [T1].'
)

# ── T1 — Genus-level: MBTS #3 Lepomis table ──────────────────────────────────
text = text.replace(
    '| *Lepomis* spp. — Sunfish | 13.2% | Native — genus-level only; freshwater tributary input |',
    '| *Lepomis* spp. — Sunfish | 13.2% | Native [T1] — freshwater tributary |'
)

# ── T1 — Genus-level: Lincoln Pool Lepomis table ─────────────────────────────
text = text.replace(
    '| *Lepomis* spp. — Sunfish | 19.4% | Native — genus-level only |',
    '| *Lepomis* spp. — Sunfish | 19.4% | Native [T1] |'
)

# ── T1 — Genus-level: Lincoln Pool Micropterus table ─────────────────────────
text = text.replace(
    '| *Micropterus* spp. — Bass | 3.5% | Native — genus-level only |',
    '| *Micropterus* spp. — Bass | 3.5% | Native [T1] |'
)

# ── T1 — Genus-level: Lincoln Pool narrative ─────────────────────────────────
text = text.replace(
    '*Micropterus* spp. at 3.5% is genus-level only (Smallmouth Bass or Largemouth Bass — cannot distinguish).',
    '*Micropterus* spp. at 3.5% is genus-level only [T1].'
)

# ── T1 — Genus-level: Atwater Lepomis and Ameiurus table ─────────────────────
text = text.replace(
    '| *Lepomis* spp. — Sunfish | 10.2% | Native — genus-level only |',
    '| *Lepomis* spp. — Sunfish | 10.2% | Native [T1] |'
)
text = text.replace(
    '| *Ameiurus* spp. — Bullhead Catfish | 1.7% | Native — genus-level only |',
    '| *Ameiurus* spp. — Bullhead Catfish | 1.7% | Native [T1] |'
)

# ── T4 — Fundulus parvipinnis: Atwater table ─────────────────────────────────
text = text.replace(
    '| *Fundulus parvipinnis* | 0.8% | California Killifish — Pacific species; database artifact |',
    '| *Fundulus parvipinnis* | 0.8% | Database artifact [T4] — excluded |'
)

# ── T5 — Cormorant QC block: Atwater (condense 3 paragraphs → 1) ─────────────
old_cormorant = """### QC Note — Cormorant Fecal eDNA

The Atwater site is **miles above the tidal zone** on Sawmill Brook, a small freshwater stream. The June 8, 2025 sample was taken under low-water, potentially de-watered summer conditions. Three detections are physically incompatible with live fish presence:

**Brevoortia spp. (Menhaden, 176 reads / 1.7%):** Menhaden are coastal marine/estuarine schooling fish with no freshwater range anywhere in their biology. 176 reads of menhaden DNA in a mid-watershed Sawmill Brook sample is conclusive evidence of **Double-crested Cormorant fecal input** — cormorants actively feed on menhaden in Manchester Harbor and the adjacent coast and transit inland waterways, depositing dietary fish DNA via feces.

**Xiphister spp. (marine prickleback, 65 reads / 0.6%):** An intertidal rocky-shore species with zero freshwater range. Same interpretation — cormorant or other piscivorous seabird dietary artifact.

**Alosa pseudoharengus (Alewife, 85 reads / 0.8%):** Alewife do ascend the lower MBTS system in spring and are confirmed at Second Pond / Cat Brook (Forest Landing). However, the Atwater site is miles above the tidal zone with documented summer dewatering — well beyond where Alewife would appear as live fish in June. The Menhaden signal at the same sample event establishes active cormorant input; the Alewife reads are most parsimoniously explained as cormorant dietary eDNA from the spring coastal run.

**Conclusion:** The Menhaden detection is proof-by-elimination of cormorant fecal eDNA at this sampling event. The Alewife signal shares the same source. **No authenticated live Alewife in Sawmill Brook at the Atwater reach.** This is consistent with the known Alewife distribution in the MBTS watershed — confirmed at Second Pond (the Cat Brook headwater pond at Forest Landing), not reported in mid-watershed freshwater reaches above the tidal zone."""

new_cormorant = """### QC Note — Cormorant Fecal eDNA [T5]

Three detections at this inland freshwater site are cormorant dietary artifacts: **Menhaden (1.7%, 176 reads)** — coastal marine species, no freshwater range; **Xiphister spp. (0.6%, 65 reads)** — intertidal marine species; **Alewife (0.8%, 85 reads)** — above confirmed anadromous limit in June. Menhaden is the diagnostic indicator of Double-crested Cormorant fecal input at inland sites [T5]. **No authenticated live Alewife at the Atwater reach.** Alewife is confirmed at Second Pond (Cat Brook headwater) — not at mid-watershed reaches above the tidal zone."""

text = text.replace(old_cormorant, new_cormorant)

# ── T3 — Longear Sunfish: Upper Sawmill Nov 2025 table ───────────────────────
text = text.replace(
    '| *Longear Sunfish* | *0.3%* | *Database artifact -- not native to New England; treat as misassigned Lepomis spp.* |',
    '| *Longear Sunfish* | *0.3%* | *Database artifact [T3] — excluded* |'
)

# ── T3 — Longear Sunfish: Upper Sawmill Nov 2025 narrative paragraph ─────────
text = text.replace(
    '*Longear Sunfish* (*Lepomis megalotis*, 0.3%) is not native to New England. This detection is a database artifact -- the same category as the *Esox lucius* misassignment documented at Second Pond. It is treated as misassigned *Lepomis* spp. and excluded from ecological interpretation.',
    '*Longear Sunfish* (0.3%) is a database artifact — excluded from ecological interpretation [T3].'
)

# ── T3 — Longear Sunfish: Native vs. Non-Native ──────────────────────────────
text = text.replace(
    'All detected fish are native to eastern North America. No confirmed non-native species. The *Longear Sunfish* assignment is a database artifact (see above).',
    'All detected fish are native to eastern North America. No confirmed non-native species. *Longear Sunfish* is a database artifact [T3].'
)

# ── T2 — Esox in Key Findings table note (Aureoumbra in same table row) ───────
# The Aureoumbra row in Inferred Water Chemistry at Second Pond
text = text.replace(
    '| *Aureoumbra* note | Uncertain | May be database artifact for a freshwater taxon |',
    '| *Aureoumbra* note | Uncertain | Database assignment uncertain — freshwater taxon identification pending ESV review |'
)

# ── Write Taxonomic & QC Notes appendix ──────────────────────────────────────
FOOTNOTES = """

---

# Taxonomic & QC Notes

**[T1] — MiFish 12S barcode resolution limits.** The MiFish 12S rRNA barcode resolves most teleost fish to species level, but certain genera cannot be distinguished below genus. *Lepomis* spp. (sunfish) includes Bluegill, Pumpkinseed, Redear Sunfish, and Longear Sunfish (*L. megalotis*), among others. *Micropterus* spp. includes Largemouth Bass and Smallmouth Bass. *Ameiurus* spp. includes Brown Bullhead, Yellow Bullhead, and Black Bullhead. Cottidae spp. (sculpin) includes Slimy Sculpin and Mottled Sculpin. In all cases the genus-level assignment is reliable; species-level is not. *Salmo* spp. may be Brown Trout (*S. trutta*, non-native, stocked throughout New England) or Atlantic Salmon (*S. salar*, native anadromous) — these two species cannot be distinguished by the MiFish barcode. Life history forms (sea-run vs. stream-resident) cannot be determined by eDNA for any species.

**[T2] — *Esox* spp. / *Esox lucius* database artifact.** The MiFish 12S barcode cannot reliably distinguish *Esox lucius* (Northern Pike, native to northern Maine, non-native in most of Massachusetts) from *Esox niger* (Chain Pickerel, native throughout coastal New England) or *Esox americanus* (Redfin Pickerel, native). In this dataset, ESV_010000 — the *Esox* sequence recovered across all batches — returns a 100% match to native pickerel. The *Esox lucius* species-level database assignment is a reference database artifact, not a confirmed Northern Pike detection. Do not report as Northern Pike or illegal stocking without electrofishing or species-specific PCR confirmation.

**[T3] — *Longear Sunfish* (*Lepomis megalotis*) database artifact.** *Lepomis megalotis* is native to the Great Lakes and Mississippi drainage — not to New England. Any detection in a Massachusetts or Maine eDNA sample is a database artifact: the MiFish barcode assigns the read to the closest reference database entry, which for certain *Lepomis* ESVs is *L. megalotis* rather than the true species (most likely Pumpkinseed *L. gibbosus* or Bluegill *L. macrochirus*). All *Longear Sunfish* detections in this dataset are treated as misassigned *Lepomis* spp. and excluded from ecological interpretation.

**[T4] — *Fundulus parvipinnis* database artifact.** *Fundulus parvipinnis* (California Killifish) is a Pacific coast species with no range east of the Rockies. Any detection in a New England eDNA sample is a database artifact — the barcode assigns these reads to *F. parvipinnis* as the closest available reference match for an eastern *Fundulus* ESV (most likely *Fundulus heteroclitus*, Mummichog). Exclude from ecological interpretation.

**[T5] — Cormorant fecal eDNA.** Double-crested Cormorants (*Phalacrocorax auritus*) forage actively in Manchester Harbor and adjacent coastal waters on Atlantic Menhaden (*Brevoortia* spp.), Alewife, and other marine/estuarine fish. Cormorants transit inland waterways and deposit dietary fish DNA via feces. The diagnostic indicator is **Atlantic Menhaden** — a coastal marine schooling fish with no freshwater range. Any Menhaden detection at an inland freshwater site is evidence of cormorant fecal eDNA input. *Xiphister* spp. (marine prickleback, intertidal rocky shore) is a secondary corroborating indicator. Alewife detections at sites above the confirmed anadromous limit should be evaluated in light of co-occurring Menhaden signal; if Menhaden is present, Alewife is parsimoniously explained by the same fecal source rather than live fish presence.

**[T6] — Charophyte genus / *Nitellopsis obtusa* invasive species uncertainty.** The 23S rRNA barcode in this dataset resolves the Charophyte (Stonewort) signal to class (Charophyceae) but not to genus. Native *Chara* spp. and *Nitella* spp. — clean-water ecological indicators — and invasive *Nitellopsis obtusa* (Starry Stonewort, regulated invasive in multiple northeastern states, expanding rapidly from Great Lakes origin) are both Charophyceae and cannot be distinguished from this data alone. The top database hit at Golf Course/Sawmill Brook is *Nitellopsis obtusa* at 95.8% identity — below the species-level threshold of 97%, with only a 0.3% margin over native *Chara*/*Nitella*. Anecdotal reports from local ecologists and phycologists indicate that *Nitellopsis obtusa* has not been documented in Massachusetts. Field morphological identification or species-specific PCR is required before invasive status can be confirmed or ruled out. The Charophyte signal at this site is ecologically significant regardless of species identity — but its management implications depend entirely on the field determination.

**[T7] — eDNA degradation in tidal/saline water.** eDNA degrades more rapidly in saline and brackish water than in freshwater, due to elevated enzymatic activity and UV exposure in open tidal reaches. Fish eDNA signals from upstream freshwater sources collected at tidal sampling points may therefore be attenuated relative to the true upstream population signal. Brook Trout detections at Below School St (a tidal sampling point) likely understate upstream Brook Trout abundance. Where possible, sampling locations should be sited upstream of the tidal limit to maximize detection sensitivity for freshwater species.

**[T8] — Read count reliability.** eDNA read counts are proportional, not absolute — they represent the fraction of total DNA molecules in a sample matching each species, not fish abundance. Detection reliability scales with both read percentage and total read count. A species at 1% with 50,000 total reads (500 reads) is a reliable detection; the same 1% from only 500 total reads (5 reads) is marginal. In this dataset, total read counts per sample range from ~3,700 (Sawmill Swamp algae) to ~47,870 (Below Lincoln Pool fish). Detections below ~10 reads should be treated with caution regardless of percentage.

**[T9] — Rainbow Smelt anomalous detection (Golf Course/Sawmill Brook, Nov 2023).** Rainbow Smelt (*Osmerus mordax*) are anadromous and do enter some Massachusetts coastal streams for late-winter/spring spawning runs, but are not documented in Sawmill Brook or Cat Brook. The 0.2% detection at Golf Course/Sawmill Brook in November is anomalous for this site and season. ESV-level review is needed to confirm whether this represents a genuine smelt detection or a barcode cross-match. Treat as unconfirmed pending ESV verification.
"""

# Append footnotes before any final section that might exist, or at end
text = text.rstrip() + '\n' + FOOTNOTES

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
