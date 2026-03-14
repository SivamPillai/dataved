"""Data loading service: load CSV and write to session state."""

import streamlit as st
from typing import Dict

from services.data_utils import get_data_from_csv, handle_null_values


def load_and_process_data(params: Dict) -> bool:
    """Load CSV from params, clean nulls, store in st.session_state.data. Returns True on success."""
    with st.spinner("Loading data..."):
        try:
            if params.get("uploaded_file") is None:
                st.error("Please upload a CSV file")
                return False
            df = get_data_from_csv(
                params["uploaded_file"],
                params.get("timestamp_column", "timestamp"),
            )
            if df is not None and not df.empty:
                df_clean, _ = handle_null_values(df.copy())
                st.session_state.data[params["dataset_name"]] = df_clean
                st.toast(f"Data loaded successfully for {params['dataset_name']}!", icon="✅")
                return True
            st.error("No data found.")
            return False
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return False
