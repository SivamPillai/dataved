"""Sidebar UI: Load New Dataset form, then Select dataset (after load may have run)."""

import streamlit as st
from typing import Dict, List


def render_sidebar_load_section() -> Dict:
    """Render Load New Dataset form only. Return dataset_name, uploaded_file, timestamp_column."""
    st.sidebar.header("Load New Dataset")
    default_name = f"Dataset_{st.session_state.get('dataset_submit_count', 0) + 1}"
    dataset_name = st.sidebar.text_input("Dataset Name", value=default_name)
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help="Upload a CSV file with timestamp column",
    )
    timestamp_column = st.sidebar.text_input(
        "Timestamp Column Name",
        value="timestamp",
        help="Name of the column containing timestamps",
    )
    return {
        "dataset_name": dataset_name,
        "uploaded_file": uploaded_file,
        "timestamp_column": timestamp_column,
    }


def render_sidebar_select_section() -> List[str]:
    """Render Select dataset (when data exists); single select. Return selected as list of one or empty."""
    selected_datasets: List[str] = []
    if st.session_state.data:
        st.sidebar.header("Select dataset")
        keys = list(st.session_state.data.keys())
        default = (
            st.session_state.selected_datasets[0]
            if st.session_state.selected_datasets and st.session_state.selected_datasets[0] in st.session_state.data
            else keys[0]
        )
        selected = st.sidebar.selectbox(
            "Select dataset",
            options=keys,
            index=keys.index(default) if default in keys else 0,
            key="sidebar_dataset_select",
        )
        selected_datasets = [selected] if selected else []
        if "trend_analysis_state" in st.session_state:
            st.session_state.trend_analysis_state["is_initialized"] = False
        st.sidebar.caption("Loaded datasets persist until you clear or reload.")
    return selected_datasets
