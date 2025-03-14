"""
The status of a match.
"""

from dataclasses import dataclass, field


@dataclass
class Status:
    """
    The status of a match.
    """

    enum: int = field(default=0)
    name: str = field(default=None)
    short_name: str = field(default=None)
    symbol_name: str = field(default=None)


def parse_status(data: dict) -> Status:
    """
    Parse the status data.
    """
    return Status(
        enum=data.get("enum", 0),
        name=data.get("name"),
        short_name=data.get("short_name"),
        symbol_name=data.get("symbol_name"),
    )
