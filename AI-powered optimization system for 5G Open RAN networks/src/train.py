from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def _ensure_repo_on_syspath() -> None:
    # Allows running: python src/train.py ...
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train a simple model for predictive planning.")
    p.add_argument("--input", required=True, help="Path to training CSV.")
    p.add_argument("--output", required=True, help="Directory to write trained model artifacts.")
    p.add_argument("--target", default="traffic_load_mbps", help="Target column to predict (default: traffic_load_mbps).")
    p.add_argument("--random-state", type=int, default=42)
    return p.parse_args()


def _make_supervised_frame(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    out = df.copy()
    if "cell_id" in out.columns:
        out["target_next"] = out.groupby("cell_id")[target_col].shift(-1)
    else:
        out["target_next"] = out[target_col].shift(-1)
    out = out.dropna(subset=["target_next"])
    return out


def main() -> None:
    args = _parse_args()
    _ensure_repo_on_syspath()

    from src.data_preparation.data_cleaning import clean_data
    from src.utils.logger import get_logger

    logger = get_logger(__name__)

    input_path = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Reading training data: {input_path}")
    df = pd.read_csv(input_path)
    df = clean_data(df)

    if args.target not in df.columns:
        raise SystemExit(f"Target column not found: {args.target}. Columns: {list(df.columns)}")

    df = _make_supervised_frame(df, args.target)

    # Build numeric feature matrix
    numeric_cols = [c for c in df.columns if c not in ["timestamp", "target_next"] and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise SystemExit("No numeric feature columns found to train on.")

    X = df[numeric_cols].to_numpy(dtype=float)
    y = df["target_next"].to_numpy(dtype=float)

    # Handle any NaNs/infs just in case
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.25, random_state=args.random_state
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=args.random_state,
        n_jobs=-1,
    )

    logger.info(f"Training model on {X_train.shape[0]} rows; validating on {X_val.shape[0]} rows")
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    logger.info(f"Validation MAE: {mae:.4f}")

    artifact = {
        "model": model,
        "feature_columns": numeric_cols,
        "target_column": args.target,
    }

    model_path = out_dir / "model.joblib"
    dump(artifact, model_path)
    logger.info(f"Wrote model: {model_path}")


if __name__ == "__main__":
    main()

