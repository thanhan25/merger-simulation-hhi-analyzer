"""
Core econometric metrics for market concentration analysis.
"""

from typing import Tuple
import pandas as pd
from .config import THRESHOLDS


def calculate_hhi(market_shares: pd.Series) -> float:
    """Calculate the Herfindahl-Hirschman Index (HHI) for a given market."""
    if market_shares.sum() > 100.1:
        raise ValueError(
            f"Market shares cannot exceed 100%. Current sum: {market_shares.sum()}"
        )
    if (market_shares < 0).any():
        raise ValueError("Market shares cannot be negative.")

    return float((market_shares**2).sum())


def evaluate_antitrust_risk(hhi_pre: float, hhi_post: float) -> Tuple[str, str]:
    """Evaluate the antitrust risk of a merger based on regulatory thresholds."""
    delta = hhi_post - hhi_pre

    # Determine Post-Merger Concentration
    if hhi_post < THRESHOLDS.UNCONCENTRATED_MAX:
        concentration = "Unconcentrated"
    elif (
        THRESHOLDS.UNCONCENTRATED_MAX <= hhi_post <= THRESHOLDS.HIGHLY_CONCENTRATED_MIN
    ):
        concentration = "Moderately Concentrated"
    else:
        concentration = "Highly Concentrated"

    # Determine Regulatory Risk
    if delta < THRESHOLDS.DELTA_LOW_RISK_MAX:
        risk = "Low Risk: Unlikely to have adverse competitive effects."
    elif (
        concentration == "Moderately Concentrated"
        and delta > THRESHOLDS.DELTA_LOW_RISK_MAX
    ):
        risk = "Moderate Risk: Potentially raises significant competitive concerns."
    elif (
        concentration == "Highly Concentrated"
        and THRESHOLDS.DELTA_LOW_RISK_MAX <= delta <= THRESHOLDS.DELTA_HIGH_RISK_MIN
    ):
        risk = (
            "Moderate/High Risk: Potentially raises significant competitive concerns."
        )
    elif (
        concentration == "Highly Concentrated"
        and delta > THRESHOLDS.DELTA_HIGH_RISK_MIN
    ):
        risk = "High Risk: Presumed to enhance market power (Red Flag)."
    else:
        risk = "Low Risk: Safe harbor thresholds met."

    return concentration, risk
