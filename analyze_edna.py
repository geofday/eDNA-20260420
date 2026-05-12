import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ---------------------------------------------------------------------------
# Taxonomic common-name lookup tables (genus → class → phylum → kingdom)
# Freshwater algae have poor common names; ecological group names are used
# where species-level or genus-level common names don't exist.
# ---------------------------------------------------------------------------

GENUS_COMMON = {
    # Diatoms (Bacillariophyta)
    'Halamphora': 'Halamphora Diatom',
    'Navicula': 'Navicula Diatom',
    'Nitzschia': 'Nitzschia Diatom',
    'Pinnularia': 'Pinnularia Diatom',
    'Cymbella': 'Cymbella Diatom',
    'Gomphonema': 'Gomphonema Diatom',
    'Sellaphora': 'Sellaphora Diatom',
    'Fragilaria': 'Fragilaria (Araphid Diatom)',
    'Staurosira': 'Staurosira (Araphid Diatom)',
    'Aulacoseira': 'Aulacoseira (Centric Diatom)',
    'Cyclotella': 'Cyclotella (Centric Diatom)',
    'Stephanodiscus': 'Stephanodiscus (Centric Diatom)',
    'Asterionella': 'Asterionella (Star Diatom)',
    'Tabellaria': 'Tabellaria (Ribbon Diatom)',
    'Achnanthidium': 'Achnanthidium Diatom',
    'Eunotia': 'Eunotia Diatom',
    # Synurophytes
    'Synura': 'Synura (Colonial Synurophyte)',
    'Mallomonas': 'Mallomonas (Scaled Synurophyte)',
    'Chrysosphaerella': 'Chrysosphaerella (Synurophyte)',
    # Chrysophytes
    'Chromulina': 'Chromulina (Chrysophyte)',
    'Chrysococcus': 'Chrysococcus (Chrysophyte)',
    'Ochromonas': 'Ochromonas (Chrysophyte)',
    'Dinobryon': 'Dinobryon (Colonial Chrysophyte)',
    'Uroglena': 'Uroglena (Colonial Chrysophyte)',
    # Cryptophytes
    'Cryptomonas': 'Cryptomonas (Cryptophyte)',
    'Geminigera': 'Geminigera (Cryptophyte)',
    'Teleaulax': 'Teleaulax (Cryptophyte)',
    'Chroomonas': 'Chroomonas (Cryptophyte)',
    'Guillardia': 'Guillardia (Cryptophyte)',
    'Rhodomonas': 'Rhodomonas (Cryptophyte)',
    # Chlorophytes (green algae)
    'Chlamydomonas': 'Chlamydomonas (Green Alga)',
    'Chlorella': 'Chlorella (Green Alga)',
    'Scenedesmus': 'Scenedesmus (Colonial Green Alga)',
    'Desmodesmus': 'Desmodesmus (Colonial Green Alga)',
    'Pediastrum': 'Pediastrum (Plate Green Alga)',
    'Oocystis': 'Oocystis (Green Alga)',
    'Ankistrodesmus': 'Ankistrodesmus (Needle Green Alga)',
    'Selenastrum': 'Selenastrum (Green Alga)',
    'Micromonas': 'Micromonas (Picoplanktonic Green Alga)',
    'Monomastix': 'Monomastix (Mamiellophyte)',
    # Streptophytes / Charophytes
    'Spirogyra': 'Spirogyra (Filamentous Green Alga)',
    'Zygnema': 'Zygnema (Conjugating Green Alga)',
    'Mougeotia': 'Mougeotia (Conjugating Green Alga)',
    'Closterium': 'Closterium (Desmid)',
    'Cosmarium': 'Cosmarium (Desmid)',
    'Staurastrum': 'Staurastrum (Desmid)',
    'Micrasterias': 'Micrasterias (Desmid)',
    'Nitella': 'Nitella (Stonewort)',
    'Chara': 'Chara (Stonewort)',
    'Klebsormidium': 'Klebsormidium (Charophyte)',
    # Cyanobacteria
    'Synechococcus': 'Synechococcus (Picocyanobacterium)',
    'Cyanobium': 'Cyanobium (Picocyanobacterium)',
    'Microcystis': 'Microcystis (Bloom-Forming Cyanobacterium)',
    'Anabaena': 'Anabaena (Nitrogen-Fixing Cyanobacterium)',
    'Aphanizomenon': 'Aphanizomenon (Nitrogen-Fixing Cyanobacterium)',
    'Oscillatoria': 'Oscillatoria (Filamentous Cyanobacterium)',
    'Planktothrix': 'Planktothrix (Filamentous Cyanobacterium)',
    # Euglenoids
    'Euglena': 'Euglena (Euglenoid)',
    'Euglenaria': 'Euglenaria (Euglenoid)',
    'Phacus': 'Phacus (Euglenoid)',
    'Trachelomonas': 'Trachelomonas (Loricate Euglenoid)',
    # Other flagellates
    'Tribonema': 'Tribonema (Yellow-Green Alga)',
    'Pseudopedinella': 'Pseudopedinella (Dictyochophyte)',
    'Trachydiscus': 'Trachydiscus (Eustigmatophyte)',
    'Chrysochromulina': 'Chrysochromulina (Haptophyte)',
    'Prymnesium': 'Prymnesium (Haptophyte)',
    # Red algae
    'Batrachospermum': 'Batrachospermum (Freshwater Red Alga)',
    'Hildenbrandia': 'Hildenbrandia (Freshwater Red Alga)',
}

CLASS_COMMON = {
    'Bacillariophyceae': 'Pennate Diatoms',
    'Fragilariophyceae': 'Araphid Diatoms',
    'Coscinodiscophyceae': 'Centric Diatoms',
    'Mediophyceae': 'Centric Diatoms',
    'Synurophyceae': 'Synurophytes (Golden-Brown Algae)',
    'Chrysophyceae': 'Chrysophytes (Golden Algae)',
    'Cryptophyceae': 'Cryptophytes',
    'Chlorophyceae': 'Green Algae',
    'Trebouxiophyceae': 'Trebouxiophytes (Green Algae)',
    'Mamiellophyceae': 'Mamiellophytes (Pico-Green Algae)',
    'Ulvophyceae': 'Ulvophytes (Green Algae)',
    'Prasinophyceae': 'Prasinophytes (Green Algae)',
    'Charophyceae': 'Charophytes (Stoneworts)',
    'Zygnemophyceae': 'Conjugating Green Algae (Desmids)',
    'Klebsormidiophyceae': 'Klebsormidiophytes (Charophytes)',
    'Zygnematophyceae': 'Conjugating Green Algae (Desmids)',
    'Coleochaetophyceae': 'Coleochaetophytes (Charophytes)',
    'Magnoliopsida': 'Aquatic Flowering Plants',
    'Liliopsida': 'Aquatic Monocots',
    'Bryopsida': 'Mosses',
    'Cyanophyceae': 'Cyanobacteria',
    'Nostocophyceae': 'Nostocales Cyanobacteria',
    'Euglenophyceae': 'Euglenoids',
    'Xanthophyceae': 'Yellow-Green Algae (Xanthophytes)',
    'Dictyochophyceae': 'Silicoflagellates / Dictyochophytes',
    'Eustigmatophyceae': 'Eustigmatophytes',
    'Florideophyceae': 'Red Algae (Florideophytes)',
    'Porphyridiophyceae': 'Red Algae',
    'Dinophyceae': 'Dinoflagellates',
    'Phaeophyceae': 'Brown Algae',
    'Raphidophyceae': 'Raphidophytes',
}

