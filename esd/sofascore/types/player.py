from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ProposedMarketValueRaw:
    value: int = field(default=0)
    currency: str = field(default=None)


@dataclass
class Player:
    name: str = field(default=None)
    slug: str = field(default=None)
    short_name: str = field(default=None)
    position: str = field(default=None)
    jersey_number: str = field(default=None)
    height: int = field(default=0)
    preferred_foot: str = field(default=None)
    # userCount: int
    gender: str = field(default=None)
    id: int = field(default=0)
    shirt_number: int = field(default=0)
    date_of_birth: int = field(default=0)
    contract_until: int = field(default=0)
    market_value: int = field(default=0)  # proposed
    # market_value_raw: ProposedMarketValueRaw = field(
    #     default_factory=ProposedMarketValueRaw
    # )
    # fieldTranslations: Dict[str, Dict[str, str]]


def parse_proposed_market_value_raw(data: dict) -> ProposedMarketValueRaw:
    return ProposedMarketValueRaw(value=data["value"], currency=data["currency"])


def parse_player(data: dict) -> Player:
    return Player(
        name=data["name"],
        slug=data["slug"],
        short_name=data["shortName"],
        position=data["position"],
        jersey_number=data["jerseyNumber"],
        height=data["height"],
        preferred_foot=data["preferredFoot"],
        # userCount=data["userCount"],
        gender=data["gender"],
        id=data["id"],
        shirt_number=data["shirtNumber"],
        date_of_birth=data["dateOfBirthTimestamp"],
        contract_until=data["contractUntilTimestamp"],
        market_value=data["proposedMarketValue"],
        # market_value_raw=parse_proposed_market_value_raw(
        #     data["proposedMarketValueRaw"]
        # ),
        # fieldTranslations=data["fieldTranslations"],
    )
