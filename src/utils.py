"""
Utility functions for Kuta WasteSense AI.
Constants, mappings, and shared helpers.
"""

import os

# ── Zone definitions ──────────────────────────────────────────────────────────
ZONES = [
    "Beachwalk Area",
    "Main Beach Gate",
    "Food Vendor Area",
    "Parking Area",
    "Hotel Front Area",
    "Event Area",
    "Legian-side Beach Zone",
]

# Base waste multipliers per zone (relative to average)
ZONE_WASTE_MULTIPLIER = {
    "Beachwalk Area": 1.35,
    "Main Beach Gate": 1.10,
    "Food Vendor Area": 1.25,
    "Parking Area": 0.80,
    "Hotel Front Area": 0.95,
    "Event Area": 1.40,
    "Legian-side Beach Zone": 0.90,
}

# ── Categorical feature values ───────────────────────────────────────────────
DAY_TYPES = ["Weekday", "Weekend", "Public Holiday"]
WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Stormy"]
EVENT_TYPES = ["None", "Beach Festival", "Cultural Ceremony", "Music Concert", "Sports Event", "Market Day"]
SEASONS = ["Dry Season", "Wet Season", "Peak Tourist Season"]

# ── Operational capacity constants ────────────────────────────────────────────
STAFF_CAPACITY_KG = 300       # kg per staff per shift
BIN_CAPACITY_KG = 150         # kg per bin
TRUCK_CAPACITY_KG = 1500      # kg per truck

# ── Risk thresholds ───────────────────────────────────────────────────────────
RISK_LOW_MAX = 1000
RISK_MEDIUM_MAX = 3000

# ── Feature columns for the ML model ─────────────────────────────────────────
FEATURE_COLS = [
    "zone",
    "day_of_week",
    "is_weekend",
    "is_holiday",
    "weather_condition",
    "rainfall_mm",
    "event_type",
    "estimated_visitors",
    "season",
    "bin_availability",
    "previous_waste_kg",
]

TARGET_COL = "waste_volume_kg"

# ── Path helpers ──────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
DATASET_PATH = os.path.join(DATA_DIR, "kuta_waste_synthetic_dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "waste_model.pkl")


def ensure_dirs():
    """Create data/ and models/ directories if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)
