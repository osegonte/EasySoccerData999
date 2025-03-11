"""
Sofascore service module
"""

from __future__ import annotations
from ..utils import get_json, get_today
from .endpoints import SofascoreEndpoints
from .types import (
    Event,
    parse_event,
    parse_events,
    parse_player,
    parse_team,
    Team,
    Player,
    MatchStats,
    parse_match_stats,
    Lineups,
    parse_lineups,
    EntityType,
)


class SofascoreService:
    """
    A class to represent the SofaScore service.
    """

    def __init__(self):
        """
        Initializes the SofaScore service.
        """
        self.endpoints = SofascoreEndpoints()

    def get_events(self, date: str = None) -> list[Event]:
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
            return parse_events(get_json(url)["events"])
        except Exception as exc:
            raise exc

    def get_live_events(self) -> list[Event]:
        """
        Get the live events.

        Returns:
            list[Event]: The live events.
        """
        try:
            url = self.endpoints.live_events_endpoint
            return parse_events(get_json(url)["events"])
        except Exception as exc:
            raise exc

    def get_match_lineups(self, event_id: int) -> Lineups:
        """
        Get the match lineups.

        Args:
            event_id (int): The event id.

        Returns:
            dict: The match lineups.
        """
        try:
            url = self.endpoints.match_lineups_endpoint(event_id)
            return parse_lineups(get_json(url))
        except Exception as exc:
            raise exc

    def get_match_stats(self, event_id: int) -> MatchStats:
        """
        Get the match statistics.

        Args:
            event_id (int): The event id.

        Returns:
            MatchStats: The match statistics.
        """
        try:
            url = self.endpoints.match_stats_endpoint(event_id)
            data = get_json(url).get("statistics", {})
            url = self.endpoints.match_probabilities_endpoint(event_id)
            win_probabilities = get_json(url).get("winProbability", {})
            return parse_match_stats(data, win_probabilities)
        except Exception as exc:
            raise exc

    def get_team(self, team_id: int) -> Team:
        """
        Get the team information.

        Args:
            team_id (int): The team id.

        Returns:
            Team: The team information
        """
        try:
            url = self.endpoints.team_endpoint(team_id)
            data = get_json(url)["team"]
            return parse_team(data)
        except Exception as exc:
            raise exc

    def get_team_players(self, team_id: int) -> list[Player]:
        """
        Get the team players.

        Args:
            team_id (int): The team id.

        Returns:
            list[Player]: The players of the team.
        """
        try:
            url = self.endpoints.team_players_endpoint(team_id)
            return [
                parse_player(player["player"]) for player in get_json(url)["players"]
            ]
        except Exception as exc:
            raise exc

    def search(
        self, query: str, entity: EntityType = EntityType.ALL
    ) -> list[Event | Team | Player]:
        """
        Search query for matches, teams, players, and tournaments.

        Args:
            query (str): The search query.
            entity (EntityType): The entity type to search for.

        Returns:
            a list of Event, Team, or Player objects.
        """
        try:
            entity_type = entity.value
            url = self.endpoints.search_endpoint(query=query, entity_type=entity_type)
            results = get_json(url)["results"]

            specific_parsers = {
                EntityType.TEAM: parse_team,
                EntityType.PLAYER: parse_player,
                EntityType.EVENT: parse_event,
                EntityType.TOURNAMENT: lambda x: x,
            }

            if entity == EntityType.ALL:
                type_parsers = {
                    "team": parse_team,
                    "player": parse_player,
                    "event": parse_events,
                }
                entities = []
                for result in results:
                    result_type = result.get("type")
                    entity_data = result.get("entity")
                    parser = type_parsers.get(result_type, lambda x: x)
                    entities.append(parser(entity_data))
                return entities
            parser = specific_parsers.get(entity, lambda x: x)
            return [parser(result.get("entity")) for result in results]
        except Exception as exc:
            raise exc
