import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


def camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@dataclass
class StatisticItem:
    # name: str = field(default="")
    # home: str = field(default="")
    # away: str = field(default="")
    # compareCode: int = field(default=0)
    # valueType: str = field(default="")
    # renderType: int = field(default=0)
    # key: str = field(default="")
    home_value: float = field(default=0.0)
    away_value: float = field(default=0.0)
    stat_type: str = field(default="")
    home_total: Optional[int] = field(default=None)
    away_total: Optional[int] = field(default=None)


def parse_statistic_item(item: Dict[str, Any]) -> StatisticItem:
    return StatisticItem(
        # name=item.get("name", ""),
        # home=item.get("home", ""),
        # away=item.get("away", ""),
        # compareCode=item.get("compareCode", 0),
        # valueType=item.get("valueType", ""),
        # renderType=item.get("renderType", 0),
        # key=item.get("key", ""),
        stat_type=item.get("statisticsType", ""),
        home_value=item.get("homeValue", 0.0),
        away_value=item.get("awayValue", 0.0),
        home_total=item.get("homeTotal"),
        away_total=item.get("awayTotal"),
    )


@dataclass
class MatchOverviewStats:
    ball_possession: StatisticItem = field(default_factory=StatisticItem)
    expected_goals: StatisticItem = field(default_factory=StatisticItem)
    big_chance_created: StatisticItem = field(default_factory=StatisticItem)
    total_shots_on_goal: StatisticItem = field(default_factory=StatisticItem)
    goalkeeper_saves: StatisticItem = field(default_factory=StatisticItem)
    corner_kicks: StatisticItem = field(default_factory=StatisticItem)
    fouls: StatisticItem = field(default_factory=StatisticItem)
    passes: StatisticItem = field(default_factory=StatisticItem)
    total_tackle: StatisticItem = field(default_factory=StatisticItem)
    free_kicks: StatisticItem = field(default_factory=StatisticItem)
    yellow_cards: StatisticItem = field(default_factory=StatisticItem)


def parse_match_overview_stats(items: List[Dict[str, Any]]) -> MatchOverviewStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return MatchOverviewStats(
        ball_possession=mapping.get("ballPossession", StatisticItem()),
        expected_goals=mapping.get("expectedGoals", StatisticItem()),
        big_chance_created=mapping.get("bigChanceCreated", StatisticItem()),
        total_shots_on_goal=mapping.get("totalShotsOnGoal", StatisticItem()),
        goalkeeper_saves=mapping.get("goalkeeperSaves", StatisticItem()),
        corner_kicks=mapping.get("cornerKicks", StatisticItem()),
        fouls=mapping.get("fouls", StatisticItem()),
        passes=mapping.get("passes", StatisticItem()),
        total_tackle=mapping.get("totalTackle", StatisticItem()),
        free_kicks=mapping.get("freeKicks", StatisticItem()),
        yellow_cards=mapping.get("yellowCards", StatisticItem()),
    )


@dataclass
class ShotsStats:
    total_shots_on_goal: StatisticItem = field(default_factory=StatisticItem)
    shots_on_goal: StatisticItem = field(default_factory=StatisticItem)
    hit_woodwork: StatisticItem = field(default_factory=StatisticItem)
    shots_off_goal: StatisticItem = field(default_factory=StatisticItem)
    blocked_scoring_attempt: StatisticItem = field(default_factory=StatisticItem)
    total_shots_inside_box: StatisticItem = field(default_factory=StatisticItem)
    total_shots_outside_box: StatisticItem = field(default_factory=StatisticItem)


def parse_shots_stats(items: List[Dict[str, Any]]) -> ShotsStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return ShotsStats(
        total_shots_on_goal=mapping.get("totalShotsOnGoal", StatisticItem()),
        shots_on_goal=mapping.get("shotsOnGoal", StatisticItem()),
        hit_woodwork=mapping.get("hitWoodwork", StatisticItem()),
        shots_off_goal=mapping.get("shotsOffGoal", StatisticItem()),
        blocked_scoring_attempt=mapping.get("blockedScoringAttempt", StatisticItem()),
        total_shots_inside_box=mapping.get("totalShotsInsideBox", StatisticItem()),
        total_shots_outside_box=mapping.get("totalShotsOutsideBox", StatisticItem()),
    )


@dataclass
class AttackStats:
    big_chance_scored: StatisticItem = field(default_factory=StatisticItem)
    big_chance_missed: StatisticItem = field(default_factory=StatisticItem)
    touches_in_opp_box: StatisticItem = field(default_factory=StatisticItem)
    fouled_final_third: StatisticItem = field(default_factory=StatisticItem)
    offsides: StatisticItem = field(default_factory=StatisticItem)


def parse_attack_stats(items: List[Dict[str, Any]]) -> AttackStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return AttackStats(
        big_chance_scored=mapping.get("bigChanceScored", StatisticItem()),
        big_chance_missed=mapping.get("bigChanceMissed", StatisticItem()),
        touches_in_opp_box=mapping.get("touchesInOppBox", StatisticItem()),
        fouled_final_third=mapping.get("fouledFinalThird", StatisticItem()),
        offsides=mapping.get("offsides", StatisticItem()),
    )


@dataclass
class PassesStats:
    accurate_passes: StatisticItem = field(default_factory=StatisticItem)
    throw_ins: StatisticItem = field(default_factory=StatisticItem)
    final_third_entries: StatisticItem = field(default_factory=StatisticItem)
    final_third_phase_statistic: StatisticItem = field(default_factory=StatisticItem)
    accurate_long_balls: StatisticItem = field(default_factory=StatisticItem)
    accurate_cross: StatisticItem = field(default_factory=StatisticItem)


