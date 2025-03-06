"""
This module contains the Team related data classes.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .country import Country, parse_country


@dataclass
class TeamColors:
    primary: str = field(default="#000000")
    secondary: str = field(default="#000000")
    text: str = field(default="#000000")


@dataclass
class TeamScore:
    current: int = field(default=0)
    display: int = field(default=0)
    period1: int = field(default=0)
    period2: int = field(default=0)
    normaltime: int = field(default=0)


@dataclass
class TeamSummary:
    name: str = field(default="")
    short_name: str = field(default="")
    slug: str = field(default="")
    # gender: str = field(default="")
    name_code: str = field(default="")
    # disabled: bool = field(default=False)
    # type: int = field(default=0)
    id: int = field(default=0)
    country: Country = field(default_factory=Country)
    entity_type: str = field(default="")
    team_colors: TeamColors = field(default_factory=TeamColors)


def parse_team_score(data: Dict) -> TeamScore:
    """
    Parse the team score data.

    Args:
        data (dict): The team score data.

    Returns:
        Score: The team score object.
    """
    return TeamScore(
        current=data.get("current", 0),
        display=data.get("display", 0),
        period1=data.get("period1", 0),
        period2=data.get("period2", 0),
        normaltime=data.get("normaltime", 0),
    )


def parse_team_summary(data: Dict) -> TeamSummary:
    """
    Parse the summary team data.

    Args:
        data (dict): The summary team data.

    Returns:
        Team: The team object.
    """
    return TeamSummary(
        name=data.get("name", ""),
        short_name=data.get("shortName", ""),
        slug=data.get("slug", ""),
        name_code=data.get("nameCode", ""),
        # disabled=data.get("disabled", False),
        # type=data.get("type", 0),
        # gender=data.get("gender", ""),
        id=data.get("id", 0),
        country=parse_country(data.get("country", {})),
        entity_type=data.get("entityType", ""),
        team_colors=TeamColors(
            primary=data.get("teamColors", {}).get("primary", "#000000"),
            secondary=data.get("teamColors", {}).get("secondary", "#000000"),
            text=data.get("teamColors", {}).get("text", "#000000"),
        ),
    )
