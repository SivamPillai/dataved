"""Save plot as HTML button and handler."""

import os
from datetime import datetime

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio


def save_plot_button(fig: go.Figure, plot_type: str, key: str | None = None) -> None:
    """Render save button and perform save on next run if clicked. Use key when multiple instances exist (e.g. per dataset)."""
    save_state_key = f"save_{plot_type}_plot" if key is None else f"save_{plot_type}_plot_{key}"
    button_kw = {} if key is None else {"key": key}

    if st.button(f"Save {plot_type.title()} Plot as HTML", **button_kw):
        st.session_state[save_state_key] = True

    if st.session_state.get(save_state_key):
        try:
            os.makedirs("plots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"plots/{plot_type}_analysis_{timestamp}.html"
            pio.write_html(fig, filename)
            st.success(f"Plot saved as {filename}")
        except Exception as e:
            st.error(f"Error saving plot: {str(e)}")
        finally:
            st.session_state[save_state_key] = False
