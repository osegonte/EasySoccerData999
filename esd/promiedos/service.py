"""
Promiedos service module.
"""

from __future__ import annotations
from ..utils import get_json
from .endpoints import PromiedosEndpoints


class PromiedosService:
    """
    A class to represent the Promiedos service.
    """

    def __init__(self):
        """
        Initializes the Promiedos service.
        """
        self.endpoints = PromiedosEndpoints()

    def get_events(self, date: str = "today") -> dict:
        """
        Get the events for the given date.

        Args:
            date (str): The date to get the events. Defaults to "today".

        Returns:
            dict: The events for the given date.
        """
        available_dates = ["today", "yesterday", "tomorrow", "DD-MM-YYYY"]
        try:
            url = self.endpoints.events_endpoint.format(date=date)
            data = get_json(url)["leagues"]
            return data
        except Exception as exc:
            raise exc
