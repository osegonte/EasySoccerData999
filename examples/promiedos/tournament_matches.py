"""
In this example we will get the matches of a tournament.

Output example:

Champions League uefa-champions-league
Current filter is Cuartos De Final
Matches:
Bayern Munich vs Inter Milan
Arsenal vs Real Madrid
FC Barcelona vs Borussia Dortmund
PSG vs Aston Villa
Borussia Dortmund vs FC Barcelona
Aston Villa vs PSG
Inter Milan vs Bayern Munich
Real Madrid vs Arsenal

"""

from esd import PromiedosClient, PromiedosTypes

client = PromiedosClient()

# "fhc" is the ID of uefa champions league
tournament: PromiedosTypes.Tournament = client.get_tournament("fhc")

# print some info
print(tournament.league.name, tournament.league.slug)

# Get the current stage for getting the matches
stage: PromiedosTypes.Stage = tournament.current_stage()
print("Current stage is", stage.name)

# Get the matches for the tournament
matches: list[PromiedosTypes.Match] = client.get_tournament_matchs(
    tournament.league.id, stage.id
)

# Print the matches
print("Matches:")
for match in matches:
    print(match.home_team.name, "vs", match.away_team.name)
