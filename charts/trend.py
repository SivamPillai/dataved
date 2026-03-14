"""Trend chart builder: time series line plot with optional resample/rolling."""

from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go

from core.rolling import calculate_rolling_window


def build_trend_figure(
    plot_data: pd.DataFrame,
    columns: List[str],
    dataset_name: str,
    trend_or_raw: bool = True,
    resample_period: Optional[str] = None,
) -> go.Figure:
    """
    Build a Plotly figure for trend analysis.
    plot_data must have a DatetimeIndex and contain the selected columns.
    If trend_or_raw is True, rolling mean is applied (window from resample_period).
    """
    fig = go.Figure()
    symbols = [
        "circle",
        "diamond",
        "square",
        "star",
        "triangle-up",
        "triangle-down",
        "pentagon",
        "hexagon",
    ]
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
    ]
    for i, col in enumerate(columns):
        unit = (
            "A"
            if "cur" in col
            else "V"
            if "vol" in col
            else "count"
            if "cnt" in col
            else ""
        )
        fig.add_trace(
            go.Scattergl(
                x=plot_data.index,
                y=plot_data[col],
                mode="lines+markers",
                name=f"{dataset_name} - {col} ({unit})",
                marker=dict(
                    size=5,
                    symbol=symbols[i % len(symbols)],
                    color=colors[i % len(colors)],
                ),
                line=dict(color=colors[i % len(colors)], width=2),
            )
        )
    fig.update_layout(
        height=600,
        title=f"Analysis for {dataset_name}",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis_title="Time",
        yaxis_title="Value",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=50, r=50, t=50, b=50),
    )
    for trace in fig.data:
        unit = trace.name.split("(")[1].split(")")[0] if "(" in trace.name else ""
        trace.update(
            hovertemplate=f"Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>"
        )
    return fig


def prepare_trend_data(
    df: pd.DataFrame,
    columns: List[str],
    trend_or_raw: bool,
    resample_period: Optional[str],
) -> pd.DataFrame:
    """Resample and optionally apply rolling mean. Returns DataFrame with selected columns."""
    plot_data = df[columns].copy()
    if resample_period is not None:
        plot_data = plot_data.resample(resample_period).mean()
    if trend_or_raw:
        plot_data = plot_data.rolling(
            calculate_rolling_window(resample_period)
        ).mean()
    return plot_data
