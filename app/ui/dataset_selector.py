"""Dataset selector UI: expanders + multiselect."""

import streamlit as st
from typing import List


def render_dataset_selector() -> List[str]:
    """Show available datasets and return list of selected dataset names."""
    if not st.session_state.data:
        return []

    st.subheader("Available Datasets")
    for name in st.session_state.data.keys():
        with st.expander(f"Dataset: {name}"):
            df_display = st.session_state.data[name]
            if "_id" in df_display.columns:
                df_display = df_display.drop(["_id"], axis=1)
            st.dataframe(df_display)

    if "trend_analysis_state" in st.session_state:
        st.session_state.trend_analysis_state["is_initialized"] = False

    return st.multiselect(
        "Select datasets for analysis",
        list(st.session_state.data.keys()),
        default=st.session_state.selected_datasets,
    )
