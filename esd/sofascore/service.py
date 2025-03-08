"""
Sofascore service module
"""

from ..utils import get_json, get_today
from .endpoints import SofascoreEndpoints
from .types import (
    Event,
    parse_events,
    parse_team_ex,
    parse_player,
    MatchStats,
    parse_match_stats,
)


class SofascoreService:
    """
    A class to represent the SofaScore service.
    """

    def __init__(self):
        """
        Initializes the SofaScore service.
        """
        self.endpoints = SofascoreEndpoints()

    def get_events(self, date: str = None) -> list[Event]:
        """
        Get the scheduled events.

        Args:
            date (str): The date of the events in the format "YYYY-MM-DD".

        Returns:
            dict: The scheduled events.
        """
        if not date:
            date = get_today()
        try:
            url = self.endpoints.events_endpoint.format(date=date)
            return parse_events(get_json(url)["events"])
        except Exception as exc:
            raise exc

    def get_live_events(self) -> list[Event]:
        """
        Get the live events.

        Returns:
            list[Event]: The live events.
        """
        try:
            url = self.endpoints.live_events_endpoint
            return parse_events(get_json(url)["events"])
        except Exception as exc:
            raise exc

    def get_match_stats(self, event_id: int) -> dict:
        """
        Get the match statistics.

        Args:
            event_id (int): The event id.

        Returns:
            dict: The match statistics.
        """
        try:
            url = self.endpoints.match_stats_endpoint(event_id)
            data = get_json(url).get("statistics", {})
            return parse_match_stats(data)
        except Exception as exc:
            raise exc

    def get_team(self, team_id: int) -> dict:
        """
        Get the team information.

        Args:
            team_id (int): The team id.

        Returns:
            dict: The team information.
        """
        try:
            url = self.endpoints.team_endpoint(team_id)
            data = get_json(url)["team"]
            return parse_team_ex(data)
        except Exception as exc:
            raise exc

    def get_team_players(self, team_id: int) -> dict:
        """
        Get the team players.

        Args:
            team_id (int): The team id.

        Returns:
            dict: The team players.
        """
        try:
            url = self.endpoints.team_players_endpoint(team_id)
            return [
                parse_player(player["player"]) for player in get_json(url)["players"]
            ]
        except Exception as exc:
            raise exc
