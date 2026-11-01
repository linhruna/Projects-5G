import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

def make_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal prediction routine for the demo pipeline.
    If `traffic_load_mbps` exists, predict next-step traffic via a 1-step lag.
    Falls back to a constant prediction otherwise.
    """
    out = df.copy()

    if "traffic_load_mbps" in out.columns:
        out["predicted_traffic_load_mbps"] = out["traffic_load_mbps"].shift(-1)
        out["predicted_traffic_load_mbps"] = out["predicted_traffic_load_mbps"].fillna(out["traffic_load_mbps"])
    else:
        out["predicted_value"] = 0.0

    # Keep output compact
    keep = [c for c in ["timestamp", "cell_id", "predicted_traffic_load_mbps", "predicted_value"] if c in out.columns]
    if keep:
        return out[keep]
    return out

