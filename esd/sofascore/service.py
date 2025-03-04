"""
Sofascore service module
"""

from ..utils import get_json, get_today
from .endpoints import SofascoreEndpoints
from .types import Event, parse_events


class SofascoreService:
    """
    A class to represent the SofaScore service.
    """

    def __init__(self):
        """
        Initializes the SofaScore service.
        """
        self.endpoints = SofascoreEndpoints()

    def get_events(self, date: str = None, status: str = "nostarted") -> list[Event]:
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
            data = get_json(url)["events"]
            return parse_events(data, target_status=status)
        except Exception as exc:
            raise exc
