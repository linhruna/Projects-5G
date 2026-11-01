from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import load


def _ensure_repo_on_syspath() -> None:
    # Allows running: python src/optimize.py ...
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run optimization using a trained model.")
    p.add_argument("--input", required=True, help="Path to real-time CSV.")
    p.add_argument("--models", required=True, help="Directory containing model.joblib.")
    p.add_argument("--output", required=True, help="Path to output CSV (optimized plan).")
    return p.parse_args()


def _resource_multiplier(predicted: np.ndarray) -> np.ndarray:
    # Simple heuristic: scale resources relative to max predicted load.
    denom = float(np.max(predicted)) if predicted.size else 1.0
    denom = denom if denom > 0 else 1.0
    mult = predicted / denom
    return np.clip(mult, 0.2, 1.0)


def main() -> None:
    args = _parse_args()
    _ensure_repo_on_syspath()

    from src.data_preparation.data_cleaning import clean_data
    from src.utils.logger import get_logger

    logger = get_logger(__name__)

    input_path = Path(args.input)
    model_dir = Path(args.models)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    artifact_path = model_dir / "model.joblib"
    if not artifact_path.exists():
        raise SystemExit(f"Missing model artifact: {artifact_path}")

    artifact = load(artifact_path)
    model = artifact["model"]
    feature_cols = artifact["feature_columns"]

    df = pd.read_csv(input_path)
    df = clean_data(df)

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise SystemExit(f"Input data missing feature columns: {missing}")

    X = df[feature_cols].to_numpy(dtype=float)
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    predicted_next = model.predict(X)

    mult = _resource_multiplier(predicted_next)

    out = pd.DataFrame(
        {
            "timestamp": df["timestamp"] if "timestamp" in df.columns else pd.RangeIndex(len(df)),
            "cell_id": df["cell_id"] if "cell_id" in df.columns else 0,
            "predicted_traffic_load_mbps_next": predicted_next,
            "suggested_resource_multiplier": mult,
        }
    )

    logger.info(f"Writing optimized output: {out_path}")
    out.to_csv(out_path, index=False)


if __name__ == "__main__":
    main()

