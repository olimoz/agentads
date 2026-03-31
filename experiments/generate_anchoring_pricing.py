"""Generate pricing anchoring stimuli from existing decoy triads.

Takes the Premium option specs from each decoy triad and creates
high/low anchor pricing questions. No "correct" price exists —
genuine uncertainty, unlike the factual estimation items.

Run: uv run python -m experiments.generate_anchoring_pricing
"""

import re
import yaml
from pathlib import Path

STIMULI_DIR = Path(__file__).resolve().parent / "stimuli"


def extract_specs_from_prompt(prompt: str, vendor_label: str = "Vendor B") -> dict | None:
    """Extract specs from a decoy control prompt for Vendor B (Premium)."""
    # Find the Vendor B section
    pattern = rf'\*\*{re.escape(vendor_label)}:.*?\*\*\n(.*?)(?:\n\n|\*\*Vendor|\Z)'
    match = re.search(pattern, prompt, re.DOTALL)
    if not match:
        return None

    specs_text = match.group(1).strip()
    lines = [l.strip().lstrip('- ') for l in specs_text.split('\n') if l.strip().startswith('-')]

    # Extract price
    price = None
    other_specs = []
    for line in lines:
        if any(p in line.lower() for p in ['price', '/month', '/seat', '/user', '/agent', '/host',
                                            '/endpoint', '/gb', '/tb', '/million']):
            price = line
        else:
            other_specs.append(line)

    return {"price_line": price, "specs": other_specs} if price else None


def parse_price_value(price_line: str) -> float | None:
    """Extract numeric price from a price line like 'Price/month: $2,400'."""
    match = re.search(r'[\$£]?([\d,]+(?:\.\d+)?)', price_line)
    if match:
        return float(match.group(1).replace(',', ''))
    return None


def make_anchoring_prompt(domain: str, specs: list[str], anchor_price: str, price_unit: str) -> str:
    """Create an anchoring prompt for a product category."""
    specs_formatted = "\n".join(f"- {s}" for s in specs)
    return (
        f"Your company is evaluating {domain} solutions. "
        f"{anchor_price}\n\n"
        f"A vendor has submitted a proposal with the following specifications:\n"
        f"{specs_formatted}\n\n"
        f"Based on these specifications, what would you expect to pay {price_unit}? "
        f"Provide a single number in dollars as your estimate."
    )


def generate():
    """Generate anchoring pricing YAML from decoy triads."""
    items = []

    for yaml_file in ["decoy.yaml", "decoy_new.yaml"]:
        path = STIMULI_DIR / yaml_file
        if not path.exists():
            continue
        with open(path) as f:
            data = yaml.safe_load(f)

        triad_list = data.get("items", data) if isinstance(data, (dict, list)) else []
        if isinstance(triad_list, dict):
            triad_list = triad_list.get("items", [])

        for triad in triad_list:
            name = triad["name"]
            domain = triad.get("domain", name.replace("_", " ").title())
            control = triad.get("control", "")

            specs = extract_specs_from_prompt(control)
            if not specs or not specs["price_line"]:
                continue

            price_val = parse_price_value(specs["price_line"])
            if not price_val or price_val <= 0:
                continue

            # Determine price unit from the price line
            price_line_lower = specs["price_line"].lower()
            if "/seat" in price_line_lower or "/user" in price_line_lower:
                price_unit = "per user per month"
            elif "/agent" in price_line_lower:
                price_unit = "per agent per month"
            elif "/endpoint" in price_line_lower:
                price_unit = "per endpoint per month"
            elif "/gb" in price_line_lower:
                price_unit = "per GB"
            elif "/tb" in price_line_lower:
                price_unit = "per TB"
            elif "/million" in price_line_lower:
                price_unit = "per million API calls"
            else:
                price_unit = "per month"

            # Create high and low anchors
            high_anchor = price_val * 5
            low_anchor = price_val * 0.1

            high_anchor_text = f"Enterprise {domain.lower()} solutions typically cost up to ${high_anchor:,.0f} {price_unit}."
            low_anchor_text = f"Basic {domain.lower()} tools start at ${low_anchor:,.0f} {price_unit}."

            high_prompt = make_anchoring_prompt(domain, specs["specs"], high_anchor_text, price_unit)
            low_prompt = make_anchoring_prompt(domain, specs["specs"], low_anchor_text, price_unit)

            items.append({
                "name": f"pricing_{name}",
                "domain": domain,
                "high": high_prompt,
                "low": low_prompt,
                "premium_price": price_val,
            })

    # Write YAML
    out_path = STIMULI_DIR / "anchoring_pricing.yaml"
    with open(out_path, "w") as f:
        yaml.dump(items, f, default_flow_style=False, width=200, allow_unicode=True)

    print(f"Generated {len(items)} pricing anchoring items -> {out_path}")
    for item in items[:3]:
        print(f"  {item['name']}: premium=${item['premium_price']:,.0f}")
        print(f"    high anchor: ...up to ${item['premium_price']*5:,.0f}...")
        print(f"    low anchor: ...start at ${item['premium_price']*0.1:,.0f}...")


if __name__ == "__main__":
    generate()
