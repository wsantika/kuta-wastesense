"""
Train waste volume prediction model (Random Forest Regressor).
Saves trained pipeline to models/waste_model.pkl.
Run: python src/train_model.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import FEATURE_COLS, TARGET_COL, DATASET_PATH, MODEL_PATH, ensure_dirs


# Separate categorical and numerical features
CAT_FEATURES = ["zone", "weather_condition", "event_type", "season"]
NUM_FEATURES = [c for c in FEATURE_COLS if c not in CAT_FEATURES]


def build_pipeline(model_type: str = "rf") -> Pipeline:
    """Build a sklearn pipeline with preprocessing + model."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_FEATURES),
            ("num", StandardScaler(), NUM_FEATURES),
        ],
        remainder="drop",
    )

    if model_type == "lr":
        model = LinearRegression()
    else:
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=18,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1,
        )

    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def train(model_type: str = "rf"):
    ensure_dirs()

    # -- Load data ---------------------------------------------------------
    print(f"[*] Loading dataset from {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Rows: {len(df):,}")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # -- Train / test split ------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )

    # -- Optional baseline: Linear Regression --
    print("\n-- Linear Regression (baseline) --")
    lr_pipe = build_pipeline("lr")
    lr_pipe.fit(X_train, y_train)
    y_pred_lr = lr_pipe.predict(X_test)
    lr_mae = mean_absolute_error(y_test, y_pred_lr)
    lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    print(f"   MAE  = {lr_mae:.2f} kg")
    print(f"   RMSE = {lr_rmse:.2f} kg")

    # -- Main model: Random Forest -----------------------------------------
    print("\n-- Random Forest Regressor (main) --")
    rf_pipe = build_pipeline("rf")
    rf_pipe.fit(X_train, y_train)
    y_pred_rf = rf_pipe.predict(X_test)
    rf_mae = mean_absolute_error(y_test, y_pred_rf)
    rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    print(f"   MAE  = {rf_mae:.2f} kg")
    print(f"   RMSE = {rf_rmse:.2f} kg")

    # -- Save best model ---------------------------------------------------
    joblib.dump(rf_pipe, MODEL_PATH)
    print(f"\n[OK] Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