PHYLUM_COMMON = {
    'Bacillariophyta': 'Diatoms (unclassified)',
    'Chlorophyta': 'Green Algae (unclassified)',
    'Streptophyta': 'Streptophytes / Charophytes (unclassified)',
    'Cyanobacteriota': 'Cyanobacteria (unclassified)',
    'Cryptophyta': 'Cryptophytes (unclassified)',
    'Ochrophyta': 'Ochrophytes / Heterokonts (unclassified)',
    'Chrysophyta': 'Chrysophytes (unclassified)',
    'Euglenozoa': 'Euglenoids (unclassified)',
    'Haptophyta': 'Haptophytes (unclassified)',
    'Rhodophyta': 'Red Algae (unclassified)',
    'Dinoflagellata': 'Dinoflagellates (unclassified)',
    'Xanthophyta': 'Yellow-Green Algae (unclassified)',
    'Charophyta': 'Charophytes (unclassified)',
    'Myzozoa': 'Myzozoans (unclassified)',
}

KINGDOM_COMMON = {
    'Plantae': 'Plants / Plant-like (unclassified)',
    'Chromista': 'Chromists (unclassified)',
    'Protozoa': 'Protozoans (unclassified)',
    'Bacteria': 'Bacteria (unclassified)',
    'Fungi': 'Fungi (unclassified)',
}


def assign_common_name(row):
    genus = str(row.get('Genus', '')).strip()
    cls = str(row.get('Class', '')).strip()
    phylum = str(row.get('Phylum', '')).strip()
    kingdom = str(row.get('Kingdom', '')).strip()
    species = str(row.get('Species', '')).strip()

    # Skip clearly empty / NaN values
    def is_valid(s):
        return s and s.lower() not in ('nan', '', 'none', 'na')

    # Handle 'unk_phylum' style tokens
    def is_unknown(s):
        return s.lower().startswith('unk_') or s.lower() in ('unclassified', 'unknown')

    if is_valid(genus) and not is_unknown(genus) and genus in GENUS_COMMON:
        name = GENUS_COMMON[genus]
        if is_valid(species) and not is_unknown(species) and species != genus:
            sp_epithet = species.split()[-1] if ' ' in species else species
            name = f'{genus} {sp_epithet} ({GENUS_COMMON[genus]})'
        return name

    if is_valid(cls) and not is_unknown(cls) and cls in CLASS_COMMON:
        label = CLASS_COMMON[cls]
        if is_valid(genus) and not is_unknown(genus):
            return f'{genus} ({label})'
        return label

    if is_valid(phylum) and not is_unknown(phylum) and phylum in PHYLUM_COMMON:
        return PHYLUM_COMMON[phylum]

    if is_valid(kingdom) and not is_unknown(kingdom) and kingdom in KINGDOM_COMMON:
        return KINGDOM_COMMON[kingdom]

    # Last resort: use whatever taxonomic info is available
    for val in [genus, cls, phylum, kingdom]:
        if is_valid(val) and not is_unknown(val):
            return f'{val} (unclassified)'

    return 'Unresolved Taxon'


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_CSV = 'JVB5776-23S-read-data-1.csv'
OUTPUT_DIR = 'output'


def _versioned(path):
    """Return path with _vN inserted before the extension, incrementing until unused."""
    base, ext = os.path.splitext(path)
    v = 1
    while os.path.exists(f'{base}_v{v}{ext}'):
        v += 1
    return f'{base}_v{v}{ext}'

SAMPLE_COLS = [
    'CY92PPTX.1', 'CVVU52A9.1', 'CSWEE3DX.1', 'CNTLVPX4.1',
    'CNR7WZYJ.1', 'CDWD42KP.1', 'CA66THTZ.1', 'C4SUMTFY.1', '4JKGTSJ5.1'
]

# Sample location labels  (name → display title with city/state)
SAMPLE_LOCATIONS = {
    'CY92PPTX.1': 'West Branch\nNarraguagus River',
    'CVVU52A9.1': 'Upper Sawmill',
    'CSWEE3DX.1': 'McCoy Brook',
    'CNTLVPX4.1': 'Crotch Camp Brook',
    'CNR7WZYJ.1': 'UNT Lane Rd',
    'CDWD42KP.1': 'Below School St',
    'CA66THTZ.1': 'Narraguagus Rt 193',
    'C4SUMTFY.1': 'Lower Golf Course\nSawmill Brook',
    '4JKGTSJ5.1': 'Ducktrap River\nLincoln, ME',
}

# Date corrections for samples missing a capture date in the CSV
SAMPLE_DATE_OVERRIDES = {
    'CA66THTZ.1': '11/11/2025',  # same collection day as other Deblois sites
}

# Colour palette for up to ~30 groups (tab20 + tab20b)
_cm1 = matplotlib.colormaps.get_cmap('tab20').resampled(20)
_cm2 = matplotlib.colormaps.get_cmap('tab20b').resampled(20)
PALETTE = [_cm1(i) for i in range(20)] + [_cm2(i) for i in range(20)]


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def load_data(path):
    df = pd.read_csv(path, sep=',', skipinitialspace=True)
    # Drop any unnamed trailing column caused by trailing comma in header
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
    # Coerce sample columns to numeric
    for col in SAMPLE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def compute_percentages(df):
    pct = df[SAMPLE_COLS].copy()
    col_sums = pct.sum(axis=0)
    pct = pct.div(col_sums, axis=1) * 100
    return pct


def build_group_table(df, pct_df):
    df = df.copy()
    df['CommonName'] = df.apply(assign_common_name, axis=1)
    pct_df = pct_df.copy()
    pct_df['CommonName'] = df['CommonName'].values

    grouped = pct_df.groupby('CommonName')[SAMPLE_COLS].sum()
    # Sort by mean abundance descending
    grouped['_mean'] = grouped.mean(axis=1)
    grouped = grouped.sort_values('_mean', ascending=False).drop(columns='_mean')
    return grouped


