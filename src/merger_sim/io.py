"""
Data input and output handlers for the merger simulation toolkit.
"""

import pandas as pd
from pathlib import Path


def load_market_data(filepath: str) -> pd.DataFrame:
    """
    Load market share data from a CSV file.

    Expected CSV format:
    Firm,Market_Share
    Company A, 35.0
    Company B, 25.0

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Validated dataframe containing the market data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the required columns are missing.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found at: {filepath}")

    df = pd.read_csv(path)

    # Strip whitespace from column names just in case
    df.columns = df.columns.str.strip()

    required_cols = {"Firm", "Market_Share"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns {required_cols}. Found: {set(df.columns)}"
        )

    # Ensure Market_Share is numeric
    df["Market_Share"] = pd.to_numeric(df["Market_Share"], errors="coerce")

    # Drop rows with NaN in Market_Share and warn the user
    if df["Market_Share"].isna().any():
        print("Warning: Dropping rows with invalid or missing Market_Share values.")
        df = df.dropna(subset=["Market_Share"])

    return df
