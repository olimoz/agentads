"""Forest plots — one per experiment, models vs human baselines."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .config import OUTPUT_DIR

# Consistent model colours
MODEL_COLORS = {
    "claude-opus-4.6": "#D97706",   # amber
    "gpt-5.4": "#10B981",           # green
    "gemini-3.1-pro": "#3B82F6",    # blue
    "glm-5": "#8B5CF6",             # purple
    "kimi-k2.5": "#EF4444",         # red
}

MODEL_ORDER = ["claude-opus-4.6", "gpt-5.4", "gemini-3.1-pro", "glm-5", "kimi-k2.5"]


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def plot_all(results: dict) -> None:
    """Generate all forest plots."""
    sns.set_theme(style="whitegrid", font_scale=1.1)
    out = ensure_output_dir()

    plot_framing(results["framing"], out)
    plot_anchoring(results["anchoring"], out)
    plot_sunk_cost(results["sunk_cost"], out)
    plot_source_credibility(results["source_credibility"], out)
    plot_wording(results["wording"], out)

    print(f"Plots saved to {out}/")


def plot_framing(data: dict, out: Path) -> None:
    """Forest plot: framing effect (% safe gain - % safe loss) per model."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    for ax, version in zip(axes, ["classic", "product"]):
        models = []
        effects = []
        for model in MODEL_ORDER:
            if model in data and version in data[model]:
                models.append(model)
                effects.append(data[model][version]["effect_pp"])

        y_pos = range(len(models))
        colors = [MODEL_COLORS.get(m, "grey") for m in models]

        ax.barh(y_pos, effects, color=colors, height=0.6, alpha=0.8)

        # Human baseline band
        ax.axvspan(0.45, 0.55, alpha=0.15, color="grey", label="Human baseline (~50pp)")
        ax.axvline(x=0.50, color="grey", linestyle="--", alpha=0.5)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(models)
        ax.set_xlabel("Framing Effect (% safe gain − % safe loss)")
        ax.set_title(f"Framing — {version.title()}")
        ax.set_xlim(-0.1, 1.1)
        ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    fig.savefig(out / "framing_forest.png", dpi=150, bbox_inches="tight")
    fig.savefig(out / "framing_forest.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_anchoring(data: dict, out: Path) -> None:
    """Forest plot: anchoring effect sizes per model."""
    fig, ax = plt.subplots(figsize=(10, 6))

    models = []
    d_values = []
    for model in MODEL_ORDER:
        if model not in data:
            continue
        # Average Cohen's d across classic items
        ds = [
            v["cohens_d"]
            for k, v in data[model].items()
            if k.startswith("classic/") and "cohens_d" in v and not np.isnan(v["cohens_d"])
        ]
        if ds:
            models.append(model)
            d_values.append(np.mean(ds))

    y_pos = range(len(models))
    colors = [MODEL_COLORS.get(m, "grey") for m in models]

    ax.barh(y_pos, d_values, color=colors, height=0.6, alpha=0.8)

    # Human baseline band
    ax.axvspan(0.35, 0.52, alpha=0.15, color="grey", label="Human baseline (r=0.35–0.52)")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(models)
    ax.set_xlabel("Mean Cohen's d (High vs Low anchor)")
    ax.set_title("Anchoring — Classic Items")
    ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    fig.savefig(out / "anchoring_forest.png", dpi=150, bbox_inches="tight")
    fig.savefig(out / "anchoring_forest.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_sunk_cost(data: dict, out: Path) -> None:
    """Sunk cost: classic = mean rating (1-9), product = % sunk cost."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Classic: 1-9 scale bar chart
    ax = axes[0]
    models = []
    means = []
    for model in MODEL_ORDER:
        if model in data and "classic" in data[model] and "mean_rating" in data[model]["classic"]:
            models.append(model)
            means.append(data[model]["classic"]["mean_rating"])

    y_pos = range(len(models))
    colors = [MODEL_COLORS.get(m, "grey") for m in models]
    ax.barh(y_pos, means, color=colors, height=0.6, alpha=0.8)
    ax.axvline(x=7.85, color="grey", linestyle="--", alpha=0.5, label="Human baseline (paid=7.85)")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(models)
    ax.set_xlabel("Mean Rating (1=stay home, 9=go to game)")
    ax.set_title("Sunk Cost — Classic (Paid Ticket)")
    ax.set_xlim(1, 9)
    ax.legend(loc="lower right", fontsize=9)

    # Product: binary choice
    ax = axes[1]
    models = []
    pcts = []
    for model in MODEL_ORDER:
        if model in data and "product" in data[model] and "pct_sunk_cost" in data[model]["product"]:
            models.append(model)
            pcts.append(data[model]["product"]["pct_sunk_cost"])

    y_pos = range(len(models))
    colors = [MODEL_COLORS.get(m, "grey") for m in models]
    ax.barh(y_pos, pcts, color=colors, height=0.6, alpha=0.8)
    ax.axvline(x=0.50, color="grey", linestyle="--", alpha=0.5, label="50% line")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(models)
    ax.set_xlabel("% Choosing Sunk Cost Option (Stay with Vendor A)")
    ax.set_title("Sunk Cost — Product (CRM Vendor)")
    ax.set_xlim(0, 1.0)
    ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    fig.savefig(out / "sunk_cost_forest.png", dpi=150, bbox_inches="tight")
    fig.savefig(out / "sunk_cost_forest.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_source_credibility(data: dict, out: Path) -> None:
    """Grouped bar chart: mean rating per source per model."""
    fig, ax = plt.subplots(figsize=(10, 6))

    sources = ["fraunhofer", "blog", "amazon"]
    source_labels = ["Fraunhofer\n(academic)", "BestDeals247\n(blog)", "TechGuy_2025\n(Amazon)"]
    x = np.arange(len(sources))
    width = 0.18

    for i, model in enumerate(MODEL_ORDER):
        if model not in data:
            continue
        means = [data[model].get(s, {}).get("mean_rating", 0) for s in sources]
        ax.bar(x + i * width, means, width, label=model, color=MODEL_COLORS.get(model, "grey"), alpha=0.8)

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(source_labels)
    ax.set_ylabel("Mean Rating (1-10)")
    ax.set_title("Source Credibility — Same Review, Different Attribution")
    ax.set_ylim(0, 10)
    ax.legend(fontsize=9)

    plt.tight_layout()
    fig.savefig(out / "source_credibility.png", dpi=150, bbox_inches="tight")
    fig.savefig(out / "source_credibility.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_wording(data: dict, out: Path) -> None:
    """Forest plot: wording effect per model."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    for ax, version in zip(axes, ["classic", "product"]):
        models = []
        effects = []
        for model in MODEL_ORDER:
            if model in data and version in data[model]:
                v = data[model][version]
                models.append(model)
                # The wording effect: deviation of sum from 1.0
                # If allow→yes + forbid→yes = 1.0, no wording effect
                effects.append(abs(v["sum"] - 1.0) if not np.isnan(v["sum"]) else 0)

        y_pos = range(len(models))
        colors = [MODEL_COLORS.get(m, "grey") for m in models]

        ax.barh(y_pos, effects, color=colors, height=0.6, alpha=0.8)
        ax.axvline(x=0.0, color="grey", linestyle="-", alpha=0.3)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(models)
        ax.set_xlabel("|allow→yes + forbid→yes − 1.0| (0 = no wording effect)")
        ax.set_title(f"Wording Effect — {version.title()}")
        ax.legend(loc="lower right", fontsize=9)

    plt.tight_layout()
    fig.savefig(out / "wording_forest.png", dpi=150, bbox_inches="tight")
    fig.savefig(out / "wording_forest.pdf", bbox_inches="tight")
    plt.close(fig)
