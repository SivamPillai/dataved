"""Raw Data tab: show selected datasets as dataframes only."""

from typing import List

import streamlit as st


def render_raw_data(selected_datasets: List[str]) -> None:
    """Render each selected dataset as st.dataframe with optional subheader per dataset."""
    st.header("Raw Data")
    for name in selected_datasets:
        df = st.session_state.data[name]
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])
        st.subheader(f"Dataset: {name}")
        st.dataframe(df)
