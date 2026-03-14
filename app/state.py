"""Centralized session state initialization and schema for the dashboard."""

import streamlit as st


def init_session_state() -> None:
    """Initialize all session state keys used across the app."""
    # Data states
    if "data" not in st.session_state:
        st.session_state.data = {}
    if "selected_datasets" not in st.session_state:
        st.session_state.selected_datasets = []
    if "dataset_submit_count" not in st.session_state:
        st.session_state.dataset_submit_count = 0
    if "active_analysis" not in st.session_state:
        st.session_state.active_analysis = None

    # Analysis states (trend, correlation)
    analysis_states = {
        "trend": {
            "columns": [],
            "figure": None,
            "is_initialized": False,
            "trend_or_raw": True,
            "resample_period": None,
        },
        "correlation": {
            "columns": [],
            "figure": None,
            "is_initialized": False,
        },
    }

    for analysis_type, state in analysis_states.items():
        state_key = f"{analysis_type}_analysis_state"
        if state_key not in st.session_state:
            st.session_state[state_key] = state

    for analysis_type in ["trend", "correlation", "distribution", "anomaly"]:
        save_state_key = f"save_{analysis_type}_plot"
        if save_state_key not in st.session_state:
            st.session_state[save_state_key] = False

    if "pygwalker_dataset" not in st.session_state:
        st.session_state.pygwalker_dataset = None
    if "distribution_analysis_state" not in st.session_state:
        st.session_state.distribution_analysis_state = {
            "columns": [],
            "plot_type": "Histogram",
            "bins": 30,
            "show_kde": False,
            "figure": None,
            "dataset": None,
        }
    if "anomaly_analysis_state" not in st.session_state:
        st.session_state.anomaly_analysis_state = {
            "method": "IQR",
            "columns": [],
            "figure": None,
            "dataset": None,
        }