def plot_stacked_bar(grouped, out_path):
    # Collapse minor groups (< 1 % mean) into 'Other'
    mean_pct = grouped.mean(axis=1)
    major = grouped[mean_pct >= 1.0]
    minor = grouped[mean_pct < 1.0]
    if not minor.empty:
        other_row = minor.sum(axis=0).to_frame('Other').T
        major = pd.concat([major, other_row])

    n_groups = len(major)
    colors = PALETTE[:n_groups]

    fig, ax = plt.subplots(figsize=(14, 7))
    bottom = np.zeros(len(SAMPLE_COLS))
    bars = []
    for i, (name, row) in enumerate(major.iterrows()):
        vals = row[SAMPLE_COLS].values.astype(float)
        b = ax.bar(SAMPLE_COLS, vals, bottom=bottom, color=colors[i], label=name, width=0.7)
        bars.append(b)
        bottom += vals

    ax.set_ylim(0, 100)
    ax.set_ylabel('Relative Abundance (%)', fontsize=12)
    ax.set_xlabel('Sample', fontsize=12)
    ax.set_title('eDNA Community Composition — Normalized Stacked Bar Chart\n(23S rRNA gene amplicon data)', fontsize=13)
    ax.set_xticks(range(len(SAMPLE_COLS)))
    ax.set_xticklabels(SAMPLE_COLS, rotation=30, ha='right', fontsize=9)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    legend = ax.legend(
        loc='upper left', bbox_to_anchor=(1.01, 1), fontsize=8,
        title='Taxonomic Group', title_fontsize=9, frameon=True
    )
    fig.tight_layout(rect=[0, 0, 0.82, 1])
    vpath = _versioned(out_path)
    fig.savefig(vpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {vpath}')


def plot_pie_grid(grouped, out_path):
    # Collapse < 2 % into Other for readability
    mean_pct = grouped.mean(axis=1)
    major = grouped[mean_pct >= 2.0]
    minor_sum = grouped[mean_pct < 2.0].sum(axis=0)
    if minor_sum.sum() > 0:
        major = pd.concat([major, minor_sum.to_frame('Other').T])

    n_samples = len(SAMPLE_COLS)
    ncols = 3
    nrows = (n_samples + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 5))
    axes = axes.flatten()

    n_groups = len(major)
    colors = PALETTE[:n_groups]

    for idx, sample in enumerate(SAMPLE_COLS):
        ax = axes[idx]
        vals = major[sample].values.astype(float)
        labels = major.index.tolist()
        nonzero = vals > 0
        ax.pie(
            vals[nonzero],
            labels=None,
            colors=[colors[i] for i in range(n_groups) if nonzero[i]],
            autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
            startangle=90,
            pctdistance=0.8,
        )
        title = SAMPLE_LOCATIONS.get(sample, sample)
        ax.set_title(title, fontsize=9, fontweight='bold', linespacing=1.4)

    # Hide unused axes
    for idx in range(n_samples, len(axes)):
        axes[idx].set_visible(False)

    # Shared legend at bottom
    patches = [mpatches.Patch(color=colors[i], label=major.index[i]) for i in range(n_groups)]
    fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=7,
               bbox_to_anchor=(0.5, -0.02), title='Taxonomic Group', title_fontsize=8)
    fig.suptitle('eDNA Community Composition — Per-Sample Pie Charts\n(23S rRNA gene amplicon data)', fontsize=13)
    fig.tight_layout(rect=[0, 0.06, 1, 0.97])
    vpath = _versioned(out_path)
    fig.savefig(vpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {vpath}')


def compute_diversity(pct_df):
    records = []
    for col in SAMPLE_COLS:
        p = pct_df[col].values / 100.0
        p = p[p > 0]
        shannon = -np.sum(p * np.log(p))
        richness = int((pct_df[col] > 0).sum())
        records.append({'Sample': col, 'Shannon_H': round(shannon, 4), 'ESV_Richness': richness})
    return pd.DataFrame(records)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f'Loading {INPUT_CSV}...')
    df = load_data(INPUT_CSV)
    print(f'  {len(df)} ESVs loaded, {len(SAMPLE_COLS)} samples detected.')

    print('Assigning common names...')
    df['CommonName'] = df.apply(assign_common_name, axis=1)
    unique_names = df['CommonName'].nunique()
    print(f'  {unique_names} unique taxonomic groups identified.')

    print('Computing per-sample percentages...')
    pct_df = compute_percentages(df)

    print('Aggregating by taxonomic group...')
    grouped = build_group_table(df, pct_df)

    # --- CSV output ---
    out_pct_csv = os.path.join(OUTPUT_DIR, 'percentages_by_group.csv')
    grouped.round(4).to_csv(out_pct_csv)
    print(f'  Saved: {out_pct_csv}')

    out_raw_csv = os.path.join(OUTPUT_DIR, 'raw_with_common_names.csv')
    df_out = df.copy()
    for col in SAMPLE_COLS:
        df_out[col + '_pct'] = pct_df[col].round(4)
    df_out.to_csv(out_raw_csv, index=False)
    print(f'  Saved: {out_raw_csv}')

    # --- Plots ---
    print('Generating stacked bar chart...')
    plot_stacked_bar(grouped, os.path.join(OUTPUT_DIR, 'stacked_bar_comparison.png'))

    print('Generating pie chart grid...')
    plot_pie_grid(grouped, os.path.join(OUTPUT_DIR, 'pie_charts_grid.png'))

    # --- Diversity metrics ---
    print('Computing diversity metrics...')
    div_df = compute_diversity(pct_df)
    out_div = os.path.join(OUTPUT_DIR, 'diversity_metrics.csv')
    div_df.to_csv(out_div, index=False)
    print(f'  Saved: {out_div}')
    print('\nDiversity summary:')
    print(div_df.to_string(index=False))

    print('\nDone. All outputs written to the output/ directory.')


# ---------------------------------------------------------------------------
# MiFish (12S rRNA) — real eDNA fish data, Batch JVB5776
# ---------------------------------------------------------------------------

MIFISH_CSV  = 'JVB5776-MiFishU-read-data.csv'
SAMPLES_CSV = 'JVB5776-samples.csv'

MA_SITES = ['CVVU52A9.1', 'CDWD42KP.1', 'C4SUMTFY.1']
ME_SITES = ['CY92PPTX.1', 'CSWEE3DX.1', 'CNTLVPX4.1', 'CNR7WZYJ.1', 'CA66THTZ.1']
DUCKTRAP = '4JKGTSJ5.1'  # always treated separately — community too distinct to compare

