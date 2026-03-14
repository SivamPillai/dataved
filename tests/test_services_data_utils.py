"""Unit tests for services.data_utils pure functions."""

import numpy as np
import pandas as pd
import pytest

from services.data_utils import (
    is_not_subset_pure,
    fill_nulls_pure,
    parse_csv_pure,
)


def test_is_not_subset_pure_subset():
    assert is_not_subset_pure([1, 2], [1, 2, 3]) is False


def test_is_not_subset_pure_not_subset():
    assert is_not_subset_pure([1, 4], [1, 2, 3]) is True


def test_is_not_subset_pure_empty():
    assert is_not_subset_pure([], [1, 2, 3]) is False


def test_fill_nulls_pure():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [10, 10, 10]})
    df_filled, stats = fill_nulls_pure(df)
    assert df_filled["a"].isna().sum() == 0
    assert "a" in stats
    assert stats["a"]["filled"] == 1


def test_fill_nulls_pure_no_nulls():
    df = pd.DataFrame({"a": [1, 2, 3]})
    df_filled, stats = fill_nulls_pure(df)
    pd.testing.assert_frame_equal(df_filled, df)
    assert len(stats) == 0


def test_parse_csv_pure(sample_csv_bytes):
    df = parse_csv_pure(sample_csv_bytes, "timestamp")
    assert "timestamp" not in df.columns  # now index
    assert list(df.columns) == ["cur1", "cur2"]
    assert len(df) == 3


def test_parse_csv_pure_missing_timestamp():
    csv = b"a,b\n1,2"
    with pytest.raises(ValueError, match="Timestamp column 'ts' not found"):
        parse_csv_pure(csv, "ts")
