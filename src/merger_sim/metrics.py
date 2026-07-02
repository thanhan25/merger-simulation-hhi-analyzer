"""
Mathematical logic and HHI functions.
"""


def calculate_hhi(market_shares: list[float]) -> float:
    """Calculate the Herfindahl-Hirschman Index (HHI) for a given market."""
    if sum(market_shares) > 100.1:
        raise ValueError("Market shares cannot sum to more than 100%.")

    hhi = sum(share**2 for share in market_shares)
    return round(hhi, 2)


def evaluate_antitrust_risk(
    pre_hhi: float, post_hhi: float, delta: float
) -> tuple[str, str]:
    """
    Evaluate the regulatory risk of a merger based on DOJ/FTC guidelines.
    Returns a tuple of (Concentration Level, Risk Assessment).
    """
    if post_hhi < 1500:
        concentration = "Unconcentrated"
        risk = "Safe Harbor: Unlikely to have adverse competitive effects."
    elif 1500 <= post_hhi <= 2500:
        concentration = "Moderately Concentrated"
        if delta > 100:
            risk = "Moderate Risk: Potentially raises significant competitive concerns."
        else:
            risk = "Safe Harbor: Unlikely to have adverse competitive effects."
    else:
        concentration = "Highly Concentrated"
        if delta > 200:
            risk = "High Risk: Presumed to enhance market power (Red Flag)."
        elif delta > 100:
            risk = "Moderate Risk: Potentially raises significant competitive concerns."
        else:
            risk = "Safe Harbor: Unlikely to have adverse competitive effects."

    return concentration, risk
