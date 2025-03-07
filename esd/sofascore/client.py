"""
This module contains the client class for interacting with the Sofascore API.
"""

import typing
from .service import SofascoreService
from .types import Event


class SofascoreClient:
    """
    A class to represent the client for interacting with the Sofascore API.
    """

    def __init__(self) -> None:
        """
        Initializes the Sofascore client.
        """
        self.__service = SofascoreService()

    def get_events(self, date: str = None, live: bool = False) -> typing.List[Event]:
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

    def get_team(self, team_id: int) -> dict:
        """
        Get detailed information about a team.

        Args:
            team_id (int): The team id.

        Returns:
            dict: The team information.
        """
        return self.__service.get_team(team_id)
