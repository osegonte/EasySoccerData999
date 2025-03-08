"""
Contains the types for the Sofascore service.
"""

from .event import Event, parse_events, parse_event
from .team import Team, parse_team
from .team_ex import TeamEx, parse_team_ex
from .player import Player, parse_player
from .match_stats import MatchStats, parse_match_stats
from .entity import EntityType

__all__ = [
    "Event",
    "parse_events",
    "parse_event",
    "Team",
    "parse_team",
    "TeamEx",
    "parse_team_ex",
    "Player",
    "parse_player",
    "MatchStats",
    "parse_match_stats",
    "EntityType",
]
