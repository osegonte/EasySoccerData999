"""
This example shows how to get the standings of a tournament.
In this case, we get the standings of the last season of the UEFA Champions League.

The tournament id is 7 and the last season id is 61644.

Example output:

1. Liverpool 21 points
Matches: 8 Wins: 7 Draws: 0 Losses: 1
2. Barcelona 19 points
Matches: 8 Wins: 6 Draws: 1 Losses: 1
3. Arsenal 19 points
Matches: 8 Wins: 6 Draws: 1 Losses: 1
4. Inter 19 points
Matches: 8 Wins: 6 Draws: 1 Losses: 1
5. Atlético Madrid 18 points
Matches: 8 Wins: 6 Draws: 0 Losses: 2

"""

import esd


client = esd.SofascoreClient()

"""
Each id is obtained using the client.search() method.
In this case we skip the search and use the ids directly.
Also see the search tournament example.
"""
uefa_tournament_id = 7
last_season_id = 61644

standings: list[esd.sofascore.Standing] = client.get_tournament_standings(
    uefa_tournament_id, last_season_id
)

# in this case uefa champions league has only one standing
current_standing = standings[0]

for item in current_standing.items:
    print(f"{item.position}. {item.team.name} {item.points} points")
    print(
        f"Matches: {item.matches}Wins: {item.wins} Draws: {item.draws} Losses: {item.losses}"
    )
