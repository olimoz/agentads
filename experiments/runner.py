"""Async trial runner with rate limiting and resume support."""

import asyncio
import random
import time
from datetime import datetime, timezone

from .config import MODEL_PROVIDERS, RATE_LIMITS, REPS, SEED
from .db import get_completed_trials, insert_trial
from .parsing import parse_response
from .stimuli import TrialSpec

# Semaphores created at run time
_semaphores: dict[str, asyncio.Semaphore] = {}


def _init_semaphores() -> None:
    for provider, limit in RATE_LIMITS.items():
        _semaphores[provider] = asyncio.Semaphore(limit)


async def run_single_trial(
    agent,
    model_name: str,
    spec: TrialSpec,
    rep: int,
    conn,
) -> dict:
    """Run one trial: call model, parse, store."""
    provider = MODEL_PROVIDERS[model_name]
    sem = _semaphores[provider]

    # Retry with exponential backoff
    last_error = None
    for attempt in range(3):
        async with sem:
            start = time.monotonic()
            try:
                result = await agent.run(spec.stimulus_text)
                latency_ms = int((time.monotonic() - start) * 1000)
                response_text = result.text
                usage = result.usage_details or {}
                break
            except Exception as e:
                latency_ms = int((time.monotonic() - start) * 1000)
                last_error = e
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
    else:
        # All retries failed
        trial_data = _make_trial_data(
            spec, model_name, rep,
            response_text="",
            usage={},
            latency_ms=latency_ms,
            parsed={},
            error=str(last_error),
        )
        insert_trial(conn, trial_data)
        return trial_data

    parsed = parse_response(response_text, spec)

    trial_data = _make_trial_data(
        spec, model_name, rep,
        response_text=response_text,
        usage=usage,
        latency_ms=latency_ms,
        parsed=parsed,
        error=None,
    )
    insert_trial(conn, trial_data)
    return trial_data


def _make_trial_data(
    spec: TrialSpec, model_name: str, rep: int,
    response_text: str, usage: dict, latency_ms: int,
    parsed: dict, error: str | None,
) -> dict:
    return {
        "experiment": spec.experiment,
        "version": spec.version,
        "condition": spec.condition,
        "format": spec.format,
        "item": spec.item,
        "model": model_name,
        "rep": rep,
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


async def run_all_trials(
    specs: list[TrialSpec],
    agents: dict,
    conn,
    n_reps: int | None = None,
) -> list[dict]:
    """Run all trials across all models and reps."""
    if n_reps is None:
        n_reps = REPS

    _init_semaphores()

    # Check what's already done (resume support)
    completed = get_completed_trials(conn)

    # Build task list
    tasks = []
    for spec in specs:
        for model_name, agent in agents.items():
            for rep in range(n_reps):
                key = (spec.experiment, spec.version, spec.condition,
                       spec.format, spec.item, model_name, rep)
                if key in completed:
                    continue
                tasks.append((agent, model_name, spec, rep))

    if not tasks:
        print("All trials already completed. Nothing to run.")
        return []

    # Shuffle to distribute load across providers
    rng = random.Random(SEED)
    rng.shuffle(tasks)

    total = len(tasks)
    print(f"Running {total} trials ({len(completed)} already completed)...")

    # Create coroutines and gather
    async def _run(idx, agent, model_name, spec, rep):
        result = await run_single_trial(agent, model_name, spec, rep, conn)
        if (idx + 1) % 50 == 0 or (idx + 1) == total:
            errors = "error" if result.get("error") else "ok"
            print(f"  [{idx + 1}/{total}] {spec.experiment}/{model_name} rep={rep} — {errors}")
        return result

    coros = [
        _run(i, agent, model_name, spec, rep)
        for i, (agent, model_name, spec, rep) in enumerate(tasks)
    ]

    results = await asyncio.gather(*coros, return_exceptions=True)

    # Report summary
    ok = sum(1 for r in results if isinstance(r, dict) and not r.get("error"))
    failed = sum(1 for r in results if isinstance(r, dict) and r.get("error"))
    exceptions = sum(1 for r in results if isinstance(r, Exception))
    print(f"\nDone: {ok} succeeded, {failed} API errors, {exceptions} exceptions")

    return [r for r in results if isinstance(r, dict)]
