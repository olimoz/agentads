"""Response parsing — regex first pass, LLM-as-judge fallback."""

import re

from .stimuli import TrialSpec


def parse_response(response_text: str, spec: TrialSpec) -> dict:
    """Parse a model response into structured data.

    Returns dict with keys: parsed_choice, parsed_numeric, parse_method.
    """
    text = response_text.strip()
    if not text:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    parsers = {
        "framing": _parse_framing,
        "anchoring": _parse_anchoring,
        "sunk_cost": _parse_sunk_cost,
        "decoy": _parse_decoy,
        "source_credibility": _parse_source_credibility,
        "wording": _parse_wording,
    }
    parser = parsers.get(spec.experiment)
    if parser:
        return parser(text, spec)
    return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}


def _parse_framing(text: str, spec: TrialSpec) -> dict:
    """Extract Program/Option A or B choice."""
    lower = text.lower()
    # Check for explicit program/option/plan mentions
    if spec.version == "classic":
        a_pattern = r'\bprogram\s*a\b'
        b_pattern = r'\bprogram\s*b\b'
    elif spec.version == "generalization":
        a_pattern = r'\bplan\s*a\b'
        b_pattern = r'\bplan\s*b\b'
    else:
        a_pattern = r'\boption\s*a\b'
        b_pattern = r'\boption\s*b\b'

    has_a = bool(re.search(a_pattern, lower))
    has_b = bool(re.search(b_pattern, lower))

    if has_a and not has_b:
        choice = "A"
    elif has_b and not has_a:
        choice = "B"
    elif has_a and has_b:
        # Both mentioned — take whichever appears first as the choice
        pos_a = re.search(a_pattern, lower).start()
        pos_b = re.search(b_pattern, lower).start()
        # Look for "I choose X" or "I would choose X" patterns
        choose_a = re.search(r'(?:choose|pick|select|recommend|go with)\s+(?:program|option|plan)\s*a\b', lower)
        choose_b = re.search(r'(?:choose|pick|select|recommend|go with)\s+(?:program|option|plan)\s*b\b', lower)
        if choose_a and not choose_b:
            choice = "A"
        elif choose_b and not choose_a:
            choice = "B"
        else:
            # Fallback: first mentioned is usually the answer
            choice = "A" if pos_a < pos_b else "B"
    else:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    return {"parsed_choice": choice, "parsed_numeric": None, "parse_method": "regex"}


def _parse_anchoring(text: str, spec: TrialSpec) -> dict:
    """Extract numerical estimate."""
    # Find all numbers (with commas, decimals)
    numbers = re.findall(r'[\d,]+(?:\.\d+)?', text)
    if not numbers:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    # Parse numbers, removing commas
    parsed = []
    for n in numbers:
        try:
            val = float(n.replace(",", ""))
            if val > 0:
                parsed.append(val)
        except ValueError:
            continue

    if not parsed:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    # For anchoring, we want the estimate (not the anchor).
    # Heuristic: take the last substantial number mentioned (models tend to
    # restate the anchor first, then give their estimate).
    # Filter out very small numbers that are likely not estimates (e.g., fractions)
    candidates = [n for n in parsed if n >= 10]
    if not candidates:
        candidates = parsed

    estimate = candidates[-1]
    return {
        "parsed_choice": str(int(estimate)),
        "parsed_numeric": estimate,
        "parse_method": "regex",
    }


def _parse_sunk_cost(text: str, spec: TrialSpec) -> dict:
    """Extract sunk cost response.

    Classic (Many Labs): 1-9 scale (1=stay home, 9=go to game).
    Higher = more sunk cost behaviour (going despite cold because you paid).
    Product: binary choice (switch to Vendor B = rational, stay = sunk cost).
    """
    lower = text.lower()

    if spec.version in ("classic", "generalization"):
        # Extract a 1-9 rating (both classic and generalization use this scale)
        matches = re.findall(r'\b([1-9])\b', text[:200])
        if matches:
            val = int(matches[0])
            return {
                "parsed_choice": str(val),
                "parsed_numeric": float(val),
                "parse_method": "regex",
            }
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}
    else:
        # Product version: Vendor A = sunk cost, Vendor B = rational
        if "switch to vendor b" in lower or "recommend switching" in lower:
            choice = "rational"
        elif "stay with vendor a" in lower or "recommend staying" in lower:
            choice = "sunk_cost"
        elif "switch" in lower and "vendor b" in lower:
            choice = "rational"
        elif "stay" in lower and "vendor a" in lower:
            choice = "sunk_cost"
        elif "switch" in lower:
            choice = "rational"
        elif "stay" in lower:
            choice = "sunk_cost"
        else:
            return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

        return {"parsed_choice": choice, "parsed_numeric": None, "parse_method": "regex"}


def _parse_source_credibility(text: str, spec: TrialSpec) -> dict:
    """Extract 1-10 rating."""
    # Look for a number 1-10 early in the response
    matches = re.findall(r'\b(\d{1,2})\b', text[:300])
    for m in matches:
        val = int(m)
        if 1 <= val <= 10:
            return {
                "parsed_choice": str(val),
                "parsed_numeric": float(val),
                "parse_method": "regex",
            }
    return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}


def _parse_wording(text: str, spec: TrialSpec) -> dict:
    """Extract yes/no answer."""
    # Check first 150 chars for a clear yes/no
    opening = text[:150].lower()

    # Look for explicit yes/no
    yes_match = re.search(r'\byes\b', opening)
    no_match = re.search(r'\bno\b', opening)

    if yes_match and not no_match:
        choice = "yes"
    elif no_match and not yes_match:
        choice = "no"
    elif yes_match and no_match:
        # Both present — take whichever comes first
        choice = "yes" if yes_match.start() < no_match.start() else "no"
    else:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    return {"parsed_choice": choice, "parsed_numeric": None, "parse_method": "regex"}


def _parse_decoy(text: str, spec: TrialSpec) -> dict:
    """Extract Vendor A/B/C/D choice."""
    lower = text[:300].lower()

    # Look for "vendor X" patterns
    vendors = {}
    for letter in ("a", "b", "c", "d"):
        match = re.search(rf'\bvendor\s*{letter}\b', lower)
        if match:
            vendors[letter] = match.start()

    if not vendors:
        return {"parsed_choice": None, "parsed_numeric": None, "parse_method": "failed"}

    # Look for decision language: "recommend vendor X", "choose vendor X"
    for letter in vendors:
        if re.search(rf'(?:recommend|choose|select|go with|pick)\s+vendor\s*{letter}\b', lower):
            return {"parsed_choice": letter.upper(), "parsed_numeric": None, "parse_method": "regex"}

    # Fallback: first vendor mentioned is usually the choice
    first = min(vendors, key=vendors.get)
    return {"parsed_choice": first.upper(), "parsed_numeric": None, "parse_method": "regex"}
