from __future__ import annotations

import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent
DATASET_PATH = PROJECT_ROOT / "data" / "kuta_waste_synthetic_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "waste_model.pkl"


def ensure_project_root_on_path() -> None:
    project_root = str(PROJECT_ROOT)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
