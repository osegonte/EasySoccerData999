"""
In this example we will get all the stages of a tournament
also we will get the matches of the first stage.

Output example:

Fecha 1 False
Fecha 2 False
Fecha 3 False
Fecha 4 False
Fecha 5 False
Fecha 6 False
Fecha 7 False
Fecha 8 False
Playoff False
Octavos de Final False
Cuartos De Final True

Monaco vs Aston Villa
Atalanta vs Sturm Graz
Slovan Bratislava vs Stuttgart
and more...

"""
from esd import PromiedosClient, PromiedosTypes

client = PromiedosClient()

# "fhc" is the ID of uefa champions league
tournament: PromiedosTypes.Tournament = client.get_tournament("fhc")

# get all stages
stages: list[PromiedosTypes.Stage] = tournament.stages

# print the stages
for stage in stages:
    print(stage.name, stage.selected)

# now we will use the first stage
stage = stages[0]
matches = client.get_tournament_matchs(tournament.league.id, stage.id)
for match in matches:
    print(match.home_team.name, "vs", match.away_team.name)