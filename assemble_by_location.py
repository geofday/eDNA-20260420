"""
assemble_by_location.py
Reads three source markdown files, extracts site sections, routes each to a
location-based bucket, and assembles a single unified document with abstract,
introduction, and table of contents preceding the bucketed narratives.
"""

import re, os

SOURCE_FILES = [
    'output/ecological_narrative_JVB5776.md',
    'output/algal_summaries_JVB3759_JVB3787_JVB4307_v2.md',
    'output/fish_summaries_JVB3988_JVB4279_JVB4678_JVB4846_JVB4981_JVB5403.md',
    'output/algal_summaries_JVB5403.md',          # JVB5403 algal — overrides fish-only versions
    'output/algal_summaries_JVB3988_JVB4678.md',  # JVB3988 + JVB4678 algal additions
]

OUTPUT_BASE = 'output/eDNA_Reports_by_Location'

def versioned(base, ext='.md'):
    i = 1
    while os.path.exists(f'{base}_v{i}{ext}'):
        i += 1
    return f'{base}_v{i}{ext}'

# ── Bucket definitions ────────────────────────────────────────────────────────

BUCKET_ORDER = [
    'narraguagus',
    'union_river',
    'east_machias',
    'orange_river',
    'mbts',
    'south_shore',
    'cape_cod',
    'saltwater',
]