MIFISH_COMMON = {
    'Alosa pseudoharengus':      'Alewife',
    'Anguilla rostrata':         'American Eel',
    'Menidia menidia':           'Atlantic Silverside',
    'Catostomus commersonii':    'White Sucker',
    'Micropterus salmoides':     'Largemouth Bass',
    'Lepomis auritus':           'Redbreast Sunfish',
    'Fundulus heteroclitus':     'Mummichog',
    'Microgadus tomcod':         'Atlantic Tomcod',
    'Apeltes quadracus':         'Fourspine Stickleback',
    'Chrosomus neogaeus':        'Finescale Dace',
    'Semotilus atromaculatus':   'Creek Chub',
    'Semotilus corporalis':      'Fallfish',
    'Hybognathus regius':        'Eastern Silvery Minnow',
    'Notemigonus crysoleucas':   'Golden Shiner',
    'Rhinichthys atratulus':     'Blacknose Dace',
    'Morone saxatilis':          'Striped Bass',
    'Morone americana':          'White Perch',
    'Osmerus mordax':            'Rainbow Smelt',
    'Perca flavescens':          'Yellow Perch',
    'Petromyzon marinus':        'Sea Lamprey',
    'Salmo salar':               'Atlantic Salmon',
    'Scomber scombrus':          'Atlantic Mackerel',
    'Syngnathus fuscus':         'Northern Pipefish',
    'Myoxocephalus aenaeus':     'Grubby (Sculpin)',
    'Castor canadensis':         'American Beaver',
    'Ondatra zibethicus':        'Muskrat',
    'Alces alces':               'Moose',
    'Chrysemys picta':           'Painted Turtle',
    'Eurycea bislineata':        'Two-lined Salamander',
    'Notophthalmus viridescens': 'Eastern Newt',
    'Bucephala albeola':         'Bufflehead',
    'Aix sponsa':                'Wood Duck',
    'Microtus montanus':         'Vole sp.',
    'Sus scrofa':                'Wild Boar',
    'Castor fiber':              'European Beaver',
    'Ovis':                      'Sheep sp.',
}

MIFISH_GENUS_COMMON = {
    'Esox':          'Pickerel / Pike sp.',
    'Lepomis':       'Sunfish sp.',
    'Micropterus':   'Bass sp.',
    'Ameiurus':      'Bullhead sp.',
    'Pungitius':     'Ninespine Stickleback',
    'Salvelinus':    'Trout sp.',
    'Cottus':        'Sculpin sp.',
    'Brevoortia':    'Menhaden sp.',
    'Luxilus':       'Shiner sp.',
    'Ictiobus':      'Buffalo sp.',
    'Pseudopleuronectes': 'Winter Flounder sp.',
}


def assign_mifish_name(row):
    sp  = str(row.get('Species', '')).strip()
    gen = str(row.get('Genus',   '')).strip()
    if sp and sp.lower() not in ('nan', '', 'none'):
        if sp in MIFISH_COMMON:
            return MIFISH_COMMON[sp]
        return sp
    if gen and gen.lower() not in ('nan', '', 'none'):
        if gen in MIFISH_GENUS_COMMON:
            return MIFISH_GENUS_COMMON[gen]
        if gen in MIFISH_COMMON:
            return MIFISH_COMMON[gen]
        return f'{gen} sp.'
    return 'Unidentified'


def load_mifish():
    df = pd.read_csv(MIFISH_CSV, skipinitialspace=True)
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
    df = df[df['Kingdom'] != 'PositiveControl'].copy()
    for col in SAMPLE_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['CommonName'] = df.apply(assign_mifish_name, axis=1)
    pct = df[SAMPLE_COLS].copy()
    col_sums = pct.sum(axis=0)
    pct = pct.div(col_sums, axis=1) * 100
    pct['CommonName'] = df['CommonName'].values
    grouped = pct.groupby('CommonName')[SAMPLE_COLS].sum()
    grouped['_mean'] = grouped.mean(axis=1)
    grouped = grouped.sort_values('_mean', ascending=False).drop(columns='_mean')
    return grouped


def load_sample_meta():
    meta = pd.read_csv(SAMPLES_CSV, skipinitialspace=True, index_col=False)
    result = {}
    for _, row in meta.iterrows():
        sid = str(row['SampleId']).strip() + '.1'
        date = SAMPLE_DATE_OVERRIDES.get(sid)
        if not date:
            raw = str(row.get('Capture time (MT)', '')).strip()
            date = raw.split(' ')[0] if raw and raw.lower() != 'nan' else 'date unknown'
        # SAMPLE_LOCATIONS is authoritative; CSV SiteName is fallback only
        site = SAMPLE_LOCATIONS.get(sid)
        if not site:
            site = str(row.get('SiteName', '')).strip()
            if not site or site.lower() in ('nan', 'unknown'):
                site = sid
        result[sid] = {'date': date, 'site': site}
    return result


def _draw_mifish_bar(ax, sample, species_list, data, meta, color_map, fontsize=7):
    species_rev = list(reversed(species_list))
    y_pos = list(range(len(species_rev)))
    vals, bar_colors = [], []

    for sp in species_rev:
        pct = data.loc[sp, sample] if sp in data.index else 0.0
        vals.append(pct / 100)
        bar_colors.append(color_map.get(sp, '#2e7dba') if pct > 0 else '#eeeeee')

    ax.barh(y_pos, vals, color=bar_colors, edgecolor='white', height=0.55)

    # xlim: 2.5× tallest bar so % label sits inside the column
    x_max = max(vals) * 2.5 + 0.01
    n_detected = 0
    for y, v, sp in zip(y_pos, vals, species_rev):
        pct = v * 100
        if pct == 0:
            ax.text(x_max * 0.02, y, 'NF', va='center', ha='left',
                    fontsize=fontsize - 1.5, color='#cccccc')
        else:
            n_detected += 1
            ax.text(v + x_max * 0.03, y, f'{pct:.1f}%', va='center', ha='left',
                    fontsize=fontsize, color='#222222', clip_on=True)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([])
    ax.set_xlim(0, x_max)
    ax.tick_params(axis='x', labelsize=fontsize - 1, bottom=False, labelbottom=False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)

    info = meta.get(sample, {})
    site = info.get('site', sample)
    date = info.get('date', '')
    ax.set_title(f'{site}\n{sample}\n{date}',
                 fontsize=fontsize, linespacing=1.6, pad=6, fontweight='bold')

    # Species count at bottom of column
    ax.text(0.5, -0.02, f'{n_detected} species detected',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=fontsize - 0.5, color='#444444', style='italic')


