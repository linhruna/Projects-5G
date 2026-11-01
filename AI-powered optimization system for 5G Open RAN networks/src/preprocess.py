from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def _ensure_repo_on_syspath() -> None:
    # Allows running: python src/preprocess.py ...
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Preprocess raw network data CSV.")
    p.add_argument("--input", required=True, help="Path to input CSV.")
    p.add_argument("--output", required=True, help="Path to output CSV.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    _ensure_repo_on_syspath()

    from src.data_preparation.data_cleaning import clean_data
    from src.data_preparation.data_transformation import transform_data
    from src.utils.logger import get_logger

    logger = get_logger(__name__)

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Reading raw data: {input_path}")
    df = pd.read_csv(input_path)

    logger.info("Cleaning data")
    df = clean_data(df)

    logger.info("Transforming data")
    df = transform_data(df)

    logger.info(f"Writing preprocessed data: {output_path}")
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()

