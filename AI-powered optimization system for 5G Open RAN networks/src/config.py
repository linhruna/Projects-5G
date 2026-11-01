from __future__ import annotations

import logging
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
LOGS_DIR = REPO_ROOT / "logs"
PREDICTIONS_DIR = REPO_ROOT / "predictions"

LOG_LEVEL = logging.INFO

