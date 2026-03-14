"""Smoke tests for the dashboard entrypoint (refactored app)."""

import pytest


def test_data_dashboard_main_import():
    """Entrypoint module and main function are importable."""
    from dashboard import main

    assert callable(main)


def test_app_state_init_import():
    """State init is importable from app."""
    from app.state import init_session_state

    assert callable(init_session_state)
