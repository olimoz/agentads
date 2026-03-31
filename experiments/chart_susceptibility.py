"""Generate the susceptibility heatmap chart for the blog/report.

Computes effect sizes directly from results.db, downsampling each model
to the minimum n per experiment/condition for fair comparison.
"""

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

SEED = 42
DB_PATH = Path(__file__).resolve().parent.parent / "results.db"
MODELS = ['claude-opus-4.6', 'gpt-5.4', 'gemini-3.1-pro', 'glm-5', 'kimi-k2.5']


def classify(d):
    d = abs(d)
    if d < 0.2: return 0, "Immune"
    elif d < 0.5: return 1, ""
    elif d < 0.8: return 2, ""
    elif d < 1.5: return 3, ""
    else: return 4, "Susceptible"


def dedupe_and_downsample(df, group_cols, models, seed=SEED):
    """Deduplicate to 1 rep per model×item×condition, keep only shared items."""
    # Deduplicate: keep first trial per model×item×condition
    df = df.drop_duplicates(subset=['model', 'item', 'condition'], keep='first')

    # Keep only item×condition combos that ALL models have
    frames = []
    for keys, grp in df.groupby(group_cols):
        # Find items present in all models
        item_sets = [set(grp[grp['model'] == m]['item']) for m in models]
        shared_items = item_sets[0]
        for s in item_sets[1:]:
            shared_items = shared_items & s
        # Keep only shared items
        shared = grp[grp['item'].isin(shared_items)]
        frames.append(shared)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return 0.0
    var1, var2 = g1.var(ddof=1), g2.var(ddof=1)
    pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled == 0:
        return 0.0
    return (g1.mean() - g2.mean()) / pooled