def plot_mifish_bars(out_path_ma, out_path_me):
    grouped = load_mifish()
    meta    = load_sample_meta()
    all_species = grouped.index.tolist()

    # Consistent colour map across both pages
    color_map = {sp: PALETTE[i % len(PALETTE)] for i, sp in enumerate(all_species)}

    for sites, out_path, region in [
        (MA_SITES, out_path_ma, 'Manchester-by-the-Sea, MA'),
        (ME_SITES, out_path_me, 'Maine'),
    ]:
        # Fish only — drop non-fish vertebrates and re-normalize to 100%
        fish = grouped[~grouped.index.isin(NON_FISH)][sites]
        fish = fish.div(fish.sum(axis=0), axis=1) * 100

        # Only species present in at least one site in this region
        species_list = [sp for sp in fish.index if fish.loc[sp].max() > 0]

        # Letter page portrait (8.5 x 11): bar columns + 1 legend column via gridspec
        ncols = len(sites)
        n_sp  = len(species_list)
        species_rev = list(reversed(species_list))  # bottom→top, matches barh order

        # PowerPoint slide dimensions (10" × 7.5" landscape)
        fig = plt.figure(figsize=(10, 7.5))
        gs = fig.add_gridspec(1, ncols + 1,
                              width_ratios=[1] * ncols + [0.65],
                              wspace=0.06, hspace=0,
                              left=0.03, right=0.99, top=0.80, bottom=0.10)

        bar_axes = [fig.add_subplot(gs[0, i]) for i in range(ncols)]
        leg_ax   = fig.add_subplot(gs[0, ncols], sharey=bar_axes[0])

        for i, sample in enumerate(sites):
            _draw_mifish_bar(bar_axes[i], sample, species_list, fish, meta, color_map,
                             fontsize=5.5)
            bar_axes[i].set_ylim(-0.5, n_sp - 0.5)

        # Legend axis: coloured rects aligned to bar y-positions via sharey
        leg_ax.set_xlim(0, 1)
        leg_ax.axis('off')
        leg_ax.set_title('Species', fontsize=6.5, fontweight='bold', pad=2, loc='left')
        for i, sp in enumerate(species_rev):
            color = color_map.get(sp, '#cccccc')
            rect = mpatches.FancyBboxPatch(
                (0.02, i - 0.27), 0.18, 0.55,
                boxstyle='square,pad=0', facecolor=color, edgecolor='white', lw=0.5)
            leg_ax.add_patch(rect)
            leg_ax.text(0.23, i, sp, va='center', ha='left', fontsize=6.5, clip_on=False)

        # Headline at bottom: region (+ Deblois, ME for ME page since columns omit it) + batch
        loc_note = '  \u2014  Deblois, ME' if 'Maine' in region else ''
        fig.text(0.5, 0.030,
                 f'MiFish eDNA  \u2014  {region}{loc_note}  \u2014  Batch JVB5776  \u2014  Fish Only',
                 ha='center', va='top', fontsize=9, fontweight='bold')
        fig.text(0.5, 0.010,
                 'These samples represent relative species abundance.',
                 ha='center', va='top', fontsize=8, style='italic', color='#444444')

        vpath = _versioned(out_path)
        fig.savefig(vpath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f'  Saved: {vpath}')


def _algae_grouped():
    """Load and return algae percentages grouped by common name."""
    df = load_data(INPUT_CSV)
    return build_group_table(df, compute_percentages(df))