BUCKET_META = {
    'narraguagus': {
        'title': 'Maine — Narraguagus Watershed',
        'subtitle': 'Deblois, ME · November 2023',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA)',
        'intro': (
            'The Narraguagus River drains the remote forests of Washington County, Maine — '
            'one of the least-developed watersheds in the northeastern United States. This cluster '
            'of five sites captures the upper and middle reaches of the West Branch and its '
            'tributaries, sampled in November 2023 at leaf-off when eDNA from other taxa is minimal '
            'and the fish signal is clearest. The Narraguagus is part of federally designated '
            'critical habitat for the Gulf of Maine Distinct Population Segment (DPS) of Atlantic '
            'Salmon, and it supports wild Brook Trout in its cold headwater tributaries. All five '
            'sites carry both fish (MiFish 12S) and algal (23S rRNA) data — the most complete '
            'ecological dataset in the study. Algal community composition provides independent '
            'inference of water temperature, pH, dissolved oxygen, and nutrient status, substantially '
            'deepening the ecological interpretation beyond fish alone.\n\n'
            '> **Note on pH data:** The Deblois / Narraguagus sampling is the **only study in this '
            'dataset where field-measured pH values exist.** All other sites in this document rely '
            'exclusively on algal biological indicators to infer pH — a directionally reliable '
            'but indirect method. Field pH readings here were made with a **Vivosun handheld pH meter '
            '(uncalibrated)** and should be treated as approximate (±0.5–1.0 pH unit). '
            'Even with that caveat, these are the only directly observed pH numbers in the entire dataset.\n\n'
            '**Brook Trout status: Detected.** '
            '**Atlantic Salmon status: Not detected in this batch.**'
        ),
    },
    'union_river': {
        'title': 'Maine — Union River & Ellsworth Dam',
        'subtitle': 'Ellsworth, ME · July 2024 — May 2025',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA, Jul–Sep 2024) · Fish only (May 2025)',
        'intro': (
            'The Union River at Ellsworth Dam is the most intensively sampled location in this '
            'study — eight samples spanning nearly a year, from the early fall algal bloom period '
            'through the peak spring Alewife run. The Ellsworth Dam is a critical chokepoint for '
            'anadromous fish moving between the tidal Union River estuary and upstream freshwater '
            'habitat. Fish aggregating below the dam during the upstream spawning migration produce '
            'a highly concentrated eDNA signal. Whether upstream fish movement reflects self-passage '
            'or a trap-and-truck assist operation is a key interpretive question that eDNA alone '
            'cannot resolve.\n\n'
            'Early samples (July–September 2024) carry both fish and algal panel data. Spring 2025 '
            'samples are fish-only. The 61.7% Cyanobacteria reading at the Ellsworth Dam face in '
            'September 2024 — a **potential harmful algal bloom (HAB) flag** — is one of the '
            'most ecologically significant algal detections in the entire dataset.\n\n'
            '**Brook Trout status: Detected (Crotch Camp Brook, upstream).**\n'
            '**Atlantic Salmon status: Detected (0.5% at Union River Bridge, May 2025 — '
            'Gulf of Maine DPS; local officials are aware of this finding).**'
        ),
    },
    'east_machias': {
        'title': 'Maine — East Machias / Washington County',
        'subtitle': 'East Machias, ME · October 2024 — August 2025',
        'assay': 'Fish (MiFish 12S) only · Brook Trout qPCR inconclusive',
        'intro': (
            'The East Machias watershed drains the coastal lowlands of Washington County — '
            'historically among the last refugia for wild Atlantic Salmon in the eastern '
            'United States. This bucket covers the East Machias River main stem and its major '
            'tributaries, sampled in October 2024, plus Gardner Lake (a headwater impoundment) '
            'and repeat East Machias Rt 9 sampling in July–August 2025.\n\n'
            '**Atlantic Salmon confirmed at Northern Stream (1.1%) and Richardson Stream '
            '(1.7%)** — Gulf of Maine DPS, federally endangered. These are natal tributaries '
            'with active spawning-run fish in the fall sampling window. Local officials are aware '
            'of these detections. A targeted Brook Trout qPCR assay (JVB4683) run on the same water '
            'samples returned inconclusive results — not interpretable as confirmed absence.\n\n'
            '**Brook Trout status: Not detected at mainstem / lower-reach sites. '
            'Cold headwater tributary sampling strongly recommended.**\n'
            '**Atlantic Salmon status: Confirmed — two natal tributaries.**'
        ),
    },
    'orange_river': {
        'title': 'Maine — Orange River (Temporal Monitoring)',
        'subtitle': 'Orange, ME · March — June 2025',
        'assay': 'Fish (MiFish 12S) only',
        'intro': (
            'The Orange River is a small coastal Maine stream sampled at six time points '
            'across spring and early summer 2025 — the only site in this study with a continuous '
            'temporal monitoring arc. This is an ecological diary for a single stream: March ice-out '
            'through June low water, covering the full arc of anadromous fish movement, cyprinid '
            'spring spawning, and summer low-flow concentration. The Orange River drains a mixed '
            'forest and agricultural landscape and shows marked seasonal turnover in fish community '
            'composition.\n\n'
            '**Brook Trout confirmed at four of five valid sample events (March–May 2025)**, '
            'peaking at 5.5% on April 21 (2,561 reads). The temporal arc — 0.5% in late March, '
            '5.5% in late April, 1.8% in early May, 1.0% in mid-May — is consistent with spring '
            'Brook Trout activity in cold water declining as June low-water and warming suppress '
            'eDNA shedding. **Brook Trout is an active, consistent community member in the Orange '
            'River, not absent.** Chain Pickerel (*Esox* spp.) dominates the March sample at '
            'nearly 48% (spring spawning season) and remains present at 4–20% through June. '
            'Sunfish (*Lepomis* spp.) are consistently present at 3–20%, becoming dominant '
            'alongside Eel by summer.\n\n'
            '**Brook Trout status: Confirmed — detected at four of five valid sample events '
            '(March–May 2025). Peak 5.5% April 21.**\n'
            '**Atlantic Salmon status: Not detected.**'
        ),
    },
    'mbts': {
        'title': 'MBTS / Manchester-by-the-Sea, MA — Sawmill Brook System',
        'subtitle': 'Manchester-by-the-Sea, MA · November 2023 — June 2025',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA, Nov 2023 & Aug 2024) · Fish only (Oct 2024–Jun 2025)',
        'intro': (
            'The Sawmill Brook system in Manchester-by-the-Sea is the most intensively monitored '
            'watershed in Massachusetts in this study — thirteen samples across nineteen months at '
            'multiple reaches from Cat Brook headwaters and Second Pond through the mainstem to the '
            'tidal mouth at School Street, draining southwest into Manchester Harbor. '
            'The Manchester-by-the-Sea Brook Trout monitoring program '
            '(MBTS) tracks ecological recovery of a historically impacted suburban stream. '
            'Early samples (November 2023, August 2024) carry both fish and algal data; later '
            'samples are fish-only.\n\n'
            'Second Pond is a headwater impoundment feeding into Cat Brook, which drains to Sawmill '
            'Brook. **Alewife at 63% at Second Pond in October is an exceptional finding** — '
            'Alewife are essentially absent from the rest of the MBTS system, making this '
            'the only confirmed Alewife presence in the entire watershed. This signals a direct '
            'ocean connectivity pathway through Second Pond and Cat Brook that may be available '
            'only seasonally or at specific water levels.\n\n'
            '***Esox* spp. (database: *Esox lucius*) detected at Second Pond (October 2024) — '
            'QC flag: likely native Chain or Redfin Pickerel; MiFish 12S cannot reliably '
            'distinguish *Esox lucius* from native pickerel. Verify by electrofishing before '
            'reporting as illegal stocking.**\n\n'
            '**Brook Trout status: Detected (Lower Golf Course reach, Nov 2023; Atwater site, Jun 2025).**\n'
            '**March 2025 samples (School Street, Elm Street) returned minimal fish reads** — '
            'expected for cold winter water, not a sample failure.'
        ),
    },
    'south_shore': {
        'title': 'South Shore, MA — Third Herring Brook',
        'subtitle': 'Norwell / Hanover, MA · August 2024',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA)',
        'intro': (
            'Third Herring Brook (THB) drains the Norwell/Hanover area of Plymouth County '
            'on the South Shore — a historically significant herring run stream with active '
            'restoration work. This site carries full fish and algal data from August 2024. '
            'The algal community provides independent inferences about the state of the '
            'watershed in late summer.\n\n'
            '**Brook Trout status: See site narrative.**'
        ),
    },
    'cape_cod': {
        'title': 'Cape Cod, MA — Cold-Water Stream Monitoring',
        'subtitle': 'Various, MA · August 2024 — June 2025',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA, Aug–Oct 2024) · Fish only (Jun 2025)',
        'intro': (
            "Cape Cod's coastal plain streams — fed by kettle ponds and glacial aquifer "
            'discharge — are among the most thermally stable cold-water habitats in '
            'Massachusetts. This bucket covers ten sites across multiple Cape watersheds: '
            'Mashpee River, Santuit River, Quashnet River, Red Brook, Orleans SW, and '
            'Brewster (Lower Rd.) — all south-facing, draining to Vineyard Sound. '
            'Fresh Brook (Route 6 and Impoundment) is the exception: it drains east '
            'into Cape Cod Bay.\n\n'
            'Brook Trout presence and absence tracks habitat quality, herring-run timing, and '
            'impoundment history — the primary interpretive thread throughout. **Mashpee River '
            'June 2025 vs. August 2024 comparison:** Brook Trout at 25.9% in August vs. '
            '6.3% in June — detectable in both seasons, with peak signal in August when '
            'summer thermal stress maximizes Brook Trout eDNA shedding from cold-water refugia.\n\n'
            'Early samples (August–October 2024) carry full fish and algal data. '
            'June 2025 samples are fish-only. **Fresh Brook Feces sample (JVB4279) '
            'is included as an annotated QC entry** — massive raccoon DNA contamination; '
            'not an ecological detection.\n\n'
            '**Brook Trout status: Detected at multiple sites (Red Brook, Mashpee, Quashnet). '
            'Seasonal masking documented.**'
        ),
    },
    'saltwater': {
        'title': 'Saltwater / Marine & Estuarine — Open Coast Monitoring',
        'subtitle': 'Manchester-by-the-Sea, MA / Cape Cod Canal, MA · September 2024 & June 2025',
        'assay': 'Fish (MiFish 12S) + Algae (23S rRNA, Sep 2024) · Fish only (Jun 2025)',
        'intro': (
            'This bucket contains marine and estuarine sampling — a conceptually distinct '
            'ecological domain from the freshwater work that constitutes the rest of this '
            'study. Marine and estuarine fish communities are dominated by pelagic, '
            'estuarine, and reef-associated species rather than the anadromous and resident '
            'freshwater species found elsewhere.\n\n'
            'Cohasset Narrows Bridge (September 2024) is at the Cape Cod Canal — a tidal '
            'estuary connecting Cape Cod Bay to Buzzards Bay — and carries both fish and '
            'algal data. Proctor Point Dock (June 2025) is an open-coast marine site at '
            'Manchester-by-the-Sea. These two sites anchor the estuarine-to-open-ocean '
            'range of the marine monitoring effort.\n\n'
            '**Proctor Point Dock yielded 16 species** — the richest single-sample fish '
            'community in the entire dataset — including Atlantic Herring (19.4%), Atlantic '
            'Mackerel (13.7%), Hickory Shad (7.3%), Striped Bass (2.2%), Rock Gunnel (0.6%), '
            'and Cunner. This is an open-coast oceanic assemblage with no freshwater component.\n\n'
            '**Brook Trout status: Not applicable (marine/estuarine sites).**'
        ),
    },
}

