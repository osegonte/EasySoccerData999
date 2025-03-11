"""
Contains the types for the Sofascore service.
"""

from .event import Event, parse_events, parse_event
from .team import Team, parse_team
from .player import Player, parse_player
from .match_stats import MatchStats, parse_match_stats
from .lineup import Lineups, PlayerLineup, TeamColor, TeamLineup, parse_lineups
from .tournament import Tournament, parse_tournaments, parse_tournament
from .entity import EntityType
from .categories import Category


__all__ = [
    "Event",
    "parse_events",
    "parse_event",
    "Tournament",
    "parse_tournaments",
    "parse_tournament",
    "Team",
    "parse_team",
    "Player",
    "parse_player",
    "MatchStats",
    "parse_match_stats",
    "Lineups",
    "PlayerLineup",
    "TeamColor",
    "TeamLineup",
    "parse_lineups",
    "EntityType",
    "Category",
]
