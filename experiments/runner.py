"""Async trial runner with rate limiting and resume support."""

import asyncio
import random
import time
from datetime import datetime, timezone

from collections import defaultdict

from .config import CALL_BUDGETS, MODEL_CONCURRENCY, MODEL_PROVIDERS, REPS, SEED
from .db import get_completed_trials, insert_trial
from .parsing import parse_response
from .stimuli import TrialSpec

# Per-model semaphores (created at run time)
_semaphores: dict[str, asyncio.Semaphore] = {}


def _init_semaphores(model_names: list[str]) -> None:
    for model_name in model_names:
        limit = MODEL_CONCURRENCY.get(model_name, 5)
        _semaphores[model_name] = asyncio.Semaphore(limit)


async def run_single_trial(
    agent,
    model_name: str,
    spec: TrialSpec,
    rep: int,
    conn,
) -> dict:
    """Run one trial: call model, parse, store."""
    sem = _semaphores[model_name]

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

    _init_semaphores(list(agents.keys()))

    # Check what's already done (resume support)
    completed = get_completed_trials(conn)

    # Build task list, applying per-model call budgets
    unlimited_tasks = []
    # For budget-limited models, group by experiment for round-robin
    budgeted_by_experiment: dict[str, dict[str, list]] = defaultdict(
        lambda: defaultdict(list)
    )

    for spec in specs:
        for model_name, agent in agents.items():
            for rep in range(n_reps):
                key = (spec.experiment, spec.version, spec.condition,
                       spec.format, spec.item, model_name, rep)
                if key in completed:
                    continue
                budget = CALL_BUDGETS.get(model_name)
                if budget is None:
                    unlimited_tasks.append((agent, model_name, spec, rep))
                else:
                    budgeted_by_experiment[model_name][spec.experiment].append(
                        (agent, model_name, spec, rep)
                    )

    # Round-robin selection for budget-limited models
    budgeted_tasks = []
    for model_name, by_experiment in budgeted_by_experiment.items():
        budget = CALL_BUDGETS[model_name]
        # Shuffle within each experiment for variety
        rng = random.Random(SEED)
        queues = {}
        for exp, exp_tasks in by_experiment.items():
            rng.shuffle(exp_tasks)
            queues[exp] = list(exp_tasks)

        # Round-robin across experiments until budget exhausted
        selected = []
        experiment_names = sorted(queues.keys())
        idx = 0
        while len(selected) < budget and any(queues.values()):
            exp = experiment_names[idx % len(experiment_names)]
            if queues.get(exp):
                selected.append(queues[exp].pop(0))
            idx += 1
            # Remove exhausted experiments
            experiment_names = [e for e in experiment_names if queues.get(e)]
            if not experiment_names:
                break

        skipped = sum(len(q) for q in queues.values())
        print(f"  {model_name}: {len(selected)} trials selected "
              f"(budget={budget}, {skipped} deferred)")
        budgeted_tasks.extend(selected)

    tasks = unlimited_tasks + budgeted_tasks

    if not tasks:
        print("All trials already completed. Nothing to run.")
        return []

    # Shuffle to distribute load across providers
    rng = random.Random(SEED)
    rng.shuffle(tasks)

    total = len(tasks)

    # Count planned trials per model
    model_planned = defaultdict(int)
    for _, model_name, _, _ in tasks:
        model_planned[model_name] += 1
    print(f"Running {total} trials ({len(completed)} already completed)...")
    for m, n in sorted(model_planned.items()):
        budget_info = f" (budget: {CALL_BUDGETS[m]})" if CALL_BUDGETS.get(m) else ""
        print(f"  {m}: {n} trials{budget_info}")

    # Per-model progress tracking
    model_ok = defaultdict(int)
    model_err = defaultdict(int)
    done_count = 0

    # Create coroutines and gather
    async def _run(agent, model_name, spec, rep):
        nonlocal done_count
        result = await run_single_trial(agent, model_name, spec, rep, conn)
        done_count += 1

        if result.get("error"):
            model_err[model_name] += 1
        else:
            model_ok[model_name] += 1

        if done_count % 10 == 0 or done_count == total:
            status = " | ".join(
                f"{m}: {model_ok[m]}/{model_planned[m]}"
                + (f" ({model_err[m]} err)" if model_err[m] else "")
                for m in sorted(model_planned)
            )
            print(f"  [{done_count}/{total}] {status}")
        return result

    coros = [
        _run(agent, model_name, spec, rep)
        for agent, model_name, spec, rep in tasks
    ]

    results = await asyncio.gather(*coros, return_exceptions=True)

    # Report summary
    ok = sum(1 for r in results if isinstance(r, dict) and not r.get("error"))
    failed = sum(1 for r in results if isinstance(r, dict) and r.get("error"))
    exceptions = sum(1 for r in results if isinstance(r, Exception))
    print(f"\nDone: {ok} succeeded, {failed} API errors, {exceptions} exceptions")
    for m in sorted(model_planned):
        print(f"  {m}: {model_ok[m]} ok, {model_err[m]} errors")

    return [r for r in results if isinstance(r, dict)]
