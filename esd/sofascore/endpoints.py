"""
This module contains the endpoints of the SofaScore API.
"""


class SofascoreEndpoints:
    """
    A class to represent the endpoints of the SofaScore API.
    """

    def __init__(self, base_url: str = "https://api.sofascore.com/api/v1") -> None:
        self.base_url = base_url

    @property
    def events_endpoint(self) -> str:
        """
        Returns the URL of the endpoint to get the scheduled events.

        Returns:
            str: The URL of the endpoint to get the scheduled events.
        """
        return self.base_url + "/sport/football/scheduled-events/{date}"
