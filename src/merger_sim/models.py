"""
Pydantic data models for strict input validation and type hinting.
"""

from pydantic import BaseModel, Field


class MarketFirm(BaseModel):
    name: str
    share: float = Field(
        ..., ge=0, le=100, description="Market share must be between 0 and 100"
    )


class MergerScenario(BaseModel):
    acquirer: str
    target: str
    pre_hhi: float
    post_hhi: float
    delta: float
    concentration_level: str
    regulatory_risk: str
    notes: str | None = None