# ── Sample ID → bucket ───────────────────────────────────────────────────────

SAMPLE_TO_BUCKET = {
    # Narraguagus (JVB5776)
    'CSWEE3DX': 'narraguagus',
    'CNTLVPX4': 'narraguagus',
    'CNR7WZYJ': 'narraguagus',
    'CY92PPTX': 'narraguagus',
    'CA66THTZ': 'narraguagus',
    # Union River / Ellsworth (JVB3759, JVB4307, JVB4846, JVB4981)
    'D8F0GB5R': 'union_river',
    'SUJI1BGP': 'union_river',
    'HJ7HM41U': 'union_river',
    'KJ4Q9P3R': 'union_river',
    'ASOMDVAL': 'union_river',
    'UYP2KYQ6': 'union_river',
    'TYQXSAUN': 'union_river',
    'K0RLUFS0': 'union_river',
    # East Machias (JVB3988, JVB4307, JVB5403)
    'ZAGSQ1TX': 'east_machias',
    'VD2H2Z3Q': 'east_machias',
    'O5S2DTMM': 'east_machias',
    'FYREF4C4': 'east_machias',
    'B5OWY48H': 'east_machias',
    'B77DD40T': 'east_machias',
    'A5BU49PD': 'east_machias',
    'ZLQM1TH7': 'east_machias',
    'NVHY6MNK': 'east_machias',
    # Orange River (JVB4678, JVB4846, JVB4981, JVB5403)
    '0VKQUDZE': 'orange_river',
    'DAZWXP7N': 'orange_river',
    '2EZ4FTGP': 'orange_river',
    'EYNRUYTO': 'orange_river',
    '8UCIL5TX': 'orange_river',
    '49ZA9JIJ': 'orange_river',
    # MBTS / Manchester (JVB5776, JVB3787, JVB4678, JVB4846, JVB4981)
    'CVVU52A9': 'mbts',
    'CDWD42KP': 'mbts',
    'C4SUMTFY': 'mbts',
    '5K41GBHR': 'mbts',
    'UG79PNJS': 'mbts',
    'OTLHJZBA': 'mbts',
    'UTEVR3WT': 'mbts',
    'OC41MHKC': 'mbts',
    'LZAC7T2X': 'mbts',
    'AEFBOYWK': 'mbts',
    '2KL87R0I': 'mbts',
    # South Shore (JVB3787, JVB4307)
    'L08BN6EZ': 'south_shore',
    'X3L71IPP': 'saltwater',
    # Cape Cod (JVB3787, JVB4307, JVB4279, JVB4678, JVB4981)
    'WRMXR4RT': 'cape_cod',
    'UH7L508D': 'cape_cod',
    'TYKBU74R': 'cape_cod',
    'F5LP8C1M': 'cape_cod',
    'C42JWLMM': 'cape_cod',
    '4JSG0AYS': 'cape_cod',
    'NVN8LUTP': 'mbts',
    '1YI0M1VI': 'cape_cod',
    'ZVYQK9TP': 'cape_cod',
    'KXUG2Y6J': 'mbts',
    '099SCA28': 'cape_cod',
    'S100177':  'cape_cod',
    # Saltwater (JVB4981)
    'HVFHCKJQ': 'saltwater',
}

