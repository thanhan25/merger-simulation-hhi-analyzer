"""
Core mathematical engine for HHI and market share aggregation.
"""

import pandas as pd
from .metrics import calculate_hhi, evaluate_antitrust_risk
from .models import MergerScenario


def simulate_merger(
    df: pd.DataFrame, firm_col: str, share_col: str, acquirer: str, target: str
) -> MergerScenario:
    """Simulate a merger and return a strongly-typed Pydantic model."""
    if acquirer not in df[firm_col].values or target not in df[firm_col].values:
        raise ValueError(f"Both {acquirer} and {target} must exist in the dataset.")

    pre_hhi = calculate_hhi(df[share_col].tolist())

    # Simulate merger
    post_df = df.copy()
    acquirer_idx = post_df[post_df[firm_col] == acquirer].index[0]
    target_idx = post_df[post_df[firm_col] == target].index[0]

    post_df.loc[acquirer_idx, share_col] += post_df.loc[target_idx, share_col]
    post_df = post_df.drop(target_idx)

    post_hhi = calculate_hhi(post_df[share_col].tolist())
    delta = post_hhi - pre_hhi

    concentration, risk = evaluate_antitrust_risk(pre_hhi, post_hhi, delta)

    return MergerScenario(
        acquirer=acquirer,
        target=target,
        pre_hhi=pre_hhi,
        post_hhi=post_hhi,
        delta=delta,
        concentration_level=concentration,
        regulatory_risk=risk,
    )
