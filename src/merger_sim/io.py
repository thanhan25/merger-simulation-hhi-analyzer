"""
Data input and output handlers for the merger simulation toolkit.
"""

import pandas as pd
from pathlib import Path
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError


def load_market_data(filepath: str) -> pd.DataFrame:
    """Load market share data from a local CSV file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found at: {filepath}")

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    required_cols = {"Firm", "Market_Share"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns {required_cols}. Found: {set(df.columns)}"
        )

    df["Market_Share"] = pd.to_numeric(df["Market_Share"], errors="coerce")
    if df["Market_Share"].isna().any():
        df = df.dropna(subset=["Market_Share"])

    return df


def load_market_data_from_bigquery(query: str) -> pd.DataFrame:
    """
    Execute a SQL query against Google BigQuery to retrieve market data.

    The query must return a 'Firm' column and either a 'Market_Share' or 'Revenue' column.
    If 'Revenue' is provided, market shares are calculated automatically based on the returned dataset.
    """
    try:
        client = bigquery.Client()
        df = client.query(query).to_dataframe()
    except GoogleAPIError as e:
        raise RuntimeError(f"BigQuery execution failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to authenticate or connect to BigQuery: {e}")

    # Standardize column names to lower case for flexible matching
    col_map = {c.lower(): c for c in df.columns}

    if "firm" not in col_map:
        raise ValueError("BigQuery results must contain a 'Firm' column.")

    firm_col = col_map["firm"]

    if "market_share" in col_map:
        share_col = col_map["market_share"]
        df = df[[firm_col, share_col]].rename(
            columns={firm_col: "Firm", share_col: "Market_Share"}
        )
    elif "revenue" in col_map:
        rev_col = col_map["revenue"]
        # Dynamically calculate market share from revenue
        df["Market_Share"] = (df[rev_col] / df[rev_col].sum()) * 100
        df = df[[firm_col, "Market_Share"]].rename(columns={firm_col: "Firm"})
    else:
        raise ValueError(
            "BigQuery results must contain either a 'Market_Share' or 'Revenue' column."
        )

    df["Market_Share"] = pd.to_numeric(df["Market_Share"], errors="coerce")
    df = df.dropna(subset=["Market_Share"])

    return df
