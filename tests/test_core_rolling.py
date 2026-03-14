"""Unit tests for core.rolling."""

import pytest

from core.rolling import calculate_rolling_window


def test_rolling_window_none():
    assert calculate_rolling_window(None) == "5Min"


def test_rolling_window_1min():
    assert calculate_rolling_window("1min") == "5min"


def test_rolling_window_1d():
    assert calculate_rolling_window("1D") == "5D"


def test_rolling_window_1m():
    assert calculate_rolling_window("1M") == "5M"


def test_rolling_window_unknown_fallback():
    assert calculate_rolling_window("unknown") == "5Min"
