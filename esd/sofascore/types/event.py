from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .team import TeamSummary, parse_team_summary, TeamScore, parse_team_score


@dataclass
class Category:
    id: int
    country: Dict
    name: str
    slug: str
    flag: str


@dataclass
class UniqueTournament:
    name: str
    slug: str
    category: Category
    userCount: int
    hasPerformanceGraphFeature: bool
    id: int
    hasEventPlayerStatistics: bool
    displayInverseHomeAwayTeams: bool


@dataclass
class Tournament:
    name: str
    slug: str
    category: Category
    uniqueTournament: UniqueTournament
    priority: int
    id: int


@dataclass
class Season:
    name: str
    year: str
    editor: bool
    seasonCoverageInfo: Dict
    id: int


@dataclass
class RoundInfo:
    round: int
    name: str
    cupRoundType: int


@dataclass
class Status:
    code: int = 0
    description: str = "n/a"
    type: str = "n/a"


@dataclass
class TimeEvent:
    first_injury_time: int = 0
    second_injury_time: int = 0
    current_period_start: int = 0


@dataclass
class Event:
    # tournament: Tournament
    # season: Season
    round_info: RoundInfo = field(default_factory=RoundInfo)
    id: int = 0
    custom_id: str = None
    status: Status = field(default_factory=Status)
    home_team: TeamSummary = field(default_factory=TeamSummary)
    home_score: TeamScore = field(default_factory=TeamScore)
    away_team: TeamSummary = field(default_factory=TeamSummary)
    away_score: TeamScore = field(default_factory=TeamScore)
    coverage: int = 0
    time: TimeEvent = field(default_factory=TimeEvent)
    # changes: Optional[Dict] = field(default_factory=dict)
    start_timestamp: int = 0
    slug: str = "n/a"
    final_result_only: bool = False
    feed_locked: bool = False
    # some fields are not included
    # has_global_highlights: bool = False
    # is_editor: bool = False
    # detail_id: int = 1
    # crowdsourcingDataDisplayEnabled: bool = False


def parse_time_event(data: Dict) -> TimeEvent:
    """
    Parse the time event data.

    Args:
        data (dict): The time event data.

    Returns:
        TimeEvent: The time event object.
    """
    return TimeEvent(
        first_injury_time=data.get(
            "injuryTime1", 0
        ),  # example 4 -> aggregate 4 minutes
        second_injury_time=data.get("injuryTime2", 0),
        current_period_start=data.get("currentPeriodStartTimestamp", 0),
    )


def parse_round_info(data: Dict) -> RoundInfo:
    """
    Parse the round info data.

    Args:
        data (dict): The round info data.

    Returns:
        RoundInfo: The round info object.
    """
    return RoundInfo(
        round=data.get("round", 0),
        name=data.get("name", "n/a"),
        cupRoundType=data.get("cupRoundType", 0),
    )


def parse_status(data: Dict) -> Status:
    """
    Parse the status data.

    Args:
        data (dict): The status data.

    Returns:
        Status: The status object.
    """
    return Status(
        code=data.get("code", 0),
        description=data.get("description", "n/a"),
        type=data.get("type", "n/a"),
    )


def parse_events(events: List[Dict], target_status: str) -> List[Event]:
    """
    Parse the events data.

    Args:
        events (list): The events data.
        target_status (str): The target status of the events.

    Returns:
        list[Event]: The parsed events data.
    """
    return [
        Event(
            id=event.get("id"),
            start_timestamp=event.get("startTimestamp"),
            slug=event.get("slug"),
            custom_id=event.get("customId"),
            feed_locked=event.get("feedLocked"),
            final_result_only=event.get("finalResultOnly"),
            coverage=event.get("coverage"),
            time=parse_time_event(event.get("time", {})),
            home_team=parse_team_summary(event.get("homeTeam", {})),
            away_team=parse_team_summary(event.get("awayTeam", {})),
            home_score=parse_team_score(event.get("homeScore", {})),
            away_score=parse_team_score(event.get("awayScore", {})),
            status=parse_status(event.get("status", {})),
            round_info=parse_round_info(event.get("roundInfo", {})),
        )
        for event in events
        if event.get("status", {}).get("type") == target_status
    ]