# Keyword fallback for ## sections without sample IDs
HEADING_BUCKET_KEYWORDS = {
    'orange_river':  ['Orange River'],
    'union_river':   ['Union River', 'Ellsworth Dam Alewife', 'Ellsworth Dam Story'],
    'mbts':          ['Sawmill Brook — Three Sites', 'Sawmill Brook —'],
    'east_machias':  ['JVB3988 — Summary', 'JVB4307 — Summary'],
    'cape_cod':      ['JVB3787 — Regional Summary'],
    'narraguagus':   ['Maine Summary'],
    'mbts':          ['Massachusetts Summary'],
}

SKIP_PATTERNS = [
    'How to Read This',
    'Sentinel Species Reference',
    'Diadromous Species',
    'Fish Sentinels',
    'Algae Sentinels',
    'Algal Sentinels',
    'Combined Story',
    'Water Chemistry Written',
    'Sentinel Pairs',
    'Mineral Story',
    'Algae Drive',
    'Native Species Integrity',
    'Connectivity Is',
    'Impairment Signal',
    # Batch metadata / subtitle headings
    'rRNA',
    'Lab Results:',
    'Single Sample',
    'Ten Sites',
    'Seven Sites',
    'Five Sites',
    'Multi-Site',
    'Mixed-Date',
    'Ecological Narratives',
]

APPENDIX_PATTERNS = [
    'Cross-Batch',
    'Brook Trout Status',
    'Atlantic Salmon — Confirmed',
    'Seasonal eDNA Calendar',
    'Comparative Algal Snapshot',
    'JVB5403 Algal Summary',
    'JVB3988 + JVB4678 Algal Summary',
    'Comparative Snapshot',
    'Non-Aquatic eDNA Detections',
    'What These Are',
    'Non-Aquatic Detections by Site',
    'Why Terrestrial eDNA Cannot',
    'Dietary eDNA Artifacts',
]

# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_sections(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    sections = []
    current = None

    for line in lines:
        raw = line.rstrip('\n')
        if raw.startswith('## '):
            if current is not None:
                sections.append(current)
            heading_text = raw[3:]
            m = re.search(r'\b([A-Z0-9]{8})\b', heading_text)
            sample_id = m.group(1) if m else None
            current = {
                'level': 2,
                'heading': heading_text,
                'content': '',
                'sample_id': sample_id,
                'source': os.path.basename(filepath),
            }
        elif raw.startswith('# ') and not raw.startswith('## '):
            if current is not None:
                sections.append(current)
            heading_text = raw[2:]
            current = {
                'level': 1,
                'heading': heading_text,
                'content': '',
                'sample_id': None,
                'source': os.path.basename(filepath),
            }
        else:
            if current is not None:
                current['content'] += raw + '\n'

    if current is not None:
        sections.append(current)

    return sections


