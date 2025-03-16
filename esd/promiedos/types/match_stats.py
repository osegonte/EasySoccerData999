"""
This module contains the definition of the MatchStats class.
"""

from dataclasses import dataclass, field


@dataclass
class StatsItem:
    """
    The stats item data.
    """

    home_value: str = field(default=None)
    home_percentage: str = field(default=None)
    away_value: str = field(default=None)
    away_percentage: str = field(default=None)


@dataclass
class MatchStats:
    """
    The match stats data.
    """

    total_shots: StatsItem = field(default=None)
    shots_on_target: StatsItem = field(default=None)
    possession: StatsItem = field(default=None)
    free_kicks: StatsItem = field(default=None)
    corners: StatsItem = field(default=None)
    offsides: StatsItem = field(default=None)
    yellow_cards: StatsItem = field(default=None)
    red_cards: StatsItem = field(default=None)
    fouls: StatsItem = field(default=None)


def parse_stats(stat: dict[str, any]) -> StatsItem:
    """
    Parse the stats data.
    """
    return StatsItem(
        home_value=stat["values"][0],
        away_value=stat["values"][1],
        home_percentage=stat["percentages"][0],
        away_percentage=stat["percentages"][1],
    )


def parse_match_stats(data: list[dict]) -> MatchStats:
    """
    Parse the match stats data.

    Args:
        data (list[dict]): The match stats data.

    Returns:
        MatchStats: The match stats
    """
    stats_map = {
        "Total Remates": "total_shots",
        "Remates al arco": "shots_on_target",
        "Posesión": "possession",
        "Saques de falta": "free_kicks",
        "Saques de Esquina": "corners",
        "Fueras de Juego": "offsides",
        "Faltas": "fouls",
        "Tarjetas Amarillas": "yellow_cards",
        "Tarjetas Rojas": "red_cards",
    }

    parsed_stats = {}
    for stat in data:
        key = stats_map.get(stat["name"], None)
        if key:
            parsed_stats[key] = parse_stats(stat)

    return MatchStats(**parsed_stats)
