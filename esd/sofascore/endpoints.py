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

    @property
    def live_events_endpoint(self) -> str:
        """
        Returns the URL of the endpoint to get the live events.

        Returns:
            str: The URL of the endpoint to get the live events.
        """
        return self.base_url + "/sport/football/events/live"

    def search_endpoint(self, query: str, entity_type: str) -> str:
        """
        Returns the URL of the endpoint to search for entities.

        Args:
            query (str): The search query.
            entity_type (str): The entity type.

        Returns:
            str: The URL of the endpoint to search for entities.
        """
        return f"{self.base_url}/search/{entity_type}?q={query}&page=0"

    def team_endpoint(self, team_id: int) -> str:
        """
        Returns the URL of the endpoint to get the team information.

        Args:
            team_id (int): The team id.

        Returns:
            str: The URL of the endpoint to get the team information.
        """
        return f"{self.base_url}/team/{team_id}"

    def team_players_endpoint(self, team_id: int) -> str:
        """
        Returns the URL of the endpoint to get the team players.

        Args:
            team_id (int): The team id.

        Returns:
            str: The URL of the endpoint to get the team players.
        """
        return self.team_endpoint(team_id) + "/players"

    def match_stats_endpoint(self, event_id: int) -> str:
        """
        Returns the URL of the endpoint to get the match statistics.

        Args:
            event_id (int): The event id.
        
        Returns:
            str: The URL of the endpoint to get the match statistics.
        """
        return f"{self.base_url}/event/{event_id}/statistics"

    def match_probabilities_endpoint(self, event_id: int) -> str:
        """
        Returns the URL of the endpoint to get the match probabilities.

        Args:
            event_id (int): The event id.
        
        Returns:
            str: The URL of the endpoint to get the match probabilities.
        """
        return f"{self.base_url}/event/{event_id}/win-probability"

    def match_lineups_endpoint(self, event_id: int) -> str:
        """
        Returns the URL of the endpoint to get the match lineups.

        Args:
            event_id (int): The event id.
        
        Returns:
            str: The URL of the endpoint to get the match lineups.
        """
        return f"{self.base_url}/event/{event_id}/lineups"