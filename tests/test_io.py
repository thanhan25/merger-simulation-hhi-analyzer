import pytest
from merger_sim.io import load_market_data


def test_io_missing_columns(tmp_path):
    """Test validation of missing required columns."""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "bad_data.csv"
    p.write_text("Company,Percentage\nFirm A,50")

    with pytest.raises(ValueError, match="CSV must contain columns"):
        load_market_data(str(p))
