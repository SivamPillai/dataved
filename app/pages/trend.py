"""Trend analysis tab: column selectors, trend/resample options, trend chart."""

from typing import List

import streamlit as st
import pandas as pd

from core.rolling import calculate_rolling_window
from charts.trend import build_trend_figure, prepare_trend_data
from app.ui.save_plot import save_plot_button
from services.data_utils import is_not_subset


def render_trend_analysis(dataset: str, df: pd.DataFrame) -> None:
    """Render trend analysis UI and chart for one dataset."""
    with st.spinner("Generating trend analysis..."):
        numeric_cols = [
            c for c in df.select_dtypes(include=["float64", "int64"]).columns.tolist()
            if not c.startswith("metaData")
        ]

        state = st.session_state.trend_analysis_state
        if not state["is_initialized"]:
            default_cols = (
                ["cur1", "cur2", "cur3"]
                if all(c in numeric_cols for c in ["cur1", "cur2", "cur3"])
                else numeric_cols[:3]
            )
            state["columns"] = default_cols
            state["is_initialized"] = True
            state["trend_or_raw"] = True
            state["resample_period"] = None
        if is_not_subset(state.get("columns", []), numeric_cols):
            default_cols = (
                ["cur1", "cur2", "cur3"]
                if all(c in numeric_cols for c in ["cur1", "cur2", "cur3"])
                else numeric_cols[:3]
            )
            state["columns"] = default_cols
            state["figure"] = None

        col1, _, col2, col3 = st.columns([3, 1, 1, 1])
        trend_columns = col1.multiselect(
            "Select columns to plot",
            numeric_cols,
            default=state["columns"],
            help="Select one or more columns to visualize",
            key=f"trend_columns_{dataset}",
        )
        trend_or_raw = col2.toggle(
            "Show Trend",
            value=state["trend_or_raw"],
            help="Toggle between raw data and rolling average (window = 5x resampling period)",
            key=f"trend_toggle_{dataset}",
        )
        resample_period = col3.selectbox(
            "Resample Period",
            options=[None, "1min", "1D", "1M"],
            index=(
                0
                if state["resample_period"] is None
                else (
                    1
                    if state["resample_period"] == "1min"
                    else 2 if state["resample_period"] == "1D" else 3
                )
            ),
            format_func=lambda x: "None" if x is None else x,
            help="Select the resampling period (None = original data, 1min = 1 minute, 1D = 1 day, 1M = 1 month)",
            key=f"trend_resample_{dataset}",
        )

        state_changed = False
        if trend_columns != state["columns"]:
            state["columns"] = trend_columns
            state_changed = True
        if trend_or_raw != state["trend_or_raw"]:
            state["trend_or_raw"] = trend_or_raw
            state_changed = True
        if resample_period != state["resample_period"]:
            state["resample_period"] = resample_period
            state_changed = True

        if state["trend_or_raw"]:
            rolling_window = calculate_rolling_window(state["resample_period"])
            st.info(f"📊 Rolling average window: {rolling_window}")

        if state_changed:
            state["figure"] = None

        if not trend_columns:
            st.warning("Please select at least one column to plot")
            return

        if state["figure"] is None:
            try:
                if not isinstance(df.index, pd.DatetimeIndex):
                    st.error("Data index must be datetime for resampling")
                    return
                plot_data = prepare_trend_data(
                    df, trend_columns, state["trend_or_raw"], state["resample_period"]
                )
                state["figure"] = build_trend_figure(
                    plot_data,
                    trend_columns,
                    dataset,
                    trend_or_raw=state["trend_or_raw"],
                    resample_period=state["resample_period"],
                )
            except Exception as e:
                st.error(f"Error generating plot: {str(e)}")
                return

        st.plotly_chart(state["figure"], width='stretch')
        save_plot_button(state["figure"], "trend", key=f"save_trend_{dataset}")
