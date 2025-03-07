"""
This module contains the Team related data classes.
"""

from dataclasses import dataclass, field
from typing import Dict
from .country import Country, parse_country
from .color import Color, parse_color


@dataclass
class Team:
    """
    A class to represent a team.
    """

    name: str = field(default=None)
    short_name: str = field(default=None)
    slug: str = field(default=None)
    name_code: str = field(default=None)
    entity_type: str = field(default=None)
    id: int = field(default=0)
    country: Country = field(default_factory=Country)
    color: Color = field(default_factory=Color)
    # gender: str = field(default="")
    # disabled: bool = field(default=False)
    # type: int = field(default=0)


def parse_team(data: Dict) -> Team:
    """
    Parse the team data.

    Args:
        data (dict): The team data.

    Returns:
        Team: The team object.
    """
    return Team(
        name=data.get("name"),
        short_name=data.get("shortName"),
        slug=data.get("slug"),
        name_code=data.get("nameCode"),
        id=data.get("id", 0),
        entity_type=data.get("entityType"),
        country=parse_country(data.get("country", {})),
        color=parse_color(data.get("teamColors", {})),
        # disabled=data.get("disabled", False),
        # type=data.get("type", 0),
        # gender=data.get("gender", ""),
    )
