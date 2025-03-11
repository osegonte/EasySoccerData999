"""
This example shows how to get tournament brackets.
In this case, we get the brackets of the UEFA Champions League 24/25.
Only a few details are printed.

The output will be something like:

UEFA Champions League 24/25, Knockout Phase
Current round is 2

Round: 2 Description: 1/8 has: 8 matchs
Match: PSV Eindhoven 1 - 7 Arsenal

Match: Real Madrid 2 - 1 Atlético Madrid

Match: Paris Saint-Germain 0 - 1 Liverpool

Match: Club Brugge KV 1 - 3 Aston Villa

...........
"""

import esd


client = esd.SofascoreClient()

"""
Each id is obtained using the client.search() method.
In this case we skip the search and use the ids directly.
"""
uefa_tournament_id = 7
last_season_id = 61644

brackets: list[esd.sofascore.Bracket] = client.get_tournament_brackets(
    uefa_tournament_id, last_season_id
)

# Uefa has only one bracket
unique_bracket: esd.sofascore.Bracket = brackets[0]

# Print the name of the bracket (e.g. "UEFA Champions League 24/25, Knockout Phase")
print(unique_bracket.name)
print("Current round is", unique_bracket.current_round)

print()

for round in unique_bracket.rounds:

    if round.order < unique_bracket.current_round:
        # Skip past rounds
        continue

    print(
        "Round:",
        round.order,
        "Description:",
        round.description,
        "has:",
        len(round.blocks),
        "matchs",
    )

    for block in round.blocks:

        if len(block.events) == 0:
            print("No events data available")
            continue

        first_match: esd.sofascore.Event = client.get_event(block.events[0])
        home_team = first_match.home_team.name
        away_team = first_match.away_team.name

        print(
            "Match:",
            home_team,
            block.home_team_score,
            "-",
            block.away_team_score,
            away_team,
        )

        print()
