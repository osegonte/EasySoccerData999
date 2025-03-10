"""
EasySoccerData - A Python easy-to-use library for soccer data analysis from multiple sources.
"""

from .sofascore import (
    SofascoreClient,
    EntityType,
    Event,
    Team,
    TeamEx,
    Player,
    PlayerLineup,
    MatchStats,
    Lineups,
    TeamLineup,
)

__all__ = [
    "SofascoreClient",
    "EntityType",
    "Event",
    "Team",
    "TeamEx",
    "Player",
    "MatchStats",
    "Lineups",
    "TeamLineup",
    "PlayerLineup",
]
__version__ = "0.0.1"
__description__ = "A simple python package for extracting real-time soccer data from diverse online sources, providing essential statistics and insights."
__author__ = "Manuel Cabral"
__title__ = "EasySoccerData"
__license__ = "GPL-3.0"
