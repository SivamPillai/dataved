"""
Data Analytics Dashboard — entrypoint.
Composes state, sidebar, and tab pages.
"""

import sys
from pathlib import Path

# Ensure project root is on path when run from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from app.state import init_session_state
from app.ui.sidebar import render_sidebar_load_section, render_sidebar_select_section
from services.data_loader import load_and_process_data
from app.pages.raw_data import render_raw_data
from app.pages.trend import render_trend_analysis
from app.pages.correlation import render_correlation_analysis
from app.pages.distribution import render_distribution_analysis
from app.pages.anomaly import render_anomaly_detection
from app.pages.explore import render_pygwalker_explore

st.set_page_config(
    page_title="Data Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

st.markdown(
    """
    <style>
        .appview-container .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        [data-testid="stSidebar"] > div:first-child {
            overflow-y: auto !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main() -> None:
    st.title("Data Analytics Dashboard")
    init_session_state()

    params = render_sidebar_load_section()

    if st.sidebar.button("Submit"):
        if not params["dataset_name"]:
            st.error("Please enter a dataset name")
        else:
            if load_and_process_data(params):
                st.session_state.dataset_submit_count += 1
                st.session_state.selected_datasets = [params["dataset_name"]]

    selected_datasets = render_sidebar_select_section()
    params["selected_datasets"] = selected_datasets

    if not st.session_state.data:
        st.info("Use the sidebar to upload a CSV file for analysis.")
        return
    if not selected_datasets:
        st.warning("Please select at least one dataset for analysis.")
        return

    st.session_state.selected_datasets = selected_datasets

    tab_raw, tab_trend, tab_correlation, tab_distribution, tab_anomaly, tab_explore = (
        st.tabs(
            ["Raw Data", "Trend", "Correlation", "Distribution", "Anomaly", "Explore"],
            key="main_tabs",
            on_change="rerun",
        )
    )

    if tab_raw.open:
        with tab_raw:
            render_raw_data(selected_datasets)
    if tab_trend.open:
        with tab_trend:
            st.header("Trend Analysis")
            for dataset in selected_datasets:
                render_trend_analysis(dataset, st.session_state.data[dataset])
    if tab_correlation.open:
        with tab_correlation:
            st.header("Correlation Analysis")
            render_correlation_analysis(selected_datasets)
    if tab_distribution.open:
        with tab_distribution:
            st.header("Distribution")
            render_distribution_analysis(selected_datasets)
    if tab_anomaly.open:
        with tab_anomaly:
            st.header("Anomaly Detection")
            render_anomaly_detection(selected_datasets)
    if tab_explore.open:
        with tab_explore:
            st.header("Visual Explore")
            render_pygwalker_explore(selected_datasets)


if __name__ == "__main__":
    main()
