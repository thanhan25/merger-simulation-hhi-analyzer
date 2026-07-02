"""
Configuration parameters and regulatory thresholds for antitrust analysis.
Matches general guidelines from the U.S. DOJ/FTC and European Commission.
"""

from dataclasses import dataclass


@dataclass
class AntitrustThresholds:
    UNCONCENTRATED_MAX: float = 1500.0
    HIGHLY_CONCENTRATED_MIN: float = 2500.0
    DELTA_LOW_RISK_MAX: float = 100.0
    DELTA_HIGH_RISK_MIN: float = 200.0


THRESHOLDS = AntitrustThresholds()
