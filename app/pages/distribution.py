"""Distribution tab: column select, plot type, bins, KDE; distribution chart."""

from typing import List

import streamlit as st

from charts.distribution import build_distribution_figure
from app.ui.save_plot import save_plot_button
from services.data_utils import is_not_subset


def render_distribution_analysis(selected_datasets: List[str]) -> None:
    """Render distribution UI and chart."""
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

    state = st.session_state.distribution_analysis_state
    if is_not_subset(state.get("columns", []), numeric_cols):
        state["columns"] = numeric_cols[: min(6, len(numeric_cols))]
    if state.get("dataset") != selected_datasets[0]:
        state["dataset"] = selected_datasets[0]
        state["figure"] = None

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    dist_columns = col1.multiselect(
        "Columns to plot",
        numeric_cols,
        default=state.get("columns") or numeric_cols[: min(6, len(numeric_cols))],
        key="dist_columns",
    )
    plot_type = col2.selectbox(
        "Plot type",
        ["Histogram", "KDE", "Histogram + KDE", "Box"],
        index=["Histogram", "KDE", "Histogram + KDE", "Box"].index(
            state.get("plot_type", "Histogram")
        ),
        key="dist_plot_type",
    )
    bins = col3.number_input(
        "Bins (histogram)",
        min_value=5,
        max_value=200,
        value=state.get("bins", 30),
        key="dist_bins",
    )
    show_kde = col4.checkbox(
        "Show KDE", value=state.get("show_kde", False), key="dist_show_kde"
    )
    if plot_type == "Histogram + KDE":
        show_kde = True

    state["columns"] = dist_columns
    state["plot_type"] = plot_type
    state["bins"] = int(bins)
    state["show_kde"] = show_kde

    if not dist_columns:
        st.warning("Select at least one column.")
        return

    fig = build_distribution_figure(
        df,
        dist_columns,
        plot_type,
        bins=state["bins"],
        show_kde=state["show_kde"],
        title=f"Distribution — {selected_datasets[0]}",
    )
    st.plotly_chart(fig, width='stretch')
    save_plot_button(fig, "distribution")