def route_section(section):
    heading = section['heading']

    # By sample ID first
    if section['sample_id']:
        sid = section['sample_id']
        if sid in SAMPLE_TO_BUCKET:
            return SAMPLE_TO_BUCKET[sid]

    # Skip patterns
    for p in SKIP_PATTERNS:
        if p in heading:
            return 'skip'

    # Appendix
    for p in APPENDIX_PATTERNS:
        if p in heading:
            return 'appendix'

    # Level-1 headings (batch/region titles) → skip
    if section['level'] == 1:
        return 'skip'

    # Keyword fallback for level-2 headings
    for bucket, keywords in HEADING_BUCKET_KEYWORDS.items():
        for kw in keywords:
            if kw in heading:
                return bucket

    # Additional keyword patterns
    h = heading.lower()
    if 'orange river' in h:
        return 'orange_river'
    if 'union river' in h or 'ellsworth' in h:
        return 'union_river'
    if 'sawmill' in h or 'mbts' in h or 'manchester' in h:
        return 'mbts'
    if 'narraguagus' in h or 'machias river' in h.replace('east machias', ''):
        return 'narraguagus'
    if 'east machias' in h or 'richardson' in h or 'beaver dam' in h or 'northern stream' in h or 'northern inlet' in h or 'gardner lake' in h:
        return 'east_machias'
    if 'herring brook' in h or 'thb' in h:
        return 'south_shore'
    if 'cohasset narrows' in h:
        return 'saltwater'
    if 'cat brook' in h or 'lincoln pool' in h:
        return 'mbts'
    if 'mashpee' in h or 'fresh brook' in h or 'quashnet' in h or 'santuit' in h or 'red brook' in h or 'orleans' in h or 'brewster' in h:
        return 'cape_cod'
    if 'proctor point' in h:
        return 'saltwater'

    return 'unrouted'


# ── Document content ──────────────────────────────────────────────────────────

ABSTRACT = """\
# eDNA Ecological Reports — New England Freshwater & Coastal Monitoring
## Abstract

Environmental DNA (eDNA) metabarcoding results from ten sample batches (JVB3759–JVB5776) \
collected across coastal Maine and Massachusetts between November 2023 and August 2025. Samples \
were analyzed using MiFish 12S rRNA (fish vertebrates), 23S rRNA (photosynthetic microalgae, \
select batches), and targeted Brook Trout quantitative PCR (qPCR, inconclusive). Results are \
organized by watershed and location — not by batch number — to enable longitudinal comparison \
across time points at the same site.

**Key findings:** Atlantic Salmon (*Salmo salar*, Gulf of Maine Distinct Population Segment) \
confirmed at Northern Stream and Richardson Stream in the East Machias watershed and at Union \
River Bridge — federally endangered; shared with local officials. *Esox* spp. \
(db: *Esox lucius*) detected at Second Pond, Manchester-by-the-Sea — likely native pickerel; \
species-level assignment anomalous; verify before reporting. Potential harmful algal bloom (HAB) flag at Ellsworth Dam face (61.7% Cyanobacteria, \
September 2024). Herring-run masking of Brook Trout eDNA signal documented at Mashpee River \
(June vs. August comparison). **Brook Trout confirmed at Orange River across four of five spring 2025 sample events \
(JVB4846–JVB4981), peaking at 5.5% April 21, 2025.** Sixteen-species marine assemblage at \
Proctor Point Dock, Manchester — richest single-sample community in the dataset.\
"""

