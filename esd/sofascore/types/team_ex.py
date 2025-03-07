from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .country import Country, parse_country
from .color import Color, parse_color
from .team import Team
from .manager import Manager, parse_manager


@dataclass
class TeamEx(Team):
    manager: Manager = field(default_factory=Manager)


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
