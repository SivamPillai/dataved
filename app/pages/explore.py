"""Explore tab: PyGWalker visual exploration."""

from typing import List

import streamlit as st

try:
    from pygwalker.api.streamlit import StreamlitRenderer

    HAS_PYGWALKER = True
except ImportError:
    HAS_PYGWALKER = False
    StreamlitRenderer = None


def render_pygwalker_explore(selected_datasets: List[str]) -> None:
    """Render PyGWalker explorer for selected dataset."""
    if not selected_datasets:
        return
    if not HAS_PYGWALKER:
        st.info(
            "Visual exploration requires **pygwalker**. "
            "Install with: `uv add pygwalker` or run `uv sync`"
        )
        return
    dataset_name = st.selectbox(
        "Dataset to explore",
        selected_datasets,
        index=(
            selected_datasets.index(st.session_state.pygwalker_dataset)
            if st.session_state.pygwalker_dataset in selected_datasets
            else 0
        ),
        key="pygwalker_dataset_select",
    )
    st.session_state.pygwalker_dataset = dataset_name
    df = st.session_state.data[dataset_name].reset_index()
    try:
        # default_tab="data" shows the data tab first; PyGWalker has no API to hide the tab bar or disable the vis tab
        pyg_app = StreamlitRenderer(df, spec_io_mode="rw", default_tab="vis")
        pyg_app.explorer(default_tab="vis")
    except Exception as e:
        st.error(f"Error rendering PyGWalker: {str(e)}")