def parse_passes_stats(items: List[Dict[str, Any]]) -> PassesStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return PassesStats(
        accurate_passes=mapping.get("accuratePasses", StatisticItem()),
        throw_ins=mapping.get("throwIns", StatisticItem()),
        final_third_entries=mapping.get("finalThirdEntries", StatisticItem()),
        final_third_phase_statistic=mapping.get(
            "finalThirdPhaseStatistic", StatisticItem()
        ),
        accurate_long_balls=mapping.get("accurateLongBalls", StatisticItem()),
        accurate_cross=mapping.get("accurateCross", StatisticItem()),
    )


@dataclass
class DuelsStats:
    duel_won_percent: StatisticItem = field(default_factory=StatisticItem)
    dispossessed: StatisticItem = field(default_factory=StatisticItem)
    ground_duels_percentage: StatisticItem = field(default_factory=StatisticItem)
    aerial_duels_percentage: StatisticItem = field(default_factory=StatisticItem)
    dribbles_percentage: StatisticItem = field(default_factory=StatisticItem)


def parse_duels_stats(items: List[Dict[str, Any]]) -> DuelsStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return DuelsStats(
        duel_won_percent=mapping.get("duelWonPercent", StatisticItem()),
        dispossessed=mapping.get("dispossessed", StatisticItem()),
        ground_duels_percentage=mapping.get("groundDuelsPercentage", StatisticItem()),
        aerial_duels_percentage=mapping.get("aerialDuelsPercentage", StatisticItem()),
        dribbles_percentage=mapping.get("dribblesPercentage", StatisticItem()),
    )


@dataclass
class DefendingStats:
    won_tackle_percent: StatisticItem = field(default_factory=StatisticItem)
    total_tackle: StatisticItem = field(default_factory=StatisticItem)
    interception_won: StatisticItem = field(default_factory=StatisticItem)
    ball_recovery: StatisticItem = field(default_factory=StatisticItem)
    total_clearance: StatisticItem = field(default_factory=StatisticItem)


def parse_defending_stats(items: List[Dict[str, Any]]) -> DefendingStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return DefendingStats(
        won_tackle_percent=mapping.get("wonTacklePercent", StatisticItem()),
        total_tackle=mapping.get("totalTackle", StatisticItem()),
        interception_won=mapping.get("interceptionWon", StatisticItem()),
        ball_recovery=mapping.get("ballRecovery", StatisticItem()),
        total_clearance=mapping.get("totalClearance", StatisticItem()),
    )


@dataclass
class GoalkeepingStats:
    goalkeeper_saves: StatisticItem = field(default_factory=StatisticItem)
    goals_prevented: StatisticItem = field(default_factory=StatisticItem)
    goal_kicks: StatisticItem = field(default_factory=StatisticItem)


def parse_goalkeeping_stats(items: List[Dict[str, Any]]) -> GoalkeepingStats:
    mapping = {item["key"]: parse_statistic_item(item) for item in items}
    return GoalkeepingStats(
        goalkeeper_saves=mapping.get("goalkeeperSaves", StatisticItem()),
        goals_prevented=mapping.get("goalsPrevented", StatisticItem()),
        goal_kicks=mapping.get("goalKicks", StatisticItem()),
    )


@dataclass
class PeriodStats:
    match_overview: MatchOverviewStats = field(default_factory=MatchOverviewStats)
    shots: ShotsStats = field(default_factory=ShotsStats)
    attack: AttackStats = field(default_factory=AttackStats)
    passes: PassesStats = field(default_factory=PassesStats)
    duels: DuelsStats = field(default_factory=DuelsStats)
    defending: DefendingStats = field(default_factory=DefendingStats)
    goalkeeping: GoalkeepingStats = field(default_factory=GoalkeepingStats)


def parse_period_stats(groups: List[Dict[str, Any]]) -> PeriodStats:
    group_mapping = {group["groupName"].lower(): group for group in groups}
    return PeriodStats(
        match_overview=parse_match_overview_stats(
            group_mapping.get("match overview", {}).get("statisticsItems", [])
        ),
        shots=parse_shots_stats(
            group_mapping.get("shots", {}).get("statisticsItems", [])
        ),
        attack=parse_attack_stats(
            group_mapping.get("attack", {}).get("statisticsItems", [])
        ),
        passes=parse_passes_stats(
            group_mapping.get("passes", {}).get("statisticsItems", [])
        ),
        duels=parse_duels_stats(
            group_mapping.get("duels", {}).get("statisticsItems", [])
        ),
        defending=parse_defending_stats(
            group_mapping.get("defending", {}).get("statisticsItems", [])
        ),
        goalkeeping=parse_goalkeeping_stats(
            group_mapping.get("goalkeeping", {}).get("statisticsItems", [])
        ),
    )


@dataclass
class MatchStats:
    all: Optional[PeriodStats] = field(default=None)
    first_half: Optional[PeriodStats] = field(default=None)
    second_half: Optional[PeriodStats] = field(default=None)


def parse_match_stats(data: List[Dict[str, Any]]) -> MatchStats:
    match_stats = MatchStats()
    if not data:
        # No data available
        return match_stats
    for stat in data:
        period = stat.get("period", "").upper()
        groups = stat.get("groups", [])
        period_stats = parse_period_stats(groups)
        if period == "ALL":
            match_stats.all = period_stats
        elif period == "1ST":
            match_stats.first_half = period_stats
        elif period == "2ND":
            match_stats.second_half = period_stats
    return match_stats