INTRODUCTION = """\
# Introduction

## What eDNA Metabarcoding Does — and Doesn't — Tell Us

Environmental DNA (eDNA) metabarcoding amplifies short, standardized genetic marker sequences \
from water samples and matches them to reference databases. The MiFish 12S rRNA marker targets \
fish vertebrates; the 23S rRNA marker targets photosynthetic microalgae. Results are expressed \
as relative read proportions — the fraction of identified genetic reads belonging to each species — \
not as counts, biomass, or population estimates. eDNA detects species *presence*; it cannot \
distinguish life history form (sea-run vs. resident Brook Trout), ecotype, age class, or residency. \
A single fish passing through a reach can leave detectable eDNA.

Relative read proportions are influenced by shedding rate, water temperature, flow, sample volume, \
and the composition of the co-occurring community. When a dominant species (e.g., Alewife during \
the spring herring run) constitutes 80–90% of reads, minority species may fall below detection \
thresholds even if present in the water. At Mashpee River, Brook Trout (*Salvelinus* spp.) is \
detectable at 6.3% in June alongside the herring run peak, and at 25.9% in August — demonstrating \
that Brook Trout presence is not fully masked even during peak herring passage, but that seasonal \
variation in detection intensity is substantial.

## Why We Do This Work

This work is funded by and for trout fishermen. Brook Trout (*Salvelinus fontinalis*) is the \
primary sentinel species — the canary-in-the-coal-mine for cold, clean, well-oxygenated water. \
Brook Trout require dissolved oxygen above 7 mg/L, summer water temperatures below 20°C, and \
stable, permeable gravel substrate for spawning. Where Brook Trout persist, the entire cold-water \
food web is likely intact. Where they have disappeared, the water has warmed, the chemistry has \
shifted, or the physical habitat has been altered.

Every site narrative in this document interprets the fish and algal community first through the \
lens of: *what does this signal mean for Brook Trout and Brook Trout habitat?* When Brook Trout \
is absent, we say so explicitly. When the absence may be methodological (seasonal masking, \
mainstem vs. headwater sampling, insufficient eDNA shedding in cold water), we say that too.

Brown Trout (*Salmo trutta*) and Rainbow Trout (*Oncorhynchus mykiss*) are non-native and \
stocked in New England. They are detected but not celebrated.

## How This Document Is Organized

Earlier reports organized results by batch number (JVB3988, JVB4678, etc.), corresponding to \
laboratory submission order. This document reorganizes the same data by watershed and location, \
so that multiple visits to the same site appear together — enabling year-over-year and \
season-over-season comparison. Eight location buckets are defined below.

**Algal (23S rRNA) data are available for four of ten batches** (JVB3759, JVB3787, JVB4307, \
JVB5776). Where present, the algal community provides independent inference of water temperature, \
pH, dissolved oxygen, and nutrient status that substantially deepens ecological interpretation. \
Additional 23S data are pending for priority sites and will be added to this document.

**Standing rules applied throughout:**
- Fish community percentages are re-normalized to fish-only reads (non-aquatic vertebrates excluded)
- H_f = fish Shannon diversity (−Σ p·ln p); H_a = algal Shannon diversity where available
- Shannon index interpretation: H = 0.00 → single species; 0.01–0.30 → near-monoculture (>90% one species); \
0.30–0.80 → low diversity (2–3 species dominant); 0.80–1.40 → moderate (4–6 species); \
1.40–2.00 → good (6–10 species); 2.00–2.50 → high (10–15+ species); 2.50+ → very high (richest communities)
- No claim of life history form, ecotype, or residency from eDNA alone
- No sea-run or anadromous-life-history claims from eDNA detection
- Ducktrap River, ME (sample 4JKGTSJ5) is tracked separately from all multi-batch analyses\
"""

TOC_SITES = {
    'narraguagus': [
        'McCoy Brook · Nov 2023',
        'Crotch Camp Brook · Nov 2023',
        'UNT Lane Rd · Nov 2023',
        'West Branch Narraguagus @ Sprague\'s Falls · Nov 2023',
        'Narraguagus Rt 193 · Nov 2023',
    ],
    'union_river': [
        'Ellsworth Dam, Union River · Jul 2024',
        '100 m Above Ellsworth Dam · Sep 2024',
        'Ellsworth Dam face · Sep 2024',
        'Rooster Bros, Rt 1, Ellsworth · Sep 2024',
        'Union River Bridge · May 2025',
        'Union River Rooster Bros (peak run) · May 21, 2025',
        'Union River Rooster Brothers · May 31, 2025',
        'Union River Rooster Bros — 3-Syringe Method Comparison · May 31, 2025',
    ],
    'east_machias': [
        'East Machias Rt 9 · Oct 2024',
        'Northern Stream · Oct 2024 ⚑ Atlantic Salmon confirmed',
        'Northern Outlet · Oct 2024',
        'Richardson Stream · Oct 2024 ⚑ Atlantic Salmon confirmed',
        'Beaver Dam Stream · Oct 2024',
        'Northern Inlet · Jul 2025',
        'East Machias Rt 9 · Jul 2025 (repeat)',
        'Gardner Lake (50-ft Meatball) · Aug 2025',
        'Machias River Above Falls · Sep 2024',
    ],
    'orange_river': [
        'Orange River · Mar 14, 2025 (ice-out)',
        'Orange River / High Head Rd · Mar 28, 2025',
        'Orange River "Orange Bucket" · Apr 21, 2025',
        'Orange River · May 7, 2025',
        'Orange River · May 14, 2025 (black fly season)',
        'Orange River · Jun 18, 2025 (low water)',
    ],
    'mbts': [
        'Upper Sawmill Brook · Nov 2023',
        'Below School St · Nov 2023',
        'Lower Golf Course / Sawmill Brook · Nov 2023',
        'Sawmill Swamp · Aug 2024',
        'Sawmill Brook — Below School St · Aug 2024',
        'Sawmill Brook — Fire Station · Aug 2024',
        'Sawmill Brook / School St · Mar 2025 (Fundulus only — Struthio artifact)',
        'Second Pond MBTS · Oct 2024 ⚑ Esox spp. detected (db: E. lucius — verify)',
        'Cat Brook / Forest Landing · Oct 2024',
        'Sawmill Brook Elm Street · Mar 2025 (Struthio artifact — 0 fish reads)',
        'MBTS #3 · Apr 2025',
        'Sawmill Brook — Atwater Site · Jun 2025',
        'Below Lincoln Pool · Jun 2025',
    ],
    'south_shore': [
        'Third Herring Brook (THB) — Norwell/Hanover · Aug 2024',
    ],
    'cape_cod': [
        'Mashpee River · Aug 2024',
        'Fresh Brook, Route 6 (Low Tide) · Aug 2024',
        'Fresh Brook Impoundment · Aug 2024',
        'Santuit River · Aug 2024',
        'Quashnet River · Aug 2024',
        'Orleans SW · Aug 2024',
        'Red Brook Road Pool (Low Tide) · Sep 2024',
        'Lower Rd., Brewster · Sep 2024',
        'Mashpee River · Jun 2025 (herring run — compare Aug 2024)',
        'Fresh Brook Area — Water near Fecal Deposit (QC entry) · 2024',
    ],
    'saltwater': [
        'Cohasset Narrows Bridge · Cape Cod Canal · Sep 2024',
        'Proctor Point Dock, Manchester-by-the-Sea · Jun 2025',
    ],
}

