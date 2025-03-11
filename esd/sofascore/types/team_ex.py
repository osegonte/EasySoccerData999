"""
Detailed team data class.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .country import parse_country
from .color import parse_color
from .team import Team
from .manager import Manager, parse_manager
from .player import Player


@dataclass
class TeamEx(Team):
    """
    Detailed team data class.
    """
    manager: Manager = field(default_factory=Manager)
    players: List[Player] = field(default_factory=list)


def parse_team_ex(data: Dict) -> TeamEx:
    """
    Parse detailed team data.

    Args:
        data (dict): The team data.

    Returns:
        TeamEx: The detailed team object
    """
    return TeamEx(
        name=data.get("name"),
        short_name=data.get("shortName"),
        slug=data.get("slug"),
        name_code=data.get("nameCode"),
        id=data.get("id", 0),
        entity_type=data.get("entityType"),
        country=parse_country(data.get("country", {})),
        color=parse_color(data.get("teamColors", {})),
        manager=parse_manager(data.get("manager", {})),
        # disabled=data.get("disabled", False),
        # type=data.get("type", 0),
        # gender=data.get("gender", ""),
    )
