"""
FBref service module.
"""

from __future__ import annotations
from ..utils import get_today, get_document
from .endpoints import FBrefEndpoints
from .types import Match, parse_matchs


class FBrefService:
    """
    A class to represent the FBref service.
    """

    def __init__(self, language: str = "en") -> None:
        """
        Initializes the FBref service.
        """
        self.endpoints = FBrefEndpoints(language=language)

    def get_matchs(self, date: str = None) -> list[Match]:
        """
        Get the scheduled matchs.

        Args:
            date (str): The date of the matchs in the format "YYYY-MM-DD".

        Returns:
            list[Match]: The scheduled
        """
        try:
            if not date:
                date = get_today()
            url = self.endpoints.matchs_endpoint.format(date=date)
            document = get_document(url)
            return parse_matchs(document)
        except Exception as exc:
            raise exc

    def get_match_details(self, match_id: str) -> None:
        """
        TODO: Get the details of a match.
        """
