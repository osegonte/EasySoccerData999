"""
This module contains the Team class and its parser.
"""

from dataclasses import dataclass, field
from .color import Color, parse_color


@dataclass
class Team:
    """
    The team of a match.
    """

    id: str = field(default=None)
    name: str = field(default=None)
    slug: str = field(default=None)
    short_name: str = field(default=None)
    country_id: str = field(default=None)
    color: Color = field(default_factory=Color)
    red_cards: int = field(default=0)


def parse_team(data: dict) -> Team:
    """
    Parse the team data.
    """
    return Team(
        name=data.get("name"),
        short_name=data.get("short_name"),
        slug=data.get("url_name"),
        id=data.get("id"),
        country_id=data.get("country_id"),
        color=parse_color(data.get("colors", {})),
        red_cards=data.get("red_cards", 0),
    )
