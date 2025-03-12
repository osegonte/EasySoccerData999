"""
This module contains the client class for interacting with the FBref website.
"""

from __future__ import annotations
from .service import FBrefService
from .types import Match


class FBrefClient:
    """
    A class to represent the client for interacting with the FBref website.
    """

    def __init__(self, language: str = "en") -> None:
        """
        Initializes the Sofascore client.
        """
        self.__service = FBrefService(language=language)

    def get_matchs(self, date: str = None) -> list[Match]:
        """
        Get the scheduled matchs.

        Args:
            date (str): The date of the matchs in the format "YYYY-MM-DD".

        Returns:
            list[Match]: The scheduled matchs.
        """
        return self.__service.get_matchs(date)

    def get_match_details(self, match_id: str) -> None:
        """
        TODO: Get the details of a match.
        """
