"""
Merger Simulation & Market Concentration Analyzer.
A quantitative antitrust toolkit for evaluating HHI and market dynamics.
"""

from .metrics import calculate_hhi, evaluate_antitrust_risk
from .simulation import simulate_merger
from .io import load_market_data
from .plotting import plot_merger_impact

__all__ = [
    "calculate_hhi",
    "evaluate_antitrust_risk",
    "simulate_merger",
    "load_market_data",
    "plot_merger_impact",
]
__version__ = "0.1.0"
