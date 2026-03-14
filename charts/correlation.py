"""Correlation chart builders: scatter (2 cols) and heatmap (multiple cols)."""

from typing import List

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def build_correlation_scatter(
    df: pd.DataFrame, col_x: str, col_y: str, title: str | None = None
) -> go.Figure:
    """Build scatter plot for two columns."""
    title = title or f"Correlation between {col_x} and {col_y}"
    fig = px.scatter(df, x=col_x, y=col_y, title=title)
    return fig


def build_correlation_heatmap(
    df: pd.DataFrame, columns: List[str], title: str = "Correlation Matrix"
) -> go.Figure:
    """Build correlation matrix heatmap."""
    corr_matrix = df[columns].corr()
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix,
            x=columns,
            y=columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            text=corr_matrix.round(4),
            texttemplate="%{text}",
            textfont={"size": 10},
        )
    )
    fig.update_layout(
        title=title,
        height=600,
        xaxis_title="Columns",
        yaxis_title="Columns",
    )
    return fig
