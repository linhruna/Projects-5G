from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import load
from sklearn.metrics import mean_absolute_error, mean_squared_error


def _ensure_repo_on_syspath() -> None:
    # Allows running: python src/evaluate.py ...
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate a trained model on a CSV.")
    p.add_argument("--input", required=True, help="Path to evaluation CSV.")
    p.add_argument("--models", required=True, help="Directory containing model.joblib.")
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
    model_dir = Path(args.models)
    artifact_path = model_dir / "model.joblib"
    if not artifact_path.exists():
        raise SystemExit(f"Missing model artifact: {artifact_path}")

    artifact = load(artifact_path)
    model = artifact["model"]
    feature_cols = artifact["feature_columns"]
    target_col = artifact["target_column"]

    df = pd.read_csv(input_path)
    df = clean_data(df)
    if target_col not in df.columns:
        raise SystemExit(f"Evaluation data missing target column: {target_col}")

    df = _make_supervised_frame(df, target_col)
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise SystemExit(f"Evaluation data missing feature columns: {missing}")

    X = df[feature_cols].to_numpy(dtype=float)
    y = df["target_next"].to_numpy(dtype=float)
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)

    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    mse = mean_squared_error(y, preds)
    rmse = float(np.sqrt(mse))

    logger.info(f"MAE: {mae:.4f}")
    logger.info(f"RMSE: {rmse:.4f}")


if __name__ == "__main__":
    main()

