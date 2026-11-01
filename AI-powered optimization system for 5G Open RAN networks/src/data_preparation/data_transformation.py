import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lightweight transformation used by `src.main`:
    - keeps timestamp/cell_id as-is
    - MinMax scales numeric feature columns
    """
    out = df.copy()

    passthrough_cols = [c for c in ["timestamp", "cell_id"] if c in out.columns]
    feature_cols = [c for c in out.columns if c not in passthrough_cols]
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(out[c])]

    if numeric_cols:
        scaler = MinMaxScaler()
        out[numeric_cols] = scaler.fit_transform(out[numeric_cols])

    return out

