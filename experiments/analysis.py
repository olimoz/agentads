"""Statistical analysis — effect sizes and comparison to human baselines."""

import numpy as np
import pandas as pd
from scipy import stats


def analyze_all(df: pd.DataFrame) -> dict:
    """Run all analyses and return a summary dict."""
    results = {}
    results["framing"] = analyze_framing(df)
    results["anchoring"] = analyze_anchoring(df)
    results["sunk_cost"] = analyze_sunk_cost(df)
    results["source_credibility"] = analyze_source_credibility(df)
    results["wording"] = analyze_wording(df)
    return results


def analyze_framing(df: pd.DataFrame) -> dict:
    """Framing effect: % choosing safe option per frame per model.

    In gain frame, A is the safe option.
    In loss frame, A is the safe option (certain loss) — but the *framing effect*
    is that humans switch to B (gamble) in the loss frame.
    So we measure: % choosing A in gain - % choosing A in loss.
    """
    framing = df[df["experiment"] == "framing"].copy()
    results = {}

    for model in framing["model"].unique():
        model_data = {}
        for version in framing["version"].unique():
            subset = framing[(framing["model"] == model) & (framing["version"] == version)]
            gain = subset[subset["condition"] == "gain"]
            loss = subset[subset["condition"] == "loss"]

            pct_a_gain = (gain["parsed_choice"] == "A").mean() if len(gain) > 0 else float("nan")
            pct_a_loss = (loss["parsed_choice"] == "A").mean() if len(loss) > 0 else float("nan")
            effect = pct_a_gain - pct_a_loss

            model_data[version] = {
                "pct_safe_gain": pct_a_gain,
                "pct_safe_loss": pct_a_loss,
                "effect_pp": effect,
                "n_gain": len(gain),
                "n_loss": len(loss),
            }
        results[model] = model_data

    return results


def analyze_anchoring(df: pd.DataFrame) -> dict:
    """Anchoring effect: mean estimate per anchor condition."""
    anchoring = df[df["experiment"] == "anchoring"].copy()
    anchoring["parsed_numeric"] = pd.to_numeric(anchoring["parsed_numeric"], errors="coerce")
    results = {}

    for model in anchoring["model"].unique():
        model_data = {}
        for version in anchoring["version"].unique():
            for item in anchoring[anchoring["version"] == version]["item"].unique():
                subset = anchoring[
                    (anchoring["model"] == model)
                    & (anchoring["version"] == version)
                    & (anchoring["item"] == item)
                ]
                high = subset[subset["condition"] == "high"]["parsed_numeric"].dropna()
                low = subset[subset["condition"] == "low"]["parsed_numeric"].dropna()

                key = f"{version}/{item}"
                model_data[key] = {
                    "mean_high": high.mean() if len(high) > 0 else float("nan"),
                    "mean_low": low.mean() if len(low) > 0 else float("nan"),
                    "diff": (high.mean() - low.mean()) if len(high) > 0 and len(low) > 0 else float("nan"),
                    "n_high": len(high),
                    "n_low": len(low),
                }

                # Cohen's d if enough data
                if len(high) >= 2 and len(low) >= 2:
                    d = cohens_d(high.values, low.values)
                    model_data[key]["cohens_d"] = d

        # Format mini-test: compare across formats for product version
        for fmt in anchoring["format"].unique():
            fmt_subset = anchoring[
                (anchoring["model"] == model)
                & (anchoring["version"] == "product")
                & (anchoring["format"] == fmt)
            ]
            if len(fmt_subset) > 0:
                high_fmt = fmt_subset[fmt_subset["condition"] == "high"]["parsed_numeric"].dropna()
                low_fmt = fmt_subset[fmt_subset["condition"] == "low"]["parsed_numeric"].dropna()
                model_data[f"format_{fmt}"] = {
                    "mean_high": high_fmt.mean() if len(high_fmt) > 0 else float("nan"),
                    "mean_low": low_fmt.mean() if len(low_fmt) > 0 else float("nan"),
                    "n": len(fmt_subset),
                }

        results[model] = model_data

    return results


def analyze_sunk_cost(df: pd.DataFrame) -> dict:
    """Sunk cost analysis.

    Classic (Many Labs): 1-9 scale, higher = more likely to go (sunk cost).
    Human baseline: paid=7.85, free=7.24, d=0.272.
    We only have the "paid" condition (no between-subjects free condition),
    so we report the mean rating and compare to human paid baseline.

    Product: binary switch/stay choice.
    """
    sc = df[df["experiment"] == "sunk_cost"].copy()
    results = {}

    for model in sc["model"].unique():
        model_data = {}
        for version in sc["version"].unique():
            subset = sc[(sc["model"] == model) & (sc["version"] == version)]

            if version == "classic":
                # 1-9 scale — extract numeric rating
                ratings = pd.to_numeric(subset["parsed_numeric"], errors="coerce").dropna()
                model_data[version] = {
                    "mean_rating": ratings.mean() if len(ratings) > 0 else float("nan"),
                    "std_rating": ratings.std() if len(ratings) > 1 else float("nan"),
                    "n": len(ratings),
                }
            else:
                # Product: binary choice
                valid = subset[subset["parsed_choice"].isin(["sunk_cost", "rational"])]
                pct_sunk = (valid["parsed_choice"] == "sunk_cost").mean() if len(valid) > 0 else float("nan")
                model_data[version] = {
                    "pct_sunk_cost": pct_sunk,
                    "pct_rational": 1.0 - pct_sunk if not np.isnan(pct_sunk) else float("nan"),
                    "n": len(valid),
                }
        results[model] = model_data

    return results


