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
    MatchStatus,
    MainOdds,
    OddsOption,
    TVNetwork,
    Scores,
    Penalties,
    GlobalScores,
    Player,
    Players,
    Lineups,
    LineupTeam,
    MatchStats,
)

__all__ = [
    "PromiedosClient",
    "Event",
    "Match",
    "Team",
    "League",
    "Color",
    "Status",
    "MatchStatus",
    "MainOdds",
    "OddsOption",
    "TVNetwork",
    "Scores",
    "Penalties",
    "GlobalScores",
    "Player",
    "Players",
    "Lineups",
    "LineupTeam",
    "MatchStats",
]