TOC_NUMBERS = {k: i+1 for i, k in enumerate(BUCKET_ORDER)}


def build_toc():
    lines = ['# Table of Contents\n']
    lines.append('**Front Matter**\n')
    lines.append('- Abstract\n')
    lines.append('- Introduction\n')
    lines.append('- How to Read This Document\n')
    lines.append('- Sentinel Species Reference\n')
    lines.append('\n**Field Reports by Location**\n\n')
    for bk in BUCKET_ORDER:
        meta = BUCKET_META[bk]
        num = TOC_NUMBERS[bk]
        lines.append(f'**{num}. {meta["title"]}** — {meta["subtitle"]}\n\n')
        for site in TOC_SITES.get(bk, []):
            lines.append(f'   - {site}\n')
        lines.append('\n')
    lines.append('**Appendix: Cross-Batch Brook Trout & Atlantic Salmon Summary**\n')
    return ''.join(lines)


PREAMBLE = """\
# How to Read This Document

Each site report follows a standard structure:

**Sentinel Signal** — one paragraph distilling the single most important biological message from \
the eDNA data. Written for a non-specialist reader. This is the lede.

**Inferred Water Chemistry** (where algal data available) — a table of water quality parameters \
inferred from the algal community, with the specific indicator taxa driving each inference.

**Fish Community** (or **Algal Community**) — a table of detected species with relative \
read percentages, notes, and Brook Trout / Atlantic Salmon status explicitly stated.

**Narrative** — the full ecological interpretation: what the community composition means, what \
the dominant species signal, what is conspicuously absent, how the site compares to others in the \
dataset.

**Native vs. Non-Native** — explicit accounting of non-native and stocked species.

---

# Sentinel Species Reference

## Primary Sentinel Species

**Brook Trout (*Salvelinus fontinalis*)** — the primary sentinel species for this entire program. \
Brook Trout are the canary-in-the-coal-mine for cold, clean, well-oxygenated freshwater. They \
require dissolved oxygen above 7 mg/L, summer water temperatures below 20°C, and stable, \
permeable gravel substrate for spawning. They are the first to disappear when water warms, \
nutrients rise, or physical habitat degrades. **Brook Trout presence or absence is explicitly \
stated at every site.** Absence at a mainstem reach does not confirm absence from the watershed — \
cold headwater tributaries are the priority sampling targets. Native wild Brook Trout are distinct \
from hatchery fish and cannot be separated by eDNA alone, but their presence confirms cold-water \
habitat quality regardless of life history origin.

---

## Diadromous Species — Ocean-Watershed Bridge

**Alewife (*Alosa pseudoharengus*)** — native anadromous herring; spring upstream spawning run; \
presence confirms ocean-river connectivity.

**Blueback Herring (*Alosa aestivalis*)** — native anadromous; fall run; similar connectivity signal.

**American Eel (*Anguilla rostrata*)** — native catadromous; ocean-river connectivity from the \
other direction; present in nearly all connected systems.

**Atlantic Salmon (*Salmo salar*, Gulf of Maine DPS)** — federally endangered; detection in \
a natal tributary during fall = spawning-run fish. **Report immediately to NOAA Fisheries \
(Greater Atlantic Regional Fisheries Office) and Maine DMR.**

**Rainbow Smelt (*Osmerus mordax*)** — native anadromous; early-spring spawner; cold-water indicator.

**Sea Lamprey (*Petromyzon marinus*)** — native; parasitic on large fish but ecologically \
important; presence confirms large-river connectivity.

## Brook Trout Habitat Indicators

**Fallfish (*Semotilus corporalis*)** — largest native minnow in the Northeast; requires clean \
gravel substrate; positive water quality indicator.

**Creek Chub (*Semotilus atromaculatus*)** — tolerates more marginal conditions than Fallfish; \
presence without Fallfish suggests moderate impairment.

**Tessellated Darter (*Etheostoma olmstedi*)** — clean, well-oxygenated substrate specialist; \
positive indicator wherever it appears.

**Finescale Dace (*Chrosomus neogaeus*)** — cold, soft-water specialist; Brook Trout associate \
in northern Maine headwaters.

## Species Requiring Reporting

***Esox* spp. (db: *Esox lucius*)** — species-level assignment to Northern Pike is considered \
anomalous for coastal MA pond habitat; likely native Chain or Redfin Pickerel. Verify by \
electrofishing or species-specific PCR before any reporting or management action. Local \
officials have been made aware of the detection.

**Atlantic Salmon** — see above.

## Non-Native / Stocked — Detected but Not Celebrated

**Brown Trout (*Salmo trutta*)** — hatchery stocked; European origin; does not indicate wild cold-water quality.

**Rainbow Trout (*Oncorhynchus mykiss*)** — hatchery stocked; Pacific origin.

**Largemouth Bass, Smallmouth Bass, Rock Bass (*Micropterus, Ambloplites*)** — widely introduced; \
tolerant of warm, degraded conditions; negative indicator for Brook Trout habitat quality.\
"""


