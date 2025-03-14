"""
This module contains the client class for interacting with the Promiedos API.
"""

from __future__ import annotations
from .service import PromiedosService
from .types import Event


class PromiedosClient:
    """
    A class to represent the client for interacting with the Promiedos API.
    """

    def __init__(self) -> None:
        """
        Initializes the Promiedos client.
        """
        self.__service = PromiedosService()

    def get_events(self, date: str = "today") -> list[Event]:
        """
        Get the events for the given date.

        Args:
            date (str): The date to get the events. Defaults to "today".

        Returns:
            list[Event]: The events for the given date.
        """
        return self.__service.get_events(date)
