"""
Promiedos service module.
"""

from __future__ import annotations
from ..utils import get_json, is_available_date
from .endpoints import PromiedosEndpoints
from .exceptions import InvalidDate


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
        available_dates = ["today", "yesterday", "tomorrow"]
        if date not in available_dates:
            try:
                is_available_date(date, r"\d{4}-\d{2}-\d{2}")
            except Exception as exc:
                raise InvalidDate(
                    "Invalid date format. Use DD-MM-YYYY or today, yesterday, or tomorrow."
                ) from exc
        try:
            url = self.endpoints.events_endpoint.format(date=date)
            data = get_json(url)["leagues"]
            return data
        except Exception as exc:
            raise exc
