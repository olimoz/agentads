"""SQLite database schema and helpers."""

import sqlite3

import pandas as pd

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS trials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment TEXT NOT NULL,
    version TEXT NOT NULL,
    condition TEXT NOT NULL,
    format TEXT DEFAULT 'plain',
    item TEXT,
    model TEXT NOT NULL,
    rep INTEGER NOT NULL,
    stimulus_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    parsed_choice TEXT,
    parsed_numeric REAL,
    parse_method TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    latency_ms INTEGER,
    error TEXT,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS human_baselines (
    experiment TEXT NOT NULL,
    version TEXT NOT NULL,
    condition TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    source TEXT NOT NULL,
    PRIMARY KEY (experiment, version, condition, metric_name)
);

CREATE INDEX IF NOT EXISTS idx_trials_lookup
    ON trials(experiment, version, condition, format, item, model, rep);
"""

BASELINES = [
    # Framing — from Many Labs raw data (n=6,271 across 36 sites)
    ("framing", "classic", "gain", "pct_certain", 0.622, "many_labs_raw"),
    ("framing", "classic", "loss", "pct_certain", 0.335, "many_labs_raw"),
    ("framing", "classic", "overall", "effect_pp", 0.287, "many_labs_raw"),
    ("framing", "classic", "overall", "site_effect_min", 0.048, "many_labs_raw"),
    ("framing", "classic", "overall", "site_effect_max", 0.505, "many_labs_raw"),
    ("framing", "classic", "overall", "site_effect_mean", 0.291, "many_labs_raw"),
    # Anchoring — Many Labs used different items (Everest, SF-NY, Chicago, babies)
    # We replaced with debatable-answer items; ML effect sizes are directional reference
    ("anchoring", "classic", "overall", "many_labs_d_min", 1.159, "many_labs_raw"),
    ("anchoring", "classic", "overall", "many_labs_d_max", 2.298, "many_labs_raw"),
    ("anchoring", "classic", "overall", "many_labs_d_mean", 1.856, "many_labs_raw"),
    # Sunk cost — football ticket, 1-9 scale (paid vs free, between-subjects)
    ("sunk_cost", "classic", "paid", "mean_rating", 7.85, "many_labs_raw"),
    ("sunk_cost", "classic", "free", "mean_rating", 7.24, "many_labs_raw"),
    ("sunk_cost", "classic", "overall", "cohens_d", 0.272, "many_labs_raw"),
    ("sunk_cost", "classic", "overall", "site_d_min", -0.081, "many_labs_raw"),
    ("sunk_cost", "classic", "overall", "site_d_max", 0.680, "many_labs_raw"),
    # Source credibility / quote attribution — liked vs disliked source, 1-9 agreement
    ("source_credibility", "classic", "liked", "mean_rating", 5.928, "many_labs_raw"),
    ("source_credibility", "classic", "disliked", "mean_rating", 5.232, "many_labs_raw"),
    ("source_credibility", "classic", "overall", "cohens_d", 0.322, "many_labs_raw"),
    ("source_credibility", "classic", "overall", "site_d_min", -0.358, "many_labs_raw"),
    ("source_credibility", "classic", "overall", "site_d_max", 0.944, "many_labs_raw"),
    # Wording — allow vs forbid
    ("wording", "classic", "allow", "pct_yes", 0.763, "many_labs_raw"),
    ("wording", "classic", "forbid", "pct_yes", 0.072, "many_labs_raw"),
    ("wording", "classic", "overall", "sum_pct_yes", 0.835, "many_labs_raw"),
    ("wording", "classic", "overall", "site_effect_min", -0.510, "many_labs_raw"),
    ("wording", "classic", "overall", "site_effect_max", -0.050, "many_labs_raw"),
]


def init_db(path: str | None = None) -> sqlite3.Connection:
    """Create tables and populate baselines. Returns connection."""
    conn = sqlite3.connect(str(path or DB_PATH))
    conn.executescript(SCHEMA)
    for row in BASELINES:
        conn.execute(
            "INSERT OR IGNORE INTO human_baselines VALUES (?,?,?,?,?,?)", row
        )
    conn.commit()
    return conn


def insert_trial(conn: sqlite3.Connection, data: dict) -> int:
    """Insert a single trial record. Returns row id."""
    cols = [
        "experiment", "version", "condition", "format", "item",
        "model", "rep", "stimulus_text", "response_text",
        "parsed_choice", "parsed_numeric", "parse_method",
        "input_tokens", "output_tokens", "latency_ms",
        "error", "timestamp",
    ]
    placeholders = ",".join(["?"] * len(cols))
    values = [data.get(c) for c in cols]
    cur = conn.execute(
        f"INSERT INTO trials ({','.join(cols)}) VALUES ({placeholders})", values
    )
    conn.commit()
    return cur.lastrowid


def get_completed_trials(conn: sqlite3.Connection) -> set[tuple]:
    """Return set of (experiment, version, condition, format, item, model, rep) already done."""
    rows = conn.execute(
        "SELECT experiment, version, condition, format, item, model, rep "
        "FROM trials WHERE error IS NULL"
    ).fetchall()
    return set(rows)


def get_trials_df(conn: sqlite3.Connection) -> pd.DataFrame:
    """Load all trials into a DataFrame."""
    return pd.read_sql("SELECT * FROM trials WHERE error IS NULL", conn)


def get_baselines_df(conn: sqlite3.Connection) -> pd.DataFrame:
    """Load human baselines into a DataFrame."""
    return pd.read_sql("SELECT * FROM human_baselines", conn)