def _algae_bar_page(grouped, meta, sites, out_path, region, data_label,
                    bar_vals_fn, annotation_fn, footer_line2, legend_title):
    """Shared slide-builder for algae bar charts (abundance or Shannon)."""
    all_groups = grouped.index.tolist()
    color_map = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(all_groups)}

    data = grouped[sites]
    group_list = [g for g in all_groups if data.loc[g].max() >= 3.0]
    n_sp = len(group_list)
    species_rev = list(reversed(group_list))

    fig = plt.figure(figsize=(10, 7.5))
    gs = fig.add_gridspec(1, len(sites) + 1,
                          width_ratios=[1] * len(sites) + [0.65],
                          wspace=0.06, hspace=0,
                          left=0.03, right=0.99, top=0.80, bottom=0.10)
    bar_axes = [fig.add_subplot(gs[0, i]) for i in range(len(sites))]
    leg_ax   = fig.add_subplot(gs[0, len(sites)], sharey=bar_axes[0])

    for i, sample in enumerate(sites):
        ax = bar_axes[i]
        info = meta.get(sample, {})
        vals = [bar_vals_fn(data, g, sample) for g in species_rev]
        bar_colors = [color_map[g] if vals[j] > 0 else '#eeeeee'
                      for j, g in enumerate(species_rev)]
        y_pos = list(range(n_sp))
        ax.barh(y_pos, vals, color=bar_colors, edgecolor='white', height=0.55)

        x_max = max(vals) * 2.5 + 0.001
        summary = annotation_fn(data, sample, group_list)
        for y, v, g in zip(y_pos, vals, species_rev):
            if v == 0:
                ax.text(x_max * 0.02, y, 'NF', va='center', ha='left',
                        fontsize=4.5, color='#cccccc')
            else:
                label = f'{v*100:.1f}%' if data_label == 'pct' else f'{v:.3f}'
                ax.text(v + x_max * 0.03, y, label, va='center', ha='left',
                        fontsize=5.5, color='#222222', clip_on=True)

        ax.set_yticks(y_pos)
        ax.set_yticklabels([])
        ax.set_xlim(0, x_max)
        ax.set_ylim(-0.5, n_sp - 0.5)
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        ax.xaxis.grid(True, linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)
        ax.set_title(f"{info.get('site', sample)}\n{sample}\n{info.get('date','')}",
                     fontsize=5.5, linespacing=1.6, pad=6, fontweight='bold')
        ax.text(0.5, -0.02, summary, transform=ax.transAxes,
                ha='center', va='top', fontsize=5.5, color='#333333',
                fontweight='bold')

    leg_ax.set_xlim(0, 1)
    leg_ax.axis('off')
    leg_ax.set_title(legend_title, fontsize=6.5, fontweight='bold', pad=2, loc='left')
    for i, g in enumerate(species_rev):
        rect = mpatches.FancyBboxPatch(
            (0.02, i - 0.27), 0.18, 0.55,
            boxstyle='square,pad=0', facecolor=color_map[g], edgecolor='white', lw=0.5)
        leg_ax.add_patch(rect)
        label = g if len(g) <= 34 else g[:32] + '\u2026'
        leg_ax.text(0.23, i, label, va='center', ha='left', fontsize=6.0, clip_on=False)

    loc_note = '  \u2014  Deblois, ME' if 'Maine' in region else ''
    fig.text(0.5, 0.030,
             f'eDNA Algae (23S rRNA)  \u2014  {region}{loc_note}  \u2014  Batch JVB5776',
             ha='center', va='top', fontsize=9, fontweight='bold')
    fig.text(0.5, 0.010, footer_line2,
             ha='center', va='top', fontsize=8, style='italic', color='#444444')

    vpath = _versioned(out_path)
    fig.savefig(vpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {vpath}')


def plot_algae_bars(out_path_ma, out_path_me):
    grouped = _algae_grouped()
    meta    = load_sample_meta()

    def bar_val(data, g, sample):
        return data.loc[g, sample] / 100.0 if data.loc[g, sample] > 0 else 0.0

    def summary(data, sample, group_list):
        n = int((data.loc[group_list, sample] > 0).sum())
        return f'{n} groups detected'

    for sites, out_path, region in [
        (MA_SITES, out_path_ma, 'Manchester-by-the-Sea, MA'),
        (ME_SITES, out_path_me, 'Maine'),
    ]:
        _algae_bar_page(grouped, meta, sites, out_path, region,
                        data_label='pct',
                        bar_vals_fn=bar_val,
                        annotation_fn=summary,
                        footer_line2='These samples represent relative algal community abundance.',
                        legend_title='Algal Group')


def plot_algae_bars_shannon(out_path_ma, out_path_me):
    grouped = _algae_grouped()
    meta    = load_sample_meta()

    def bar_val(data, g, sample):
        p = data.loc[g, sample] / 100.0
        return -p * np.log(p) if p > 0 else 0.0

    def summary(data, sample, group_list):
        vals = [data.loc[g, sample] / 100.0 for g in group_list]
        h = sum(-p * np.log(p) for p in vals if p > 0)
        n = sum(1 for p in vals if p > 0)
        return f"H\u2032 = {h:.2f}  |  {n} groups"

    for sites, out_path, region in [
        (MA_SITES, out_path_ma, 'Manchester-by-the-Sea, MA'),
        (ME_SITES, out_path_me, 'Maine'),
    ]:
        _algae_bar_page(grouped, meta, sites, out_path, region,
                        data_label='shannon',
                        bar_vals_fn=bar_val,
                        annotation_fn=summary,
                        footer_line2="Shannon diversity: each bar shows algal group\u2019s contribution (\u2212p\u00b7ln p) to site H\u2032.",
                        legend_title='Algal Group')


def plot_mifish_bars_shannon(out_path_ma, out_path_me):
    """Same template as plot_mifish_bars but bars = per-species Shannon contribution (-p·ln p)."""
    grouped = load_mifish()
    meta    = load_sample_meta()
    all_species = grouped.index.tolist()
    color_map = {sp: PALETTE[i % len(PALETTE)] for i, sp in enumerate(all_species)}

    for sites, out_path, region in [
        (MA_SITES, out_path_ma, 'Manchester-by-the-Sea, MA'),
        (ME_SITES, out_path_me, 'Maine'),
    ]:
        fish = grouped[~grouped.index.isin(NON_FISH)][sites]
        fish = fish.div(fish.sum(axis=0), axis=1) * 100
        species_list = [sp for sp in fish.index if fish.loc[sp].max() > 0]

        # Shannon contribution matrix: -p·ln(p) per species per site
        p = fish / 100.0
        shannon = -p * np.log(p.where(p > 0))   # NaN where p==0
        shannon = shannon.fillna(0)

        ncols = len(sites)
        n_sp  = len(species_list)
        species_rev = list(reversed(species_list))

        fig = plt.figure(figsize=(10, 7.5))
        gs = fig.add_gridspec(1, ncols + 1,
                              width_ratios=[1] * ncols + [0.65],
                              wspace=0.06, hspace=0,
                              left=0.03, right=0.99, top=0.80, bottom=0.10)

        bar_axes = [fig.add_subplot(gs[0, i]) for i in range(ncols)]
        leg_ax   = fig.add_subplot(gs[0, ncols], sharey=bar_axes[0])

        for i, sample in enumerate(sites):
            ax = bar_axes[i]
            info = meta.get(sample, {})
            species_rev_vals = [shannon.loc[sp, sample] if sp in shannon.index else 0.0
                                for sp in species_rev]
            bar_colors = [color_map.get(sp, '#eeeeee') if v > 0 else '#eeeeee'
                          for sp, v in zip(species_rev, species_rev_vals)]

            y_pos = list(range(n_sp))
            ax.barh(y_pos, species_rev_vals, color=bar_colors, edgecolor='white', height=0.55)

            x_max = max(species_rev_vals) * 2.5 + 0.001
            h_total = shannon[sample].sum()
            n_detected = int((fish[sample] > 0).sum())

            for y, v, sp in zip(y_pos, species_rev_vals, species_rev):
                if v == 0:
                    ax.text(x_max * 0.02, y, 'NF', va='center', ha='left',
                            fontsize=5, color='#cccccc')
                else:
                    ax.text(v + x_max * 0.03, y, f'{v:.3f}', va='center', ha='left',
                            fontsize=5.5, color='#222222', clip_on=True)

            ax.set_yticks(y_pos)
            ax.set_yticklabels([])
            ax.set_xlim(0, x_max)
            ax.tick_params(axis='x', labelsize=4.5, bottom=False, labelbottom=False)
            ax.xaxis.grid(True, linestyle='--', alpha=0.4)
            ax.set_axisbelow(True)
            ax.set_ylim(-0.5, n_sp - 0.5)

            site = info.get('site', sample)
            date = info.get('date', '')
            ax.set_title(f'{site}\n{sample}\n{date}',
                         fontsize=5.5, linespacing=1.6, pad=6, fontweight='bold')
            ax.text(0.5, -0.02, f'H\u2032 = {h_total:.2f}  |  {n_detected} spp.',
                    transform=ax.transAxes, ha='center', va='top',
                    fontsize=5.5, color='#333333', fontweight='bold')

        # Aligned colour key
        leg_ax.set_xlim(0, 1)
        leg_ax.axis('off')
        leg_ax.set_title('Species', fontsize=6.5, fontweight='bold', pad=2, loc='left')
        for i, sp in enumerate(species_rev):
            color = color_map.get(sp, '#cccccc')
            rect = mpatches.FancyBboxPatch(
                (0.02, i - 0.27), 0.18, 0.55,
                boxstyle='square,pad=0', facecolor=color, edgecolor='white', lw=0.5)
            leg_ax.add_patch(rect)
            leg_ax.text(0.23, i, sp, va='center', ha='left', fontsize=6.5, clip_on=False)

        loc_note = '  \u2014  Deblois, ME' if 'Maine' in region else ''
        fig.text(0.5, 0.030,
                 f'MiFish eDNA  \u2014  {region}{loc_note}  \u2014  Batch JVB5776  \u2014  Fish Only',
                 ha='center', va='top', fontsize=9, fontweight='bold')
        fig.text(0.5, 0.010,
                 "Shannon diversity: each bar shows species\u2019 contribution (\u2212p\u00b7ln p) to site H\u2032.",
                 ha='center', va='top', fontsize=8, style='italic', color='#444444')

        vpath = _versioned(out_path)
        fig.savefig(vpath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f'  Saved: {vpath}')


def plot_ducktrap_bars(out_path_abund, out_path_shannon):
    """Standalone slide pair for Ducktrap River — relative abundance and Shannon."""
    grouped = load_mifish()
    meta    = load_sample_meta()
    all_species = grouped.index.tolist()
    color_map = {sp: PALETTE[i % len(PALETTE)] for i, sp in enumerate(all_species)}

    fish = grouped[~grouped.index.isin(NON_FISH)][[DUCKTRAP]]
    fish = fish.div(fish.sum(axis=0), axis=1) * 100
    species_list = [sp for sp in fish.index if fish.loc[sp, DUCKTRAP] > 0]
    species_rev  = list(reversed(species_list))
    n_sp = len(species_list)

    p = fish / 100.0
    shannon = -p * np.log(p.where(p > 0))
    shannon = shannon.fillna(0)

    for mode, out_path in [('abund', out_path_abund), ('shannon', out_path_shannon)]:
        fig = plt.figure(figsize=(10, 7.5))
        gs = fig.add_gridspec(1, 2,
                              width_ratios=[1, 0.65],
                              wspace=0.06,
                              left=0.03, right=0.99, top=0.80, bottom=0.10)
        bar_ax = fig.add_subplot(gs[0, 0])
        leg_ax = fig.add_subplot(gs[0, 1], sharey=bar_ax)

        if mode == 'abund':
            vals = [fish.loc[sp, DUCKTRAP] / 100.0 for sp in species_rev]
        else:
            vals = [shannon.loc[sp, DUCKTRAP] if sp in shannon.index else 0.0
                    for sp in species_rev]

        bar_colors = [color_map.get(sp, '#eeeeee') if v > 0 else '#eeeeee'
                      for sp, v in zip(species_rev, vals)]
        y_pos = list(range(n_sp))
        bar_ax.barh(y_pos, vals, color=bar_colors, edgecolor='white', height=0.55)

        x_max = max(vals) * 2.5 + 0.01
        n_detected = 0
        for y, v, sp in zip(y_pos, vals, species_rev):
            if v == 0:
                bar_ax.text(x_max * 0.02, y, 'NF', va='center', ha='left',
                            fontsize=5.5, color='#cccccc')
            else:
                n_detected += 1
                label = f'{v*100:.1f}%' if mode == 'abund' else f'{v:.3f}'
                bar_ax.text(v + x_max * 0.03, y, label, va='center', ha='left',
                            fontsize=6.5, color='#222222', clip_on=True)

        bar_ax.set_yticks(y_pos)
        bar_ax.set_yticklabels([])
        bar_ax.set_xlim(0, x_max)
        bar_ax.set_ylim(-0.5, n_sp - 0.5)
        bar_ax.tick_params(axis='x', bottom=False, labelbottom=False)
        bar_ax.xaxis.grid(True, linestyle='--', alpha=0.4)
        bar_ax.set_axisbelow(True)

        info = meta.get(DUCKTRAP, {})
        bar_ax.set_title(f"{info.get('site', DUCKTRAP)}\n{DUCKTRAP}\n{info.get('date','')}",
                         fontsize=7, linespacing=1.6, pad=6, fontweight='bold')

        if mode == 'abund':
            footer_note = f'{n_detected} species detected'
        else:
            h_total = shannon[DUCKTRAP].sum()
            footer_note = f"H′ = {h_total:.2f}  |  {n_detected} spp."
        bar_ax.text(0.5, -0.02, footer_note,
                    transform=bar_ax.transAxes, ha='center', va='top',
                    fontsize=6, color='#333333', fontweight='bold', style='italic')

        leg_ax.set_xlim(0, 1)
        leg_ax.axis('off')
        leg_ax.set_title('Species', fontsize=6.5, fontweight='bold', pad=2, loc='left')
        for i, sp in enumerate(species_rev):
            rect = mpatches.FancyBboxPatch(
                (0.02, i - 0.27), 0.18, 0.55,
                boxstyle='square,pad=0', facecolor=color_map.get(sp, '#cccccc'),
                edgecolor='white', lw=0.5)
            leg_ax.add_patch(rect)
            leg_ax.text(0.23, i, sp, va='center', ha='left', fontsize=6.5, clip_on=False)

        fig.text(0.5, 0.030,
                 'MiFish eDNA  —  Ducktrap River, Lincoln, ME  —  Batch JVB5776  —  Fish Only',
                 ha='center', va='top', fontsize=9, fontweight='bold')
        if mode == 'abund':
            fig.text(0.5, 0.010,
                     'These samples represent relative species abundance.',
                     ha='center', va='top', fontsize=8, style='italic', color='#444444')
        else:
            fig.text(0.5, 0.010,
                     "Shannon diversity: each bar shows species’ contribution (−p·ln p) to site H′.",
                     ha='center', va='top', fontsize=8, style='italic', color='#444444')

        vpath = _versioned(out_path)
        fig.savefig(vpath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f'  Saved: {vpath}')


def plot_mifish_stacked_bar(out_path, exclude=None):
    exclude = exclude or []
    grouped = load_mifish()
    meta    = load_sample_meta()

    # Fish only, exclude specified sites
    fish = grouped[~grouped.index.isin(NON_FISH)]

    ma_sites = MA_SITES
    me_sites = [s for s in ME_SITES if s not in exclude]

    all_sites = ma_sites + me_sites

    # Re-normalize to 100% within fish-only reads per sample
    fish = fish[all_sites]
    col_sums = fish.sum(axis=0)
    fish = fish.div(col_sums, axis=1) * 100

    # Keep species with >= 1% in at least one site; collapse rest to Other
    data = fish
    keep = data.max(axis=1) >= 1.0
    major = data[keep].copy()
    other = data[~keep].sum(axis=0)
    if other.sum() > 0:
        major = pd.concat([major, other.to_frame('Other').T])

    # Sort by total across all sites descending (Other always last)
    non_other = major[major.index != 'Other']
    non_other = non_other.loc[non_other.sum(axis=1).sort_values(ascending=False).index]
    if 'Other' in major.index:
        major = pd.concat([non_other, major.loc[['Other']]])
    else:
        major = non_other

    n_groups = len(major)
    colors = PALETTE[:n_groups]
    color_map = {name: colors[i] for i, name in enumerate(major.index)}

    def make_x_labels(sites):
        labels = []
        for s in sites:
            info = meta.get(s, {})
            labels.append(f"{info.get('site', s)}\n{s}\n{info.get('date','')}")
        return labels

    # Two-panel figure: MA left, ME right, width proportional to site count
    fig, (ax_ma, ax_me) = plt.subplots(
        1, 2,
        figsize=(len(ma_sites) * 2.5 + len(me_sites) * 2.5 + 3, 8),
        gridspec_kw={'width_ratios': [len(ma_sites), len(me_sites)], 'wspace': 0.08}
    )

    for ax, sites, region in [(ax_ma, ma_sites, 'Massachusetts'), (ax_me, me_sites, 'Maine')]:
        bottom = np.zeros(len(sites))
        for name, row in major.iterrows():
            vals = row[sites].values.astype(float)
            ax.bar(range(len(sites)), vals, bottom=bottom,
                   color=color_map[name], label=name, width=0.65)
            bottom += vals
        ax.set_ylim(0, 100)
        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(make_x_labels(sites), fontsize=7.5, ha='center')
        ax.yaxis.grid(True, linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)
        ax.set_title(region, fontsize=11, fontweight='bold', pad=8)

    ax_ma.set_ylabel('Relative Abundance (%)', fontsize=10)
    ax_me.set_yticklabels([])

    # Single shared legend
    handles = [mpatches.Patch(color=color_map[n], label=n) for n in major.index]
    fig.legend(handles=handles, loc='lower center', ncol=4, fontsize=8,
               title='Species', title_fontsize=9, bbox_to_anchor=(0.5, -0.18))

    fig.suptitle('MiFish eDNA - Fish Community Composition\nBatch JVB5776 | 12S rRNA | Normalized Relative Abundance',
                 fontsize=12, fontweight='bold')
    fig.tight_layout(rect=[0, 0.12, 1, 0.97])
    vpath = _versioned(out_path)
    fig.savefig(vpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {vpath}')


NON_FISH = {
    'Moose', 'American Beaver', 'Muskrat', 'Wood Duck', 'Bufflehead',
    'Vole sp.', 'Wild Boar', 'European Beaver', 'Sheep sp.',
    'Painted Turtle', 'Eastern Newt', 'Two-lined Salamander',
    'Unidentified',
}


def _draw_heatmap(ax, data, sites, meta, title):
    x_labels = []
    for s in sites:
        info = meta.get(s, {})
        x_labels.append(f"{info.get('site', s)}\n{s}\n{info.get('date','')}")

    im = ax.imshow(data.values, aspect='auto', cmap='YlOrRd', interpolation='nearest',
                   vmin=0, vmax=data.values.max())
    ax.set_xticks(range(len(sites)))
    ax.set_xticklabels(x_labels, fontsize=8, ha='center')
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=8.5)
    ax.tick_params(axis='both', length=0)
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()

    for i in range(len(data)):
        for j in range(len(sites)):
            val = data.iloc[i, j]
            if val >= 0.5:
                txt_color = 'white' if val > data.values.max() * 0.6 else 'black'
                ax.text(j, i, f'{val:.1f}%', ha='center', va='center',
                        fontsize=7.5, color=txt_color)

    ax.set_title(title, fontsize=10, fontweight='bold', pad=14)
    return im


def plot_mifish_heatmap(out_path_ma, out_path_me, exclude=None):
    exclude = exclude or []
    grouped = load_mifish()
    meta    = load_sample_meta()

    # Fish only — drop non-fish vertebrates, re-normalize to 100%
    fish_data = grouped[~grouped.index.isin(NON_FISH)]
    all_inc = [s for s in SAMPLE_COLS if s not in exclude]
    fish_data = fish_data[all_inc]
    fish_data = fish_data.div(fish_data.sum(axis=0), axis=1) * 100

    for sites, out_path, region in [
        (MA_SITES, out_path_ma, 'Manchester-by-the-Sea, MA'),
        ([s for s in ME_SITES if s not in exclude], out_path_me, 'Maine'),
    ]:
        data = fish_data[sites].copy()
        # Keep only species with >= 1% in at least one site
        data = data[data.max(axis=1) >= 1.0]
        # Sort by total abundance
        data = data.loc[data.sum(axis=1).sort_values(ascending=False).index]

        fig, ax = plt.subplots(figsize=(len(sites) * 2.2 + 1.5, len(data) * 0.42 + 2.5))
        im = _draw_heatmap(ax, data, sites, meta,
                           f'MiFish eDNA - Fish Community | {region}\n'
                           f'Batch JVB5776 | 12S rRNA | Relative Abundance (%)')
        cbar = fig.colorbar(im, ax=ax, shrink=0.5, pad=0.02)
        cbar.set_label('Relative Abundance (%)', fontsize=8)
        fig.tight_layout()
        vpath = _versioned(out_path)
        fig.savefig(vpath, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f'  Saved: {vpath}')


if __name__ == '__main__':
    main()
    print('\nGenerating MiFish bar charts...')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plot_mifish_bars(
        os.path.join(OUTPUT_DIR, 'fish_bars_MA.png'),
        os.path.join(OUTPUT_DIR, 'fish_bars_ME.png'),
    )
    plot_mifish_bars_shannon(
        os.path.join(OUTPUT_DIR, 'fish_bars_shannon_MA.png'),
        os.path.join(OUTPUT_DIR, 'fish_bars_shannon_ME.png'),
    )
    print('\nGenerating Algae bar charts...')
    plot_algae_bars(
        os.path.join(OUTPUT_DIR, 'algae_bars_MA.png'),
        os.path.join(OUTPUT_DIR, 'algae_bars_ME.png'),
    )
    plot_algae_bars_shannon(
        os.path.join(OUTPUT_DIR, 'algae_bars_shannon_MA.png'),
        os.path.join(OUTPUT_DIR, 'algae_bars_shannon_ME.png'),
    )
    print('\nGenerating Ducktrap River standalone slides...')
    plot_ducktrap_bars(
        os.path.join(OUTPUT_DIR, 'fish_bars_ducktrap.png'),
        os.path.join(OUTPUT_DIR, 'fish_bars_shannon_ducktrap.png'),
    )
    plot_mifish_stacked_bar(
        os.path.join(OUTPUT_DIR, 'fish_stacked_bar.png'),
    )
    plot_mifish_heatmap(
        os.path.join(OUTPUT_DIR, 'fish_heatmap_MA.png'),
        os.path.join(OUTPUT_DIR, 'fish_heatmap_ME.png'),
    )
