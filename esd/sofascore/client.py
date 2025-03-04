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

    def get_events(
        self, date: str = None, status: str = "nostarted"
    ) -> typing.List[Event]:
        """
        Get the scheduled events.

        Args:
            date (str): The date of the events in the format "YYYY-MM-DD".
            status (str): The status of the events. (default is "nostarted")

            Available options:
            - "nostarted": Events that have not started yet.
            - "inprogress": Events that are currently live.
            - "finished": Events that have finished.

        Returns:
            list[Event]: The scheduled events.
        """
        return self.__service.get_events(date, status)
