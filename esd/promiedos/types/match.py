"""
This module contains the Match dataclass and its parser.
"""

from dataclasses import dataclass, field
from datetime import datetime
from .team import Team, parse_team
from .status import Status, parse_status
from .scores import Scores, parse_scores
from .tvnetwork import TVNetwork, parse_tv_network
from .odds import MainOdds, parse_main_odds
from .league import League
from .players import Players


@dataclass
class Match:
    """
    The match data.
    """

    id: str = field(default=None)
    stage_round_name: str = field(default=None)
    winner: int = field(default=None)
    teams: list[Team] = field(default_factory=list)
    scores: Scores = field(default_factory=Scores)
    slug: str = field(default="")
    status: Status = field(default_factory=Status)
    start_time: float = field(default=0.0)
    current_time: int = field(default=0)
    time_to_display: str = field(default=None)
    time_status_to_display: str = field(default=None)
    tv_networks: list[TVNetwork] = field(default_factory=list)
    main_odds: MainOdds = field(default_factory=MainOdds)
    league: League = field(default_factory=League)
    players: Players = field(default_factory=Players)


def parse_match(data: dict) -> Match:
    """
    Parse the match data.
    """
    teams_data = data.get("teams", [])
    scores_data = data.get("scores", [])
    tv_networks_data = data.get("tv_networks", [])
    date_str = data.get("start_time", "01-01-1970 00:00")
    dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M")

    return Match(
        id=data.get("id"),
        stage_round_name=data.get("stage_round_name"),
        winner=data.get("winner", None),
        scores=parse_scores(scores_data),
        teams=[parse_team(team) for team in teams_data],
        slug=data.get("url_name", ""),
        status=parse_status(data.get("status", {})),
        start_time=dt.timestamp(),
        current_time=data.get("game_time", 0),
        time_to_display=data.get("game_time_to_display", ""),
        time_status_to_display=data.get("game_time_status_to_display", ""),
        tv_networks=[parse_tv_network(tv) for tv in tv_networks_data],
        main_odds=parse_main_odds(data.get("main_odds", {})),
    )
