"""Anomaly detection tab: method, columns, params; anomaly chart."""

from typing import List

import streamlit as st

from charts.anomaly import build_anomaly_figure
from app.ui.save_plot import save_plot_button
from services.data_utils import is_not_subset


def render_anomaly_detection(selected_datasets: List[str]) -> None:
    """Render anomaly detection UI and chart."""
    if not selected_datasets:
        return
    df = st.session_state.data[selected_datasets[0]]
    numeric_cols = [
        c for c in df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if not c.startswith("metaData")
    ]
    if not numeric_cols:
        st.warning("No numeric columns in the selected dataset.")
        return

    state = st.session_state.anomaly_analysis_state
    if state.get("dataset") != selected_datasets[0]:
        state["dataset"] = selected_datasets[0]
        state["figure"] = None
    if is_not_subset(state.get("columns", []), numeric_cols):
        state["columns"] = numeric_cols[: min(3, len(numeric_cols))]

    method = st.selectbox(
        "Anomaly detection method",
        ["IQR", "LOESS", "Isolation Forest"],
        index=["IQR", "LOESS", "Isolation Forest"].index(
            state.get("method", "IQR")
        ),
        key="anomaly_method",
    )
    state["method"] = method
    anomaly_columns = st.multiselect(
        "Columns to analyze",
        numeric_cols,
        default=state.get("columns")
        or numeric_cols[: min(3, len(numeric_cols))],
        key="anomaly_columns",
    )
    state["columns"] = anomaly_columns

    if not anomaly_columns:
        st.warning("Select at least one column.")
        return

    extra_params = {}
    if method == "LOESS":
        extra_params["frac"] = st.slider(
            "LOESS frac", 0.05, 0.5, 0.1, key="loess_frac"
        )
        extra_params["n_std"] = st.slider(
            "Residual threshold (std)", 1.0, 5.0, 3.0, key="loess_n_std"
        )
    if method == "Isolation Forest":
        extra_params["contamination"] = st.slider(
            "Contamination", 0.01, 0.2, 0.05, key="if_contamination"
        )

    fig = build_anomaly_figure(
        df,
        anomaly_columns,
        method,
        title=f"Anomaly detection — {selected_datasets[0]}",
        **extra_params,
    )
    st.plotly_chart(fig, width='stretch')
    save_plot_button(fig, "anomaly")