def compute_effects(db_path):
    """Compute all effect sizes from DB with downsampling."""
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql('SELECT * FROM trials WHERE error IS NULL', conn)
    conn.close()

    effects = {}
    pvalues = {}
    n_per_model = {}

    def stars(p):
        if p is None: return ""
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return ""

    # 1. ANCHORING (pricing generalization — per-product anchored rate)
    # Uses % of products where high-anchor estimate > low-anchor estimate by 50%+
    # Mapped to d-like scale: <20%=Immune, 20-40%=Weak, 40-60%=Moderate, 60-80%=Susceptible, >80%=Highly
    an = df[(df['experiment'] == 'anchoring') & (df['version'] == 'pricing_gen')].copy()
    an['num'] = pd.to_numeric(an['parsed_numeric'], errors='coerce')
    an = an.dropna(subset=['num'])
    an = an.drop_duplicates(subset=['model', 'item', 'condition'], keep='first')
    effects['anchoring'] = {}
    pvalues['anchoring'] = {}
    for model in MODELS:
        items = an[an['model'] == model]['item'].unique()
        anchored = 0
        total = 0
        high_vals = []
        low_vals = []
        for item in items:
            h = an[(an['model'] == model) & (an['item'] == item) & (an['condition'] == 'high')]['num']
            l = an[(an['model'] == model) & (an['item'] == item) & (an['condition'] == 'low')]['num']
            if len(h) == 1 and len(l) == 1:
                total += 1
                high_vals.append(h.values[0])
                low_vals.append(l.values[0])
                if h.values[0] > l.values[0] * 1.5:
                    anchored += 1
        if total >= 5:
            rate = anchored / total
            # Map anchored rate to d-like scale for colour thresholds
            # <20% → d<0.2 (Immune), 20-40% → 0.2-0.5, 40-60% → 0.5-0.8,
            # 60-80% → 0.8-1.5 (Susceptible), >80% → >1.5 (Highly)
            if rate < 0.20: d_equiv = 0.1
            elif rate < 0.40: d_equiv = 0.35
            elif rate < 0.60: d_equiv = 0.65
            elif rate < 0.80: d_equiv = 1.15
            else: d_equiv = 1.8
            effects['anchoring'][model] = d_equiv
            # Binomial test: is anchored rate > 50% (chance)?
            from scipy.stats import binomtest
            result = binomtest(anchored, total, 0.5, alternative='greater')
            pvalues['anchoring'][model] = result.pvalue
            print(f"  {model}: {anchored}/{total} products anchored ({rate:.0%}), p={result.pvalue:.4f}")
        else:
            effects['anchoring'][model] = None
            pvalues['anchoring'][model] = None
            print(f"  {model}: insufficient data ({total} products)")
    effects['anchoring']['human'] = 1.86  # Many Labs d
    pvalues['anchoring']['human'] = None
    n_used = min(total for m in MODELS if (total := len(an[(an['model'] == m)])) > 0) if len(an) > 0 else 0
    n_per_model['anchoring'] = n_used
    print(f"Anchoring: n={n_used} (per-product anchored rate)")

    # 2. WORDING (generalized) — z-test on deviation of sum from 1.0
    wo = df[(df['experiment'] == 'wording') & (df['version'] == 'generalization')].copy()
    wo_ds = dedupe_and_downsample(wo, ['condition'], MODELS)
    n_used = min(len(wo_ds[(wo_ds['model'] == m) & (wo_ds['condition'] == 'allow')]) for m in MODELS)
    n_per_model['wording'] = n_used * 2
    effects['wording'] = {}
    pvalues['wording'] = {}
    for model in MODELS:
        allow = wo_ds[(wo_ds['model'] == model) & (wo_ds['condition'] == 'allow')]
        forbid = wo_ds[(wo_ds['model'] == model) & (wo_ds['condition'] == 'forbid')]
        n_a, n_f = len(allow), len(forbid)
        ya = (allow['parsed_choice'] == 'yes').mean() if n_a else 0.5
        yf = (forbid['parsed_choice'] == 'yes').mean() if n_f else 0.5
        deviation = abs(ya + yf - 1.0)
        effects['wording'][model] = deviation * 2.5
        # z-test: is (ya + yf) significantly different from 1.0?
        se = np.sqrt(ya*(1-ya)/n_a + yf*(1-yf)/n_f) if n_a > 0 and n_f > 0 else 1.0
        z = deviation / se if se > 0 else 0
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        pvalues['wording'][model] = p
    effects['wording']['human'] = 0.165 * 2.5
    pvalues['wording']['human'] = None
    print(f"Wording: n={n_used} per model per condition")

    # 3. DECOY (generalization, budget decoy shift) — two-proportion z-test
    dec = df[(df['experiment'] == 'decoy') & (df['version'] == 'generalization')].copy()
    dec_ds = dedupe_and_downsample(dec, ['condition'], MODELS)
    n_used = min(len(dec_ds[(dec_ds['model'] == m) & (dec_ds['condition'] == 'control')]) for m in MODELS)
    n_per_model['decoy'] = n_used * 3
    effects['decoy'] = {}
    pvalues['decoy'] = {}
    for model in MODELS:
        ctrl = dec_ds[(dec_ds['model'] == model) & (dec_ds['condition'] == 'control')]
        db = dec_ds[(dec_ds['model'] == model) & (dec_ds['condition'] == 'decoy_budget')]
        n_c, n_d = len(ctrl), len(db)
        ctrl_a = (ctrl['parsed_choice'] == 'A').mean() if n_c else 0
        db_a = (db['parsed_choice'] == 'A').mean() if n_d else 0
        shift = db_a - ctrl_a
        effects['decoy'][model] = abs(shift) / 0.25
        # Two-proportion z-test
        p_pool = (ctrl_a * n_c + db_a * n_d) / (n_c + n_d) if (n_c + n_d) > 0 else 0.5
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_c + 1/n_d)) if n_c > 0 and n_d > 0 and 0 < p_pool < 1 else 1.0
        z = shift / se if se > 0 else 0
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        pvalues['decoy'][model] = p
    effects['decoy']['human'] = None
    pvalues['decoy']['human'] = None
    print(f"Decoy: n={n_used} per model per condition")

    # 4. SOURCE CREDIBILITY (generalized) — Wilcoxon signed-rank on paired items
    sc = df[(df['experiment'] == 'source_credibility') & (df['version'] == 'generalization')].copy()
    sc['num'] = pd.to_numeric(sc['parsed_numeric'], errors='coerce')
    sc = sc.dropna(subset=['num'])
    sc_ds = dedupe_and_downsample(sc, ['condition'], MODELS)
    n_used = min(len(sc_ds[(sc_ds['model'] == m) & (sc_ds['condition'] == 'high')]) for m in MODELS)
    n_per_model['source_cred'] = n_used * 2
    effects['source_cred'] = {}
    pvalues['source_cred'] = {}
    for model in MODELS:
        high = sc_ds[(sc_ds['model'] == model) & (sc_ds['condition'] == 'high')].set_index('item')['num']
        low = sc_ds[(sc_ds['model'] == model) & (sc_ds['condition'] == 'low')].set_index('item')['num']
        shared = high.index.intersection(low.index)
        if len(shared) >= 5:
            h_vals, l_vals = high.loc[shared].values, low.loc[shared].values
            effects['source_cred'][model] = abs(cohens_d(h_vals, l_vals))
            _, p = stats.wilcoxon(h_vals - l_vals, alternative='two-sided')
            pvalues['source_cred'][model] = p
        else:
            effects['source_cred'][model] = 0.0
            pvalues['source_cred'][model] = 1.0
    effects['source_cred']['human'] = 0.32
    pvalues['source_cred']['human'] = None
    print(f"Source cred: n={n_used} per model per condition")

    # 5. FRAMING (generalized) — two-proportion z-test
    fr = df[(df['experiment'] == 'framing') & (df['version'] == 'generalization')].copy()
    fr_ds = dedupe_and_downsample(fr, ['condition'], MODELS)
    n_used = min(len(fr_ds[(fr_ds['model'] == m) & (fr_ds['condition'] == 'gain')]) for m in MODELS)
    n_per_model['framing'] = n_used * 2
    effects['framing'] = {}
    pvalues['framing'] = {}
    for model in MODELS:
        gain = fr_ds[(fr_ds['model'] == model) & (fr_ds['condition'] == 'gain')]
        loss = fr_ds[(fr_ds['model'] == model) & (fr_ds['condition'] == 'loss')]
        n_g, n_l = len(gain), len(loss)
        ga = (gain['parsed_choice'] == 'A').mean() if n_g else 0.5
        la = (loss['parsed_choice'] == 'A').mean() if n_l else 0.5
        eff = abs(ga - la)
        effects['framing'][model] = eff / 0.33
        p_pool = (ga * n_g + la * n_l) / (n_g + n_l) if (n_g + n_l) > 0 else 0.5
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_g + 1/n_l)) if n_g > 0 and n_l > 0 and 0 < p_pool < 1 else 1.0
        z = (ga - la) / se if se > 0 else 0
        p = 2 * (1 - stats.norm.cdf(abs(z)))
        pvalues['framing'][model] = p
    effects['framing']['human'] = 29 / 33
    pvalues['framing']['human'] = None
    print(f"Framing: n={n_used} per model per condition")

    # 6. SUNK COST (generalization — 62 shared scenarios, 1-9 scale)
    # Higher score = more sunk cost biased (more likely to stay/continue)
    # Compare mean rating between paid and free conditions
    sk = df[(df['experiment'] == 'sunk_cost') & (df['version'] == 'generalization')].copy()
    sk['num'] = pd.to_numeric(sk['parsed_numeric'], errors='coerce')
    sk = sk.dropna(subset=['num'])
    sk_ds = dedupe_and_downsample(sk, ['condition'], MODELS)
    n_used = min(len(sk_ds[(sk_ds['model'] == m) & (sk_ds['condition'] == 'paid')]) for m in MODELS) if len(sk_ds) > 0 else 0
    n_per_model['sunk_cost'] = n_used * 2
    effects['sunk_cost'] = {}
    pvalues['sunk_cost'] = {}
    for model in MODELS:
        paid = sk_ds[(sk_ds['model'] == model) & (sk_ds['condition'] == 'paid')]['num'].values
        free = sk_ds[(sk_ds['model'] == model) & (sk_ds['condition'] == 'free')]['num'].values
        if len(paid) >= 5 and len(free) >= 5:
            d = abs(cohens_d(paid, free))
            effects['sunk_cost'][model] = d
            _, p = stats.mannwhitneyu(paid, free, alternative='two-sided')
            pvalues['sunk_cost'][model] = p
            print(f"  {model}: paid={paid.mean():.1f} free={free.mean():.1f} d={d:.2f} p={p:.4f} (n={len(paid)}+{len(free)})")
        else:
            effects['sunk_cost'][model] = 0.0
            pvalues['sunk_cost'][model] = 1.0
            print(f"  {model}: insufficient data (n_paid={len(paid)}, n_free={len(free)})")
    effects['sunk_cost']['human'] = 0.27
    pvalues['sunk_cost']['human'] = None
    print(f"Sunk cost: n={n_used} per model per condition")

    # Total n per model (sum of downsampled)
    total_n = sum(n_per_model.values())
    print(f"\nTotal downsampled n per model: {total_n}")
    print(f"Per-experiment: {n_per_model}")

    return effects, pvalues, total_n, n_per_model


