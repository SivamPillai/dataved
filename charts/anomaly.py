"""Anomaly chart builder: time series with anomaly markers."""

from typing import List, Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core import anomaly_detection as core_anomaly
from loguru import logger


def build_anomaly_figure(
    df: pd.DataFrame,
    columns: List[str],
    method: str,
    title: str = "Anomaly detection",
    **extra_params: Any,
) -> go.Figure:
    """
    method in ('IQR', 'LOESS', 'Isolation Forest').
    extra_params: frac, n_std for LOESS; contamination for Isolation Forest.
    """
    fig = make_subplots(
        rows=len(columns),
        cols=1,
        subplot_titles=[f"{col} — {method}" for col in columns],
        vertical_spacing=0.08,
    )
    for i, col in enumerate(columns):
        series = df[col].dropna()
        index_vals = series.index
        if method == "IQR":
            is_anom = core_anomaly.detect_anomalies_iqr(series)
        elif method == "LOESS":
            is_anom = core_anomaly.detect_anomalies_loess(
                series,
                frac=extra_params.get("frac", 0.1),
                n_std=extra_params.get("n_std", 3.0),
            )
        else:
            is_anom = core_anomaly.detect_anomalies_isolation_forest(
                series, contamination=extra_params.get("contamination", 0.05)
            )
        row = i + 1
        fig.add_trace(
            go.Scatter(
                x=index_vals,
                y=series.values,
                mode="lines+markers",
                name=col,
                marker=dict(size=4),
                line=dict(width=1),
            ),
            row=row,
            col=1,
        )
        anom_mask = np.where(is_anom)[0]
        if len(anom_mask) > 0:
            fig.add_trace(
                go.Scatter(
                    x=index_vals[anom_mask],
                    y=series.values[anom_mask],
                    mode="markers",
                    name=f"{col} (anomaly)",
                    marker=dict(
                        size=14,
                        color="red",
                        symbol="x",
                        line=dict(width=2, color="darkred"),
                    ),
                ),
                row=row,
                col=1,
            )
    fig.update_layout(height=350 * len(columns), title_text=title)
    fig.update_xaxes(title_text="Time", row=len(columns), col=1)
    return fig
