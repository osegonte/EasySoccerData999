"""
This example shows how to get players from a team.
In this case, we get the players from Liverpool FC.

The output will be something like:

---------------------------------
Luis Díaz, position F, number 7
Date of birth: January 1997
Contract until: June 2027
---------------------------------
Darwin Núñez, position F, number 9
Date of birth: June 1999
Contract until: June 2028
---------------------------------
Cody Gakpo, position F, number 18
Date of birth: May 1999
Contract until: June 2028
---------------------------------
"""

import esd
import datetime

client = esd.SofascoreClient()

teams: list[esd.sofascore.Team] = client.search(
    "Liverpool", entity=esd.sofascore.EntityType.TEAM
)
liverpool_team = teams[0]  # Liverpool FC
liverpool_players = client.get_team_players(liverpool_team.id)

for player in liverpool_players:
    print("---------------------------------")
    print(f"{player.name}, position {player.position}, number {player.jersey_number}")
    date_of_birth = datetime.datetime.fromtimestamp(player.date_of_birth).strftime(
        "%B %Y"
    )
    contract_until = datetime.datetime.fromtimestamp(player.contract_until).strftime(
        "%B %Y"
    )
    print(f"Date of birth: {date_of_birth}")
    print(f"Contract until: {contract_until}")