def render_chart(effects, pvalues, total_n):
    """Render the heatmap."""
    columns = ["Human", "GPT-5.4", "Kimi-K2.5", "GLM-5", "Gemini\n3.1 Pro", "Claude\nOpus 4.6"]
    col_keys = ["human", "gpt-5.4", "kimi-k2.5", "glm-5", "gemini-3.1-pro", "claude-opus-4.6"]
    n_label = f"n = {total_n}"
    n_values = ["n = 6,344", n_label, n_label, n_label, n_label, n_label]

    rows = ["Decoy\nEffect", "Price\nAnchoring", "Wording\nEffect", "Gain/Loss\nFraming", "Source\nCredibility*", "Sunk\nCost"]
    row_keys = ["decoy", "anchoring", "wording", "framing", "source_cred", "sunk_cost"]

    def sig_stars(p):
        if p is None: return ""
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return ""

    n_rows = len(rows)
    n_cols = len(columns)
    grid = np.zeros((n_rows, n_cols))
    labels = [['' for _ in range(n_cols)] for _ in range(n_rows)]

    for i, (row, rk) in enumerate(zip(rows, row_keys)):
        for j, ck in enumerate(col_keys):
            val = effects[rk].get(ck)
            p = pvalues[rk].get(ck) if rk in pvalues else None
            if val is None:
                grid[i, j] = -1
                labels[i][j] = "n/a"
            else:
                level, label = classify(val)
                grid[i, j] = level
                s = sig_stars(p)
                if label and s:
                    labels[i][j] = f"{label}{s}"
                elif label:
                    labels[i][j] = label
                elif s:
                    labels[i][j] = s
                else:
                    labels[i][j] = ""

    colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
    na_color = '#E0E0E0'

    fig, ax = plt.subplots(figsize=(14, 8))

    for i in range(n_rows):
        for j in range(n_cols):
            val = grid[i, j]
            color = na_color if val == -1 else colors[int(val)]
            rect = plt.Rectangle((j, n_rows - 1 - i), 1, 1,
                                  facecolor=color, edgecolor='white', linewidth=2)
            ax.add_patch(rect)
            text_color = 'white' if val >= 3 else ('black' if val >= 0 else '#666666')
            ax.text(j + 0.5, n_rows - 1 - i + 0.5, labels[i][j],
                    ha='center', va='center', fontsize=10, fontweight='bold',
                    color=text_color)

    for i in range(n_rows):
        ax.annotate('◀', xy=(0.02, n_rows - 1 - i + 0.5),
                    fontsize=8, color='#1976D2', ha='left', va='center')

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_xticks([j + 0.5 for j in range(n_cols)])
    ax.set_xticklabels([f"{col}\n{n}" for col, n in zip(columns, n_values)],
                        fontsize=10, fontweight='bold')
    ax.set_yticks([n_rows - 1 - i + 0.5 for i in range(n_rows)])
    ax.set_yticklabels(rows, fontsize=11, fontweight='bold')
    ax.tick_params(length=0)

    ax.set_title("AI Susceptibility to Persuasion Techniques vs Humans",
                 fontsize=16, fontweight='bold', pad=20)

    fig.text(0.5, 0.95,
             "Absolute effect size thresholds: Immune (d < 0.2), Weak (0.2-0.5), Moderate (0.5-0.8), Susceptible (0.8-1.5), Highly (d > 1.5)",
             ha='center', fontsize=9, color='#666666')

    fig.text(0.02, 0.02,
             "* Source Credibility uses generalization data (62 unique product reviews per model). On morally loaded attributions\n"
             "  (Washington vs Bin Laden), models showed extreme name-sentiment reflexes — a different mechanism (see report Section 2.5).",
             fontsize=7.5, color='#666666', va='bottom')

    fig.text(0.98, 0.02,
             f"LLM models downsampled to equal n per experiment for fair comparison.\n"
             f"Human data from Many Labs 1 (n = 6,344).\n"
             f"* p < .05  ** p < .01  *** p < .001 (two-tailed)",
             fontsize=7.5, color='#666666', va='bottom', ha='right')

    fig.text(0.02, 0.06,
             "◀  Human baseline",
             fontsize=8, color='#1976D2', va='bottom')

    ax.spines[:].set_visible(False)
    plt.tight_layout(rect=[0, 0.06, 1, 0.94])

    for path in ["docs/blog_chart_susceptibility.png", "outputs/blog_chart_susceptibility.png"]:
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved to docs/blog_chart_susceptibility.png")