def analyze_source_credibility(df: pd.DataFrame) -> dict:
    """Source credibility: mean rating per source per model."""
    sc = df[df["experiment"] == "source_credibility"].copy()
    sc["parsed_numeric"] = pd.to_numeric(sc["parsed_numeric"], errors="coerce")
    results = {}

    for model in sc["model"].unique():
        model_data = {}
        for condition in ["fraunhofer", "blog", "amazon"]:
            subset = sc[(sc["model"] == model) & (sc["condition"] == condition)]
            ratings = subset["parsed_numeric"].dropna()
            model_data[condition] = {
                "mean_rating": ratings.mean() if len(ratings) > 0 else float("nan"),
                "std_rating": ratings.std() if len(ratings) > 1 else float("nan"),
                "n": len(ratings),
            }

        # Effect size: Fraunhofer vs Blog
        fraunhofer = sc[(sc["model"] == model) & (sc["condition"] == "fraunhofer")]["parsed_numeric"].dropna()
        blog = sc[(sc["model"] == model) & (sc["condition"] == "blog")]["parsed_numeric"].dropna()
        if len(fraunhofer) >= 2 and len(blog) >= 2:
            model_data["cohens_d_fraunhofer_vs_blog"] = cohens_d(fraunhofer.values, blog.values)

        results[model] = model_data

    return results


def analyze_wording(df: pd.DataFrame) -> dict:
    """Wording effect: % answering 'yes' per wording per model."""
    wording = df[df["experiment"] == "wording"].copy()
    results = {}

    for model in wording["model"].unique():
        model_data = {}
        for version in wording["version"].unique():
            subset = wording[(wording["model"] == model) & (wording["version"] == version)]
            allow = subset[subset["condition"] == "allow"]
            forbid = subset[subset["condition"] == "forbid"]

            pct_yes_allow = (allow["parsed_choice"] == "yes").mean() if len(allow) > 0 else float("nan")
            pct_yes_forbid = (forbid["parsed_choice"] == "yes").mean() if len(forbid) > 0 else float("nan")

            # "Not allow" = "forbid", so if agents are consistent:
            # allow: yes = permit, no = don't permit
            # forbid: yes = ban, no = don't ban
            # Perfect consistency: pct_yes_allow + pct_yes_forbid ≈ 1.0
            # Wording effect: deviation from this

            model_data[version] = {
                "pct_yes_allow": pct_yes_allow,
                "pct_yes_forbid": pct_yes_forbid,
                "sum": pct_yes_allow + pct_yes_forbid if not (np.isnan(pct_yes_allow) or np.isnan(pct_yes_forbid)) else float("nan"),
                "n_allow": len(allow),
                "n_forbid": len(forbid),
            }
        results[model] = model_data

    return results


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return float("nan")
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (group1.mean() - group2.mean()) / pooled_std


def print_summary(results: dict) -> None:
    """Print a human-readable summary of all results."""
    print("\n" + "=" * 70)
    print("EXPERIMENT RESULTS SUMMARY")
    print("=" * 70)

    # Framing
    print("\n--- FRAMING (Human baseline: gain 62.2% certain, loss 33.5%, effect=28.7pp) ---")
    for model, data in results["framing"].items():
        for version, v in data.items():
            print(f"  {model} [{version}]: "
                  f"gain={v['pct_safe_gain']:.0%}, loss={v['pct_safe_loss']:.0%}, "
                  f"effect={v['effect_pp']:+.0%}")

    # Anchoring
    print("\n--- ANCHORING (Human baseline: d=1.16–2.30 across items) ---")
    for model, data in results["anchoring"].items():
        for key, v in data.items():
            if key.startswith("format_"):
                continue
            print(f"  {model} [{key}]: "
                  f"high={v['mean_high']:.0f}, low={v['mean_low']:.0f}, "
                  f"diff={v['diff']:.0f}"
                  + (f", d={v.get('cohens_d', float('nan')):.2f}" if "cohens_d" in v else ""))

    # Sunk cost
    print("\n--- SUNK COST (Human baseline: paid=7.85, d=0.27) ---")
    for model, data in results["sunk_cost"].items():
        for version, v in data.items():
            if "mean_rating" in v:
                print(f"  {model} [{version}]: mean={v['mean_rating']:.1f} (n={v['n']})")
            else:
                print(f"  {model} [{version}]: "
                      f"{v['pct_sunk_cost']:.0%} sunk cost, {v['pct_rational']:.0%} rational "
                      f"(n={v['n']})")

    # Source credibility
    print("\n--- SOURCE CREDIBILITY (Human baseline: liked=5.93, disliked=5.23, d=0.32) ---")
    for model, data in results["source_credibility"].items():
        parts = []
        for src in ["fraunhofer", "blog", "amazon"]:
            if src in data:
                parts.append(f"{src}={data[src]['mean_rating']:.1f}")
        d_str = ""
        if "cohens_d_fraunhofer_vs_blog" in data:
            d_str = f", d(fraun-blog)={data['cohens_d_fraunhofer_vs_blog']:.2f}"
        print(f"  {model}: {', '.join(parts)}{d_str}")

    # Wording
    print("\n--- WORDING (Human baseline: allow=76.3% yes, forbid=7.2% yes, sum=0.835) ---")
    for model, data in results["wording"].items():
        for version, v in data.items():
            print(f"  {model} [{version}]: "
                  f"allow→yes={v['pct_yes_allow']:.0%}, forbid→yes={v['pct_yes_forbid']:.0%}, "
                  f"sum={v['sum']:.2f}")

    print("\n" + "=" * 70)
