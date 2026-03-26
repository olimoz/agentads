"""Retry just the Gemini tailored ad test.

Run when quota resets: uv run python -m experiments.demo_gemini_retry
"""

import asyncio
import json
import os

import os

from .config import SYSTEM_PROMPT
from .models import create_agents
from .demo_tailored_ads import PLAIN, ADS, parse_choice


async def run():
    from agent_framework.openai import OpenAIChatClient

    agents = create_agents()
    gemini = agents["gemini-3.1-pro"]

    # Also prepare 2.5-pro as fallback (separate daily quota)
    fallback = OpenAIChatClient(
        model_id="gemini-2.5-pro",
        api_key=os.environ.get("GOOGLE_API_KEY", ""),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    ).as_agent(
        name="evaluator",
        instructions=SYSTEM_PROMPT,
        default_options={"temperature": 0.7, "max_tokens": 2000},
    )

    print("=" * 74)
    print("  GEMINI — TAILORED AD TEST")
    print("=" * 74)

    # Phase 1: Plain — try 3.1, fall back to 2.5
    model_used = "gemini-3.1-pro"
    print("\nPlain offer:")
    try:
        r = await gemini.run(PLAIN)
    except Exception:
        print("  3.1 Pro quota hit — falling back to Gemini 2.5 Pro")
        model_used = "gemini-2.5-pro"
        r = await fallback.run(PLAIN)
    plain_choice = parse_choice(r.text, model_used)
    print(f"  Model: {model_used}")
    print(f"  Result: {plain_choice}")
    print(f"  Response: {r.text[:200].replace(chr(10), ' ')}")

    # Phase 2: Tailored ad
    ad = ADS["gemini-3.1-pro"]
    print(f"\nTailored ad ({ad['technique']}):")
    try:
        r = await gemini.run(ad["ad"])
    except Exception:
        print("  3.1 Pro quota hit — falling back to Gemini 2.5 Pro")
        model_used = "gemini-2.5-pro"
        r = await fallback.run(ad["ad"])
    ad_choice = parse_choice(r.text, model_used)
    flipped = "FLIPPED" if "YES" in ad_choice and "NO" in plain_choice else ""
    print(f"  Model: {model_used}")
    print(f"  Result: {ad_choice} {flipped}")
    print(f"  Response: {r.text[:300].replace(chr(10), ' ')}")

    # Update saved results
    results_path = "outputs/demo_tailored_ads.json"
    if os.path.exists(results_path):
        with open(results_path) as f:
            data = json.load(f)
        data["plain"][model_used] = plain_choice
        data["tailored"][model_used] = {
            "choice": ad_choice,
            "technique": ad["technique"],
            "response": r.text,
        }
        with open(results_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"\nUpdated {results_path}")

    # Full summary
    print()
    print("=" * 74)
    print("  COMPLETE RESULTS (ALL 5 MODELS)")
    print("=" * 74)
    if os.path.exists(results_path):
        with open(results_path) as f:
            data = json.load(f)
        print(f"  {'Model':<22} {'Plain':>8} {'Tailored Ad':>30} {'Flipped?':>10}")
        print("  " + "-" * 72)
        for model in ["claude-opus-4.6", "gpt-5.4", "gemini-3.1-pro", "glm-5", "kimi-k2.5"]:
            p = data["plain"].get(model, "?")
            t = data["tailored"].get(model, {}).get("choice", "?")
            f = "YES <--" if "YES" in t and "NO" in p else "no"
            print(f"  {model:<22} {p:>8} {t:>30} {f:>10}")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
