"""Entry point: python -m experiments [--pilot] [--analyze] [--parse-cleanup]"""

import argparse
import asyncio
import sys

from .analysis import analyze_all, print_summary
from .db import get_trials_df, init_db
from .plots import plot_all
from .stimuli import get_all_trial_specs, get_trial_specs


def parse_args():
    parser = argparse.ArgumentParser(description="Cognitive bias experiment harness")
    parser.add_argument("--pilot", action="store_true",
                        help="Run 1 rep of framing only (8 trials) to verify setup")
    parser.add_argument("--analyze", action="store_true",
                        help="Skip trials; run analysis on existing results.db")
    parser.add_argument("--reps", type=int, default=None,
                        help="Override number of reps per cell")
    return parser.parse_args()


async def run_trials(pilot: bool = False, reps: int | None = None):
    """Run experiment trials."""
    from .models import create_agents
    from .runner import run_all_trials

    conn = init_db()

    print("Creating model agents...")
    agents = create_agents()
    print(f"  {len(agents)} agents ready: {', '.join(agents.keys())}")

    if pilot:
        print("\n--- PILOT MODE: framing experiment, 1 rep ---")
        specs = get_trial_specs("framing")
        n_reps = 1
    else:
        specs = get_all_trial_specs()
        n_reps = reps

    print(f"  {len(specs)} unique stimuli loaded")
    total = len(specs) * len(agents) * (n_reps or 10)
    print(f"  {total} total trials planned\n")

    await run_all_trials(specs, agents, conn, n_reps=n_reps)
    conn.close()


def run_analysis():
    """Analyze existing results and generate plots."""
    conn = init_db()
    df = get_trials_df(conn)

    if df.empty:
        print("No trial data found in results.db. Run trials first.")
        sys.exit(1)

    print(f"Loaded {len(df)} trials from results.db")
    print(f"  Models: {df['model'].unique().tolist()}")
    print(f"  Experiments: {df['experiment'].unique().tolist()}")

    # Parse success rate
    total = len(df)
    parsed = df["parsed_choice"].notna().sum()
    print(f"  Parse rate: {parsed}/{total} ({parsed/total:.0%})")

    results = analyze_all(df)
    print_summary(results)
    plot_all(results)
    conn.close()


def main():
    args = parse_args()

    if args.analyze:
        run_analysis()
    else:
        asyncio.run(run_trials(pilot=args.pilot, reps=args.reps))
        # Auto-analyze after running
        print("\n--- Running analysis ---")
        run_analysis()


if __name__ == "__main__":
    main()
