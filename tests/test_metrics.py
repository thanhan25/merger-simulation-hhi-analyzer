import pytest
from merger_sim.metrics import calculate_hhi, evaluate_antitrust_risk


def test_calculate_hhi_standard():
    """Test standard HHI calculation."""
    shares = [40.0, 30.0, 30.0]
    assert calculate_hhi(shares) == 3400.0


def test_calculate_hhi_monopoly():
    """Test monopoly HHI."""
    shares = [100.0]
    assert calculate_hhi(shares) == 10000.0


def test_calculate_hhi_exceeds_100():
    """Should raise an error if market shares sum to > 100%."""
    shares = [60.0, 50.0]
    with pytest.raises(ValueError, match="Market shares cannot sum to more than 100%."):
        calculate_hhi(shares)


def test_evaluate_antitrust_risk_safe():
    """Test Safe Harbor thresholds."""
    concentration, risk = evaluate_antitrust_risk(
        pre_hhi=1000, post_hhi=1200, delta=200
    )
    assert concentration == "Unconcentrated"
    assert "Safe Harbor" in risk


def test_evaluate_antitrust_risk_red_flag():
    """Test High Risk thresholds."""
    concentration, risk = evaluate_antitrust_risk(
        pre_hhi=2400, post_hhi=2800, delta=400
    )
    assert concentration == "Highly Concentrated"
    assert "High Risk" in risk
