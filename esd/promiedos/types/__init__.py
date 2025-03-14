"""
Contains the types for the Sofascore service.
"""

from .event import Event, parse_events
from .league import League
from .color import Color
from .status import Status
from .team import Team
from .odds import MainOdds, OddsOption
from .tvnetwork import TVNetwork
from .scores import Scores
from .match import Match


__all__ = [
    "Event",
    "parse_events",
    "League",
    "Color",
    "Status",
    "Team",
    "MainOdds",
    "OddsOption",
    "TVNetwork",
    "Scores",
    "Match",
]
