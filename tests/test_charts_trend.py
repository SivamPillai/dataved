"""Unit tests for charts.trend."""

import pandas as pd
import pytest

from charts.trend import build_trend_figure, prepare_trend_data


def test_prepare_trend_data_no_resample(sample_df):
    out = prepare_trend_data(sample_df, ["cur1", "cur2"], trend_or_raw=False, resample_period=None)
    assert list(out.columns) == ["cur1", "cur2"]
    assert len(out) == len(sample_df)


def test_prepare_trend_data_with_resample(sample_df):
    out = prepare_trend_data(sample_df, ["cur1"], trend_or_raw=False, resample_period="2h")
    assert "cur1" in out.columns
    assert len(out) <= len(sample_df)


def test_build_trend_figure(sample_df):
    fig = build_trend_figure(
        sample_df[["cur1", "cur2"]],
        ["cur1", "cur2"],
        "TestDataset",
        trend_or_raw=False,
        resample_period=None,
    )
    assert fig is not None
    assert len(fig.data) == 2
    assert "TestDataset" in fig.layout.title.text
