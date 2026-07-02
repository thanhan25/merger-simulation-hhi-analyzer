import pytest
import pandas as pd
from merger_sim.metrics import calculate_hhi, evaluate_antitrust_risk


def test_calculate_hhi_standard():
    """Test standard HHI calculation for a simple market."""
    shares = pd.Series([50, 30, 20])
    # 50^2 + 30^2 + 20^2 = 2500 + 900 + 400 = 3800
    assert calculate_hhi(shares) == 3800.0


def test_calculate_hhi_monopoly():
    """A pure monopoly should have an HHI of exactly 10,000."""
    shares = pd.Series([100])
    assert calculate_hhi(shares) == 10000.0


def test_calculate_hhi_exceeds_100():
    """Should raise an error if market shares sum to > 100%."""
    shares = pd.Series([60, 50])
    with pytest.raises(ValueError, match="cannot exceed 100%"):
        calculate_hhi(shares)


def test_evaluate_antitrust_risk_safe():
    """Test safe harbor threshold."""
    # Pre: 1000, Post: 1050 (Unconcentrated, small delta)
    concentration, risk = evaluate_antitrust_risk(1000, 1050)
    assert concentration == "Unconcentrated"
    assert "Low Risk" in risk


def test_evaluate_antitrust_risk_red_flag():
    """Test major red flag threshold."""
    # Pre: 2600, Post: 3000 (Highly Concentrated, Delta > 200)
    concentration, risk = evaluate_antitrust_risk(2600, 3000)
    assert concentration == "Highly Concentrated"
    assert "High Risk" in risk
