"""Shared pytest fixtures for data-dashboard tests."""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Project root (data-dashboard) on path so app, core, services, charts import
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_df():
    """DataFrame with DatetimeIndex and numeric columns for chart tests."""
    import numpy as np

    dates = pd.date_range("2025-01-01", periods=100, freq="1h", tz="Asia/Kolkata")
    return pd.DataFrame(
        {
            "cur1": np.random.randn(100).cumsum() + 10,
            "cur2": np.random.randn(100).cumsum() + 20,
            "vol1": np.random.rand(100) * 5,
        },
        index=dates,
    )


@pytest.fixture
def sample_csv_bytes():
    """Minimal CSV bytes with timestamp column for parse_csv_pure tests."""
    return b"""timestamp,cur1,cur2
2025-01-01 00:00:00,1.0,2.0
2025-01-01 01:00:00,1.1,2.1
2025-01-01 02:00:00,1.2,2.2
"""
