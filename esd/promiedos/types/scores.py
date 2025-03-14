"""
Scores data type.
"""

from dataclasses import dataclass, field


@dataclass
class Scores:
    """
    Scores data type.
    """

    home: int = field(default=0)
    away: int = field(default=0)


def parse_scores(data: list) -> Scores:
    """
    Parse the scores data.
    """
    if not data:
        return Scores()
    return Scores(home=int(data[0]), away=int(data[1]))
