"""
Promiedos module.
"""

from .client import PromiedosClient
from .types import (
    Event,
    Match,
    Team,
    League,
    Color,
    Status,
    MainOdds,
    OddsOption,
    TVNetwork,
    Scores,
)

__all__ = [
    "PromiedosClient",
    "Event",
    "Match",
    "Team",
    "League",
    "Color",
    "Status",
    "MainOdds",
    "OddsOption",
    "TVNetwork",
    "Scores",
]
