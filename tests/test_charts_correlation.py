"""Unit tests for charts.correlation."""

import pytest

from charts.correlation import build_correlation_scatter, build_correlation_heatmap


def test_build_correlation_scatter(sample_df):
    fig = build_correlation_scatter(sample_df, "cur1", "cur2")
    assert fig is not None
    assert len(fig.data) == 1


def test_build_correlation_heatmap(sample_df):
    fig = build_correlation_heatmap(sample_df, ["cur1", "cur2", "vol1"])
    assert fig is not None
    assert fig.data[0].z is not None
    assert fig.data[0].z.shape == (3, 3)
