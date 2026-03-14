"""Distribution chart builder: histograms, KDE, box per column."""

from typing import List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_distribution_figure(
    df: pd.DataFrame,
    columns: List[str],
    plot_type: str,
    bins: int = 30,
    show_kde: bool = False,
    title: str = "Distribution",
) -> go.Figure:
    """
    Build subplots: one per column. plot_type in ('Histogram', 'KDE', 'Histogram + KDE', 'Box').
    """
    n = len(columns)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=columns)
    for i, col in enumerate(columns):
        r, c = i // ncols + 1, i % ncols + 1
        series = df[col].dropna()
        if plot_type == "Box":
            fig.add_trace(go.Box(y=series, name=col), row=r, col=c)
        else:
            if plot_type in ("Histogram", "Histogram + KDE"):
                fig.add_trace(
                    go.Histogram(
                        x=series, nbinsx=bins, name=col, showlegend=False
                    ),
                    row=r,
                    col=c,
                )
            if plot_type in ("KDE", "Histogram + KDE") or (
                plot_type == "Histogram" and show_kde
            ):
                try:
                    from scipy import stats as scipy_stats

                    if series.min() == series.max() or len(series) < 2:
                        raise ValueError("need variance and enough points for KDE")
                    kde = scipy_stats.gaussian_kde(series)
                    x_kde = np.linspace(series.min(), series.max(), 100)
                    y_kde = kde(x_kde)
                    fig.add_trace(
                        go.Scatter(
                            x=x_kde,
                            y=y_kde,
                            mode="lines",
                            name=col,
                            line=dict(color="red", width=2),
                        ),
                        row=r,
                        col=c,
                    )
                except Exception:
                    if plot_type == "KDE":
                        fig.add_trace(
                            go.Histogram(x=series, nbinsx=bins, name=col, showlegend=False),
                            row=r,
                            col=c,
                        )
    fig.update_layout(
        height=250 * nrows, title_text=title, showlegend=False
    )
    return fig
