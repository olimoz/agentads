"""Run Gemini-only on shared items that other models have completed but Gemini hasn't.

Prioritises items that all 4 non-Gemini models share, ensuring the downsampled
n per model is maximised. No repeated stimuli — every trial is unique.

Budget: 250 calls (Gemini daily limit).

Run: uv run python -m experiments.run_gemini_catchup
"""

import asyncio
import sqlite3
import time
from datetime import datetime, timezone

from .config import DB_PATH, SYSTEM_PROMPT
from .db import init_db, insert_trial
from .models import create_agents
from .parsing import parse_response
from .stimuli import get_trial_specs, TrialSpec


def find_priority_tasks(conn):
    """Find item×condition combos shared by all other models but missing from Gemini."""
    other_models = ['claude-opus-4.6', 'gpt-5.4', 'glm-5', 'kimi-k2.5']
    experiments = [
        ('anchoring', 'pricing_gen'),         # pricing anchoring (65 items)
        ('wording', 'generalization'),
        ('anchoring', 'generalization'),
        ('sunk_cost', 'generalization'),
        ('decoy', 'generalization'),
        ('source_credibility', 'generalization'),
        ('framing', 'generalization'),
    ]

    # What Gemini has already completed (deduplicated)
    gemini_done = set()
    rows = conn.execute(
        "SELECT experiment, version, condition, item "
        "FROM trials WHERE model='gemini-3.1-pro' AND error IS NULL"
    ).fetchall()
    for r in rows:
        gemini_done.add(r)

    priority_keys = []  # (experiment, version, condition, item)

    for exp, ver in experiments:
        # Find items shared by all 4 non-Gemini models
        item_sets = []
        for m in other_models:
            items = set()
            rows = conn.execute(
                "SELECT DISTINCT item FROM trials "
                "WHERE experiment=? AND version=? AND model=? AND error IS NULL",
                (exp, ver, m)
            ).fetchall()
            for r in rows:
                items.add(r[0])
            item_sets.append(items)

        shared_items = item_sets[0]
        for s in item_sets[1:]:
            shared_items = shared_items & s

        # Find conditions for this experiment
        conds = set()
        rows = conn.execute(
            "SELECT DISTINCT condition FROM trials "
            "WHERE experiment=? AND version=? AND error IS NULL",
            (exp, ver)
        ).fetchall()
        for r in rows:
            conds.add(r[0])

        # Find which shared item×condition Gemini is missing
        for item in sorted(shared_items):
            for cond in sorted(conds):
                key = (exp, ver, cond, item)
                if key not in gemini_done:
                    priority_keys.append(key)

    return priority_keys


async def run():
    conn = init_db()

    # Find priority tasks
    priority_keys = find_priority_tasks(conn)
    print(f"Found {len(priority_keys)} shared item×condition combos Gemini is missing")

    # Count by experiment
    from collections import Counter
    by_exp = Counter(k[0] for k in priority_keys)
    for exp, n in by_exp.most_common():
        print(f"  {exp}: {n}")
    print()

    if not priority_keys:
        print("Nothing to run — Gemini has all shared items.")
        conn.close()
        return

    # Load stimuli — generalization specs come from separate YAML files
    from .stimuli import get_generalization_specs
    all_specs = {}
    # Generalization stimuli
    for spec in get_generalization_specs():
        key = (spec.experiment, spec.version, spec.condition, spec.item)
        all_specs[key] = spec
    # Also load product decoy (version='product' not 'generalization' in some triads)
    for spec in get_trial_specs('decoy'):
        key = (spec.experiment, spec.version, spec.condition, spec.item)
        all_specs[key] = spec

    tasks = []
    missing_specs = 0
    for key in priority_keys:
        spec = all_specs.get(key)
        if spec:
            tasks.append(spec)
        else:
            missing_specs += 1

    if missing_specs:
        print(f"Warning: {missing_specs} priority items have no matching stimulus in YAML")

    # Cap at 245 for safety margin
    if len(tasks) > 245:
        print(f"Capping at 245 trials (from {len(tasks)})")
        tasks = tasks[:245]

    # Create Gemini agent only
    all_agents = create_agents()
    agent = all_agents["gemini-3.1-pro"]

    print(f"Running {len(tasks)} Gemini trials (shared items only, no repeats)...")
    print()

    ok = 0
    errors = 0
    for i, spec in enumerate(tasks):
        start = time.monotonic()
        try:
            result = await agent.run(spec.stimulus_text)
            latency_ms = int((time.monotonic() - start) * 1000)
            response_text = result.text
            usage = result.usage_details or {}
            parsed = parse_response(response_text, spec)
            error = None
            ok += 1
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            response_text = ""
            usage = {}
            parsed = {}
            error = str(e)
            errors += 1

            if "429" in str(e) or "quota" in str(e).lower():
                print(f"  [{i+1}/{len(tasks)}] RATE LIMITED — stopping")
                break

        trial_data = {
            "experiment": spec.experiment,
            "version": spec.version,
            "condition": spec.condition,
            "format": spec.format,
            "item": spec.item,
            "model": "gemini-3.1-pro",
            "rep": 0,
            "stimulus_text": spec.stimulus_text,
            "response_text": response_text,
            "parsed_choice": parsed.get("parsed_choice"),
            "parsed_numeric": parsed.get("parsed_numeric"),
            "parse_method": parsed.get("parse_method"),
            "input_tokens": usage.get("input_token_count"),
            "output_tokens": usage.get("output_token_count"),
            "latency_ms": latency_ms,
            "error": error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        insert_trial(conn, trial_data)

        if (i + 1) % 10 == 0 or (i + 1) == len(tasks):
            print(f"  [{i+1}/{len(tasks)}] ok={ok} err={errors} "
                  f"({spec.experiment}/{spec.condition}/{spec.item})")

    conn.close()

    print(f"\nDone: {ok} ok, {errors} errors")
    print(f"Rerun chart: uv run python experiments/chart_susceptibility.py")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
