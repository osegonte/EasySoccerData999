"""
EasySoccerData - A Python easy-to-use library for soccer data analysis from multiple sources.
"""

from .sofascore import SofascoreClient, EntityType, Event, Team, TeamEx, Player, MatchStats

__all__ = ["SofascoreClient", "EntityType", "Event", "Team", "TeamEx", "Player", "MatchStats"]
__version__ = "0.0.1"
