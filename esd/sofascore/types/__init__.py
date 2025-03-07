"""
Contains the types for the Sofascore service.
"""

from .event import Event, parse_events
from .team import Team, parse_team
from .team_ex import TeamEx, parse_team_ex

__all__ = ["Event", "parse_events", "Team", "parse_team", "TeamEx", "parse_team_ex"]
