"""Pure anomaly detection algorithms (no Streamlit)."""

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from statsmodels.nonparametric.smoothers_lowess import lowess
from loguru import logger

def detect_anomalies_iqr(series: pd.Series) -> np.ndarray:
    """IQR-based anomaly detection. Returns boolean mask (True = anomaly)."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return ((series < lower) | (series > upper)).values


def detect_anomalies_loess(
    series: pd.Series, frac: float = 0.1, n_std: float = 3.0
) -> np.ndarray:
    """LOESS-based anomaly detection. Returns boolean mask (True = anomaly)."""
    try:
        y = np.asarray(series.values, dtype=float)
        y = y[~np.isnan(y)]
        if len(y) < 2:
            return np.zeros(len(series), dtype=bool)
        x = np.arange(len(y), dtype=float)
        fitted = lowess(y, x, frac=frac, return_sorted=True)
        y_fit = np.interp(x, fitted[:, 0], fitted[:, 1])
        resid = np.abs(y - y_fit)
        std_resid = np.nanstd(resid)
        if std_resid > 0 and np.isfinite(std_resid):
            threshold = std_resid * n_std
        else:
            threshold = np.nanpercentile(resid, 99) if np.any(np.isfinite(resid)) else 0
        out = np.zeros(len(series), dtype=bool)
        valid_idx = np.where(~np.isnan(series.values))[0]
        out[valid_idx] = resid > threshold
        return out

    except Exception as e:
            logger.exception(f"Failed with exception: {e}")
            return np.zeros(len(series), dtype=bool)
    


def detect_anomalies_isolation_forest(
    series: pd.Series, contamination: float = 0.05
) -> np.ndarray:
    """Isolation Forest anomaly detection. Returns boolean mask (True = anomaly)."""
    try:
        y = np.asarray(series.values, dtype=float)
        valid = ~np.isnan(y)
        if np.sum(valid) < 2:
            return np.zeros(len(series), dtype=bool)
        X = y[valid].reshape(-1, 1)
        clf = IsolationForest(contamination=min(contamination, 0.49), random_state=42)
        pred = clf.fit_predict(X)
        out = np.zeros(len(series), dtype=bool)
        out[valid] = pred == -1
        return out

    except Exception as e:
        logger.exception(f"Failed with exception: {e}")
        return np.zeros(len(series), dtype=bool)
    
