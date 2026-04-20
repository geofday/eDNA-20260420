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

SAMPLE_COLS = [
    'CY92PPTX.1', 'CVVU52A9.1', 'CSWEE3DX.1', 'CNTLVPX4.1',
    'CNR7WZYJ.1', 'CDWD42KP.1', 'CA66THTZ.1', 'C4SUMTFY.1', '4JKGTSJ5.1'
]

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
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


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
        ax.set_title(sample, fontsize=10, fontweight='bold')

    # Hide unused axes
    for idx in range(n_samples, len(axes)):
        axes[idx].set_visible(False)

    # Shared legend at bottom
    patches = [mpatches.Patch(color=colors[i], label=major.index[i]) for i in range(n_groups)]
    fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=7,
               bbox_to_anchor=(0.5, -0.02), title='Taxonomic Group', title_fontsize=8)
    fig.suptitle('eDNA Community Composition — Per-Sample Pie Charts\n(23S rRNA gene amplicon data)', fontsize=13)
    fig.tight_layout(rect=[0, 0.06, 1, 0.97])
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out_path}')


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


if __name__ == '__main__':
    main()
