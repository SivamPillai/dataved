"""Data utilities: pure helpers + Streamlit-cached wrappers for CSV load and null handling."""

import io
import streamlit as st
import pandas as pd
from loguru import logger
from typing import Tuple, Dict, Any


# --- Pure functions (testable without Streamlit) ---


def is_not_subset_pure(list1: list, list2: list) -> bool:
    """Checks if list1 is NOT a subset of list2."""
    return not all(item in list2 for item in list1)


def fill_nulls_pure(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Fill nulls with forward/backward fill. Returns (df_filled, null_stats)."""
    null_stats = {}
    df_filled = df.copy()
    for col in df.columns:
        if df[col].isnull().any():
            df_filled[col] = df[col].ffill().bfill()
            null_count = df[col].isnull().sum()
            null_percentage = (null_count / len(df)) * 100
            null_stats[col] = {"filled": int(null_count), "percentage": round(null_percentage, 2)}
    return df_filled, null_stats


def parse_csv_pure(
    content: bytes, timestamp_column: str = "timestamp"
) -> pd.DataFrame:
    """
    Parse CSV bytes into DataFrame with timestamp as index.
    Raises ValueError if timestamp column missing.
    """
    df = pd.read_csv(io.BytesIO(content))
    if timestamp_column not in df.columns:
        raise ValueError(
            f"Timestamp column '{timestamp_column}' not found in CSV. "
            f"Available columns: {list(df.columns)}"
        )
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    if df[timestamp_column].dt.tz is None:
        df[timestamp_column] = df[timestamp_column].dt.tz_localize("UTC")
    df[timestamp_column] = df[timestamp_column].dt.tz_convert("Asia/Kolkata")
    df.set_index(timestamp_column, inplace=True)
    return df


# --- Cached Streamlit-facing API ---


@st.cache_data
def is_not_subset(list1, list2):
    """Cached wrapper for is_not_subset_pure."""
    return is_not_subset_pure(list1, list2)


@st.cache_data
def handle_null_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Cached wrapper for fill_nulls_pure."""
    return fill_nulls_pure(df)


@st.cache_data
def get_data_from_csv(uploaded_file, timestamp_column: str = "timestamp") -> pd.DataFrame:
    """
    Load and process CSV from Streamlit UploadedFile.
    Uses cached parse_csv_pure for testable logic.
    """
    try:
        content = uploaded_file.read()
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        df = parse_csv_pure(content, timestamp_column)
        logger.info(
            f"CSV data processed successfully. Index set to timestamp column '{timestamp_column}'"
        )
        return df
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}")
        raise e
