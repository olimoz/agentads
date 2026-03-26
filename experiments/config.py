"""Configuration and constants for the cognitive bias experiment."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STIMULI_DIR = Path(__file__).resolve().parent / "stimuli"
DB_PATH = PROJECT_ROOT / "results.db"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Experiment parameters
REPS = int(os.getenv("EXPERIMENT_REPS", "10"))
TEMPERATURE = float(os.getenv("EXPERIMENT_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("EXPERIMENT_MAX_TOKENS", "2000"))
SEED = int(os.getenv("RANDOM_SEED", "42"))

# Rate limits: max concurrent requests per provider
RATE_LIMITS = {
    "anthropic": 3,
    "openai": 5,
    "google": 5,
    "together": 5,
}

# Map model names to providers (for rate limiting)
MODEL_PROVIDERS = {
    "claude-opus-4.6": "anthropic",
    "gpt-5.4": "openai",
    "gemini-3.1-pro": "google",
    "glm-5": "together",
    "kimi-k2.5": "together",
}

SYSTEM_PROMPT = (
    "You are answering a survey question. "
    "Read the scenario carefully and respond with your choice, "
    "then briefly explain your reasoning."
)
