"""Load experiment stimuli from YAML files and produce TrialSpec objects."""

from dataclasses import dataclass
from pathlib import Path

import yaml

STIMULI_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class TrialSpec:
    experiment: str
    version: str       # 'classic' | 'product'
    condition: str
    format: str        # 'plain' | 'json' | 'html' | 'markdown'
    item: str | None   # for anchoring sub-items
    stimulus_text: str


def load_experiment(name: str) -> dict:
    """Load a single experiment YAML."""
    path = STIMULI_DIR / f"{name}.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def get_trial_specs(name: str) -> list[TrialSpec]:
    """Generate all TrialSpecs for a named experiment."""
    data = load_experiment(name)
    specs = []

    if name == "anchoring":
        specs.extend(_anchoring_specs(data))
    elif name == "source_credibility":
        specs.extend(_source_credibility_specs(data))
    elif name == "sunk_cost":
        specs.extend(_sunk_cost_specs(data))
    elif name == "decoy":
        specs.extend(_decoy_specs(data))
    else:
        # Standard 2-condition experiments (framing, wording)
        for condition, versions in data["conditions"].items():
            for version, body in versions.items():
                specs.append(TrialSpec(
                    experiment=name,
                    version=version,
                    condition=condition,
                    format="plain",
                    item=None,
                    stimulus_text=body["prompt"].strip(),
                ))

    # Generalization scenarios (if present)
    for gen in data.get("generalization", []):
        for condition in ("gain", "loss", "high", "low", "allow", "forbid",
                          "paid", "free", "liked", "disliked",
                          "fraunhofer", "blog", "amazon"):
            if condition in gen:
                body = gen[condition]
                prompt = body["prompt"] if isinstance(body, dict) else body
                specs.append(TrialSpec(
                    experiment=name,
                    version="generalization",
                    condition=condition,
                    format="plain",
                    item=gen.get("name"),
                    stimulus_text=prompt.strip(),
                ))

    return specs


def _anchoring_specs(data: dict) -> list[TrialSpec]:
    """Anchoring has benchmark items, classic items, and a format mini-test."""
    specs = []
    # Benchmark items (exact Many Labs stimuli)
    for item_data in data.get("benchmark_items", []):
        for condition in ("high", "low"):
            specs.append(TrialSpec(
                experiment="anchoring",
                version="benchmark",
                condition=condition,
                format="plain",
                item=item_data["name"],
                stimulus_text=item_data[condition].strip(),
            ))
    # Classic items (debatable-answer replacements)
    for item_data in data["classic_items"]:
        for condition in ("high", "low"):
            specs.append(TrialSpec(
                experiment="anchoring",
                version="classic",
                condition=condition,
                format="plain",
                item=item_data["name"],
                stimulus_text=item_data[condition].strip(),
            ))
    # Product — plain
    for condition in ("high", "low"):
        specs.append(TrialSpec(
            experiment="anchoring",
            version="product",
            condition=condition,
            format="plain",
            item="monitoring_platform",
            stimulus_text=data["product"][condition]["plain"].strip(),
        ))
    # Product — format mini-test
    for fmt in ("json", "html", "markdown"):
        for condition in ("high", "low"):
            specs.append(TrialSpec(
                experiment="anchoring",
                version="product",
                condition=condition,
                format=fmt,
                item="monitoring_platform",
                stimulus_text=data["product"][condition][fmt].strip(),
            ))
    return specs


def _source_credibility_specs(data: dict) -> list[TrialSpec]:
    """Source credibility: classic (Many Labs quote) + product (review attribution)."""
    specs = []
    # Classic Many Labs version (Washington vs Bin Laden)
    for condition, body in data.get("classic_conditions", {}).items():
        specs.append(TrialSpec(
            experiment="source_credibility",
            version="classic",
            condition=condition,
            format="plain",
            item=None,
            stimulus_text=body["prompt"].strip(),
        ))
    # Product version (review attribution)
    review_text = data["review_text"].strip()
    for condition, body in data.get("product_conditions", {}).items():
        prompt = body["prompt"].replace("{review_text}", review_text).strip()
        specs.append(TrialSpec(
            experiment="source_credibility",
            version="product",
            condition=condition,
            format="plain",
            item=None,
            stimulus_text=prompt,
        ))
    return specs


