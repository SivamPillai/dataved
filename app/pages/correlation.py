"""Correlation analysis tab: column select, scatter or heatmap, save."""

from typing import List

import streamlit as st

from charts.correlation import build_correlation_scatter, build_correlation_heatmap
from app.ui.save_plot import save_plot_button
from services.data_utils import is_not_subset


def render_correlation_analysis(selected_datasets: List[str]) -> None:
    """Render correlation UI and chart (scatter for 2 cols, heatmap otherwise)."""
    if "correlation_analysis_state" not in st.session_state:
        st.session_state.correlation_analysis_state = {
            "columns": [],
            "figure": None,
            "is_initialized": False,
        }

    df = st.session_state.data[selected_datasets[0]]
    numeric_cols = [
        c for c in df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if not c.startswith("metaData")
    ]
    state = st.session_state.correlation_analysis_state
    if is_not_subset(state.get("columns", []), numeric_cols):
        state["columns"] = numeric_cols
        state["figure"] = None
    if not state["is_initialized"]:
        state["columns"] = (
            numeric_cols[:2] if len(numeric_cols) > 2 else numeric_cols
        )
        state["is_initialized"] = True

    correlation_columns = st.multiselect(
        "Select columns for correlation analysis",
        numeric_cols,
        default=state["columns"],
    )

    if correlation_columns != state["columns"]:
        state["columns"] = correlation_columns
        state["figure"] = None

    if not correlation_columns:
        st.warning("Please select at least one column for correlation analysis")
        return

    with st.container():
        if state["figure"] is None:
            if len(correlation_columns) == 2:
                fig = build_correlation_scatter(
                    df,
                    correlation_columns[0],
                    correlation_columns[1],
                    title=f"Correlation between {correlation_columns[0]} and {correlation_columns[1]}",
                )
                st.plotly_chart(fig, width='stretch')
                corr_val = df[correlation_columns].corr().iloc[0, 1]
                st.markdown(
                    f"**Pearson Correlation Coefficient:** {corr_val:.4f}"
                )
            else:
                fig = build_correlation_heatmap(df, correlation_columns)
                st.plotly_chart(fig, width='stretch')
            state["figure"] = fig
        else:
            st.plotly_chart(state["figure"], width='stretch')
        save_plot_button(state["figure"], "correlation")
