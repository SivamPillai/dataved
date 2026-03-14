"""Unit tests for core.anomaly_detection."""

import numpy as np
import pandas as pd
import pytest

from core.anomaly_detection import (
    detect_anomalies_iqr,
    detect_anomalies_loess,
    detect_anomalies_isolation_forest,
)


def test_detect_anomalies_iqr_basic():
    # Normal range ~0-10; 100 is clear outlier
    series = pd.Series([1, 2, 3, 4, 5, 100, 2, 3])
    mask = detect_anomalies_iqr(series)
    assert mask.sum() >= 1
    assert bool(mask[5])


def test_detect_anomalies_iqr_no_outliers():
    series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    mask = detect_anomalies_iqr(series)
    assert mask.sum() == 0


def test_detect_anomalies_iqr_returns_boolean_array():
    series = pd.Series([1, 2, 3])
    mask = detect_anomalies_iqr(series)
    assert len(mask) == 3
    assert mask.dtype == bool


def test_detect_anomalies_isolation_forest():
    series = pd.Series(np.random.randn(50).tolist() + [10.0])  # one outlier
    mask = detect_anomalies_isolation_forest(series, contamination=0.05)
    assert mask.shape[0] == 51
    assert mask.dtype == bool