def _sunk_cost_specs(data: dict) -> list[TrialSpec]:
    """Sunk cost: classic_paid, classic_free (Many Labs), and product."""
    specs = []
    for version_key, body in data["versions"].items():
        # Map version keys to version/condition pairs
        if version_key.startswith("classic_"):
            version = "classic"
            condition = body.get("condition", version_key.replace("classic_", ""))
        else:
            version = version_key
            condition = body.get("condition", "default")
        specs.append(TrialSpec(
            experiment="sunk_cost",
            version=version,
            condition=condition,
            format="plain",
            item=None,
            stimulus_text=body["prompt"].strip(),
        ))
    return specs


def _decoy_specs(data: dict) -> list[TrialSpec]:
    """Decoy effect: 20 product triads × 3 conditions."""
    specs = []
    for item in data["items"]:
        for condition in ("control", "decoy_premium", "decoy_budget"):
            specs.append(TrialSpec(
                experiment="decoy",
                version="product",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[condition].strip(),
            ))
    return specs


def get_all_trial_specs() -> list[TrialSpec]:
    """Load all experiments and return combined TrialSpec list."""
    experiments = ["framing", "anchoring", "sunk_cost", "source_credibility", "wording", "decoy"]
    all_specs = []
    for name in experiments:
        all_specs.extend(get_trial_specs(name))
    return all_specs


# --- Generalization stimuli (new YAML files, 1 rep each) ---

def _load_yaml_list(filename: str) -> list[dict]:
    """Load a bare YAML list file."""
    path = STIMULI_DIR / filename
    with open(path) as f:
        return yaml.safe_load(f)


def _gen_framing_specs() -> list[TrialSpec]:
    """Load framing generalization scenarios from new file."""
    items = _load_yaml_list("framing_generalization_new.yaml")
    specs = []
    for item in items:
        for condition in ("gain", "loss"):
            if condition in item:
                prompt = item[condition]["prompt"] if isinstance(item[condition], dict) else item[condition]
                specs.append(TrialSpec(
                    experiment="framing",
                    version="generalization",
                    condition=condition,
                    format="plain",
                    item=item.get("name"),
                    stimulus_text=prompt.strip(),
                ))
    return specs


def _gen_anchoring_specs() -> list[TrialSpec]:
    """Load anchoring items from new file."""
    items = _load_yaml_list("anchoring_new.yaml")
    specs = []
    for item in items:
        for condition in ("high", "low"):
            specs.append(TrialSpec(
                experiment="anchoring",
                version="generalization",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[condition].strip(),
            ))
    return specs


def _gen_sunk_cost_specs() -> list[TrialSpec]:
    """Load sunk cost scenarios from new file."""
    items = _load_yaml_list("sunk_cost_new.yaml")
    specs = []
    for item in items:
        for condition in ("paid", "free"):
            specs.append(TrialSpec(
                experiment="sunk_cost",
                version="generalization",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[condition]["prompt"].strip(),
            ))
    return specs


def _gen_source_credibility_specs() -> list[TrialSpec]:
    """Load source credibility scenarios from new file."""
    items = _load_yaml_list("source_credibility_new.yaml")
    specs = []
    for item in items:
        for condition, prompt_key in (("high", "prompt_high"), ("low", "prompt_low")):
            specs.append(TrialSpec(
                experiment="source_credibility",
                version="generalization",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[prompt_key].strip(),
            ))
    return specs


def _gen_wording_specs() -> list[TrialSpec]:
    """Load wording scenarios from new file."""
    items = _load_yaml_list("wording_new.yaml")
    specs = []
    for item in items:
        for condition in ("allow", "forbid"):
            specs.append(TrialSpec(
                experiment="wording",
                version="generalization",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[condition]["prompt"].strip(),
            ))
    return specs


def _gen_decoy_specs() -> list[TrialSpec]:
    """Load decoy triads from new file."""
    path = STIMULI_DIR / "decoy_new.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    # File may be a bare list or have a top-level 'items' key
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    specs = []
    for item in items:
        for condition in ("control", "decoy_premium", "decoy_budget"):
            specs.append(TrialSpec(
                experiment="decoy",
                version="generalization",
                condition=condition,
                format="plain",
                item=item["name"],
                stimulus_text=item[condition].strip(),
            ))
    return specs


def get_generalization_specs() -> list[TrialSpec]:
    """Load all generalization stimuli from the new YAML files."""
    specs = []
    specs.extend(_gen_framing_specs())
    specs.extend(_gen_anchoring_specs())
    specs.extend(_gen_sunk_cost_specs())
    specs.extend(_gen_source_credibility_specs())
    specs.extend(_gen_wording_specs())
    specs.extend(_gen_decoy_specs())
    return specs
