"""
data_cleaning.py

This script loads a messy sales dataset, cleans it up, and saves a new
version that's easier to work with. The goal is just to fix common issues
like bad column names, weird spacing, missing values, and obviously wrong
numbers.
"""

import pandas as pd


# Load the raw CSV into a DataFrame so we can start cleaning it.
def load_data(file_path: str) -> pd.DataFrame:
    """Load raw sales data from a CSV file."""
    return pd.read_csv(file_path)


# Fix messy column names and clean up any text fields that might have
# random spaces. This just makes life easier later on when analyzing the data.
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names + clean common text fields."""
    df = df.copy()

    # Clean the column names: remove extra spaces, lowercase everything,
    # and replace spaces/dashes with underscores.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Some datasets have random spaces before/after product names or categories,
    # so we clean those up too if they exist.
    for col in ["product_name", "category"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df
