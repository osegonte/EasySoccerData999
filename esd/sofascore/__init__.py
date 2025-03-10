"""
EasySoccerData - Sofascore
A submodule for extracting data from Sofascore.
"""

from .client import SofascoreClient
from .types import EntityType, Event, Team, TeamEx, Player, MatchStats, PlayerLineup, TeamLineup, Lineups, TeamColor

__all__ = [
    "SofascoreClient",
    "EntityType",
    "Event",
    "Team",
    "TeamEx",
    "Player",
    "MatchStats",
    "PlayerLineup",
    "TeamLineup",
    "Lineups",
    "TeamColor",
]
