"""
Sofascore types module necessary for the client.
"""

from .client import SofascoreClient
from .types import (
    EntityType,
    Event,
    Team,
    Player,
    MatchStats,
    PlayerLineup,
    TeamLineup,
    Lineups,
    TeamColor,
)

__all__ = [
    "SofascoreClient",
    "EntityType",
    "Event",
    "Team",
    "Player",
    "MatchStats",
    "PlayerLineup",
    "TeamLineup",
    "Lineups",
    "TeamColor",
]