# ── Assembly ──────────────────────────────────────────────────────────────────

def assemble():
    buckets = {k: [] for k in BUCKET_ORDER}
    buckets['appendix'] = []
    unrouted = []
    # Track which sample IDs have been placed; later files override earlier ones
    placed_sample_ids = {}   # sample_id -> (bucket, list_index)

    for filepath in SOURCE_FILES:
        sections = parse_sections(filepath)
        for section in sections:
            dest = route_section(section)
            if dest == 'skip':
                continue
            elif dest == 'appendix':
                buckets['appendix'].append(section)
            elif dest in buckets:
                sid = section.get('sample_id')
                if sid and sid in placed_sample_ids:
                    # Override: remove the old entry, add the new one
                    old_bucket, old_idx = placed_sample_ids[sid]
                    buckets[old_bucket].pop(old_idx)
                    # Adjust stored indices for items after the removed one
                    for k, (b, i) in list(placed_sample_ids.items()):
                        if b == old_bucket and i > old_idx:
                            placed_sample_ids[k] = (b, i - 1)
                new_idx = len(buckets[dest])
                buckets[dest].append(section)
                if sid:
                    placed_sample_ids[sid] = (dest, new_idx)
            else:
                unrouted.append(section)

    out_path = versioned(OUTPUT_BASE)
    with open(out_path, 'w', encoding='utf-8') as f:
        # Front matter
        f.write(ABSTRACT + '\n\n---\n\n')
        f.write(build_toc() + '\n---\n\n')
        f.write(INTRODUCTION + '\n\n---\n\n')
        f.write(PREAMBLE + '\n\n---\n\n')

        # Buckets
        for bk in BUCKET_ORDER:
            meta = BUCKET_META[bk]
            sections = buckets[bk]
            if not sections:
                continue
            num = TOC_NUMBERS[bk]
            f.write(f'# {num}. {meta["title"]}\n\n')
            f.write(f'**{meta["subtitle"]}**\n\n')
            f.write(f'*Assay: {meta["assay"]}*\n\n')
            f.write(meta['intro'] + '\n\n')
            f.write('---\n\n')

            for sec in sections:
                f.write(f'## {sec["heading"]}\n\n')
                content = sec['content'].rstrip()
                if content:
                    f.write(content + '\n\n')
                f.write('---\n\n')

        # Appendix
        appendix = buckets['appendix']
        if appendix:
            f.write('# Appendix: Cross-Batch Brook Trout & Atlantic Salmon Summary\n\n')
            for sec in appendix:
                f.write(f'## {sec["heading"]}\n\n')
                content = sec['content'].rstrip()
                if content:
                    f.write(content + '\n\n')
                f.write('\n')

    print(f'Saved: {out_path}')

    # Report unrouted
    if unrouted:
        print(f'\nWARNING — {len(unrouted)} unrouted sections:')
        for s in unrouted:
            print(f'  [{s["source"]}] ## {s["heading"][:80]}')

    return out_path


if __name__ == '__main__':
    assemble()