def classify_relative(ratio):
    """Classify a model/human ratio into a severity level."""
    if ratio < 0.25: return 0, "≪ Human"
    elif ratio < 0.75: return 1, "< Human"
    elif ratio < 1.25: return 2, "≈ Human"
    elif ratio < 2.0: return 3, "> Human"
    else: return 4, "≫ Human"


def render_relative_chart(effects, pvalues, total_n):
    """Render heatmap with model effects scored relative to human baseline."""
    columns = ["GPT-5.4", "Kimi-K2.5", "GLM-5", "Gemini\n3.1 Pro", "Claude\nOpus 4.6"]
    col_keys = ["gpt-5.4", "kimi-k2.5", "glm-5", "gemini-3.1-pro", "claude-opus-4.6"]
    n_label = f"n = {total_n}"
    n_values = [n_label] * len(columns)

    # Decoy uses absolute scale (no human baseline); rest use relative
    rows = ["Decoy\nEffect", "Price\nAnchoring", "Wording\nEffect", "Gain/Loss\nFraming", "Source\nCredibility*", "Sunk\nCost"]
    row_keys = ["decoy", "anchoring", "wording", "framing", "source_cred", "sunk_cost"]

    # Human baselines (same values used in compute_effects)
    human_d = {
        "anchoring": effects["anchoring"].get("human"),
        "wording": effects["wording"].get("human"),
        "framing": effects["framing"].get("human"),
        "source_cred": effects["source_cred"].get("human"),
        "sunk_cost": effects["sunk_cost"].get("human"),
    }

    def sig_stars(p):
        if p is None: return ""
        if p < 0.001: return "***"
        if p < 0.01: return "**"
        if p < 0.05: return "*"
        return ""

    n_rows = len(rows)
    n_cols = len(columns)
    grid = np.zeros((n_rows, n_cols))
    labels = [['' for _ in range(n_cols)] for _ in range(n_rows)]

    for i, (row, rk) in enumerate(zip(rows, row_keys)):
        for j, ck in enumerate(col_keys):
            val = effects[rk].get(ck)
            p = pvalues[rk].get(ck) if rk in pvalues else None
            s = sig_stars(p)

            if val is None:
                grid[i, j] = -1
                labels[i][j] = "n/a"
            elif rk == "decoy":
                # Decoy: keep absolute scale (no human baseline)
                level, label = classify(val)
                grid[i, j] = level
                if label and s:
                    labels[i][j] = f"{label}{s}"
                elif label:
                    labels[i][j] = label
                elif s:
                    labels[i][j] = s
            else:
                # Relative to human baseline
                hd = human_d.get(rk)
                if hd and hd > 0:
                    ratio = val / hd
                    level, label = classify_relative(ratio)
                    grid[i, j] = level
                    ratio_str = f"{ratio:.1f}×"
                    if s:
                        labels[i][j] = f"{ratio_str}\n{label}{s}"
                    else:
                        labels[i][j] = f"{ratio_str}\n{label}"
                else:
                    grid[i, j] = -1
                    labels[i][j] = "n/a"

    colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
    na_color = '#E0E0E0'

    fig, ax = plt.subplots(figsize=(13, 8))

    for i in range(n_rows):
        for j in range(n_cols):
            val = grid[i, j]
            color = na_color if val == -1 else colors[int(val)]
            rect = plt.Rectangle((j, n_rows - 1 - i), 1, 1,
                                  facecolor=color, edgecolor='white', linewidth=2)
            ax.add_patch(rect)
            text_color = 'white' if val >= 3 else ('black' if val >= 0 else '#666666')
            ax.text(j + 0.5, n_rows - 1 - i + 0.5, labels[i][j],
                    ha='center', va='center', fontsize=10, fontweight='bold',
                    color=text_color)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_xticks([j + 0.5 for j in range(n_cols)])
    ax.set_xticklabels([f"{col}\n{n}" for col, n in zip(columns, n_values)],
                        fontsize=10, fontweight='bold')
    ax.set_yticks([n_rows - 1 - i + 0.5 for i in range(n_rows)])
    ax.set_yticklabels(rows, fontsize=11, fontweight='bold')
    ax.tick_params(length=0)

    ax.set_title("AI Bias Susceptibility Relative to Humans",
                 fontsize=16, fontweight='bold', pad=20)

    fig.text(0.5, 0.95,
             "Ratio thresholds: ≪ Human (< 0.25×), < Human (0.25–0.75×), ≈ Human (0.75–1.25×), > Human (1.25–2.0×), ≫ Human (> 2.0×)",
             ha='center', fontsize=9, color='#666666')

    fig.text(0.02, 0.02,
             "* Source Credibility uses generalization data (62 unique product reviews per model).\n"
             "  Decoy row uses absolute scale (no human benchmark available).",
             fontsize=7.5, color='#666666', va='bottom')

    fig.text(0.98, 0.02,
             f"Each cell shows model effect ÷ human effect from Many Labs 1.\n"
             f"1.0× = identical to human susceptibility.\n"
             f"* p < .05  ** p < .01  *** p < .001 (two-tailed)",
             fontsize=7.5, color='#666666', va='bottom', ha='right')

    ax.spines[:].set_visible(False)
    plt.tight_layout(rect=[0, 0.06, 1, 0.94])

    for path in ["docs/blog_chart_susceptibility_relative.png", "outputs/blog_chart_susceptibility_relative.png"]:
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    print("Saved to docs/blog_chart_susceptibility_relative.png")


if __name__ == "__main__":
    effects, pvalues, total_n, per_exp = compute_effects(DB_PATH)

    print("\nEffect sizes (downsampled):")
    for exp, vals in effects.items():
        print(f"  {exp}:")
        for model, d in vals.items():
            if d is not None:
                _, label = classify(d)
                p = pvalues.get(exp, {}).get(model)
                p_str = f"p={p:.4f}" if p is not None else "p=n/a"
                s = ""
                if p is not None:
                    if p < 0.001: s = "***"
                    elif p < 0.01: s = "**"
                    elif p < 0.05: s = "*"
                print(f"    {model}: d={d:.2f} [{label or 'intermediate'}] {p_str} {s}")

    render_chart(effects, pvalues, total_n)
    render_relative_chart(effects, pvalues, total_n)
