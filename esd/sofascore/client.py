"""
This module contains the client class for interacting with the Sofascore API.
"""

from __future__ import annotations
from .service import SofascoreService
from .types import EntityType, Event, TeamEx, Player, MatchStats, Lineups


class SofascoreClient:
    """
    A class to represent the client for interacting with the Sofascore API.
    """

    def __init__(self) -> None:
        """
        Initializes the Sofascore client.
        """
        self.__service = SofascoreService()

    def get_events(self, date: str = None, live: bool = False) -> list[Event]:
        """
        Get the scheduled events.

        Args:
            date (str): The date of the events in the format "YYYY-MM-DD".
            live (bool): Whether to get the live events (more precise).

        Returns:
            list[Event]: The scheduled events.
        """
        if live:
            return self.__service.get_live_events()
        return self.__service.get_events(date)

    def get_match_stats(self, event_id: int) -> MatchStats:
        """
        Get the match statistics by event id.

        Args:
            event_id (int): The event id (also known as match id).

        Returns:
            MatchStats: The match statistics.
        """
        return self.__service.get_match_stats(event_id)

    def get_match_lineups(self, event_id: int) -> Lineups:
        """
        Get the match lineups.

        Args:
            event_id (int): The event id.

        Returns:
            Lineups: The match lineups.
        """
        return self.__service.get_match_lineups(event_id)

    def get_team(self, team_id: int) -> TeamEx:
        """
        Get detailed information about a team.

        Args:
            team_id (int): The team id.

        Returns:
            TeamEx: The team information.
        """
        team: TeamEx = self.__service.get_team(team_id)
        players: list[Player] = self.__service.get_team_players(team_id)
        team.players = players
        return team

    def get_team_players(self, team_id: int) -> list[Player]:
        """
        Get the players of a team.

        Args:
            team_id (int): The team id.

        Returns:
            list[Player]: The players of the team.
        """
        return self.__service.get_team_players(team_id)

    def search(
        self, query: str, entity: str | EntityType = EntityType.ALL
    ) -> list[Event | TeamEx | Player]:
        """
        Search query for matches, teams, players, and tournaments.

        Args:
            query (str): The search query.
            entity (str, EntityType): The entity type to search for.

        Returns:
            dict: The search results.
        """
        if isinstance(entity, str):
            entity = EntityType(entity)
        return self.__service.search(query, entity)
