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
# Deal with missing or non-numeric values in price/quantity columns.
# Copilot usually suggests converting things with errors="coerce", so
# we use that but also tweak it to fit the dataset.
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric columns and handle missing values."""
    df = df.copy()

    # These are the types of columns that *might* contain numbers.
    candidates = ["price", "unit_price", "quantity", "qty", "total"]
    numeric_cols = [c for c in candidates if c in df.columns]

    # Convert numeric-looking columns to actual numbers.
    # Invalid entries become NaN, which we can deal with cleanly.
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # If a row is missing important numbers, it’s easier to just drop it.
    if numeric_cols:
        df = df.dropna(subset=numeric_cols)

    return df


# Remove rows with impossible values (like negative prices).
# These usually show up because of data entry mistakes, so we just filter them out.
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where numeric columns have negative values."""
    df = df.copy()

    candidates = ["price", "unit_price", "quantity", "qty", "total"]
    numeric_cols = [c for c in candidates if c in df.columns]

    for col in numeric_cols:
        df = df[df[col] >= 0]

    return df
# This lets us run everything from the terminal in one go.
# It loads the raw file, runs the cleaning steps, saves the cleaned version,
# and prints a preview so we can quickly see if things look better.
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)

    df_clean.to_csv(cleaned_path, index=False)

    print("Cleaning complete. First few rows:")
    print(df_clean.head())
