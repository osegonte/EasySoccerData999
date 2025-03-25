"""
In this example we will get all filters of a tournament (filters are like stages of the tournament).
In this case we will use the first filter to get the matches of the tournament.

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

# get all filters
filters: list[PromiedosTypes.TournamentFilter] = tournament.filters

# print the filters
for filter in filters:
    print(filter.name, filter.selected)

# in this case we will use the first filter
filter = filters[0]
matches = client.get_tournament_matchs(tournament.league.id, filter.id)
for match in matches:
    print(match.home_team.name, "vs", match.away_team.name)