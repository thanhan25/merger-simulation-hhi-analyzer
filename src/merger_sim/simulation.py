"""
Simulation engine for hypothetical mergers and acquisitions.
"""

from typing import Dict, Any
import pandas as pd
from .metrics import calculate_hhi, evaluate_antitrust_risk


def simulate_merger(
    df: pd.DataFrame, firm_col: str, share_col: str, acquirer: str, target: str
) -> Dict[str, Any]:
    """
    Simulate a merger between two firms and calculate the resulting market shift.

    Args:
        df (pd.DataFrame): DataFrame containing market data.
        firm_col (str): Column name containing firm names.
        share_col (str): Column name containing market shares (0-100).
        acquirer (str): Name of the acquiring firm.
        target (str): Name of the target firm.

    Returns:
        Dict[str, Any]: A dictionary containing pre/post dataframes and HHI metrics.
    """
    if acquirer not in df[firm_col].values or target not in df[firm_col].values:
        raise ValueError("Acquirer or Target firm not found in the dataset.")

    # Pre-merger state
    pre_shares = df.set_index(firm_col)[share_col]
    hhi_pre = calculate_hhi(pre_shares)

    # Post-merger state
    df_post = df.copy()

    # Calculate new combined share
    combined_share = pre_shares[acquirer] + pre_shares[target]

    # Update acquirer, remove target
    df_post.loc[df_post[firm_col] == acquirer, share_col] = combined_share
    df_post.loc[df_post[firm_col] == acquirer, firm_col] = f"{acquirer} + {target}"
    df_post = df_post[df_post[firm_col] != target].reset_index(drop=True)

    # Sort for cleaner presentation
    df_post = df_post.sort_values(by=share_col, ascending=False).reset_index(drop=True)

    post_shares = df_post.set_index(firm_col)[share_col]
    hhi_post = calculate_hhi(post_shares)

    # Antitrust evaluation
    concentration, risk = evaluate_antitrust_risk(hhi_pre, hhi_post)

    return {
        "pre_merger_df": df.sort_values(by=share_col, ascending=False).reset_index(
            drop=True
        ),
        "post_merger_df": df_post,
        "hhi_pre": round(hhi_pre, 2),
        "hhi_post": round(hhi_post, 2),
        "delta": round(hhi_post - hhi_pre, 2),
        "concentration_level": concentration,
        "regulatory_risk": risk,
    }
