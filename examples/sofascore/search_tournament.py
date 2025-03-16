"""
This example shows how to search for tournaments and get the seasons.
In this case, we search for tournaments that contain the word "uefa".
Once we have the tournament, we get the seasons.

The output will be something like:

7, UEFA Champions League, uefa-champions-league
---------------------------
679, UEFA Europa League, uefa-europa-league
........
........

Seasons:
61644, UEFA Champions League 24/25
52162, UEFA Champions League 23/24
......
......
12, Champions League 03/04
"""

import esd

client = esd.SofascoreClient()

# search for tournaments
tournaments: list[esd.sofascore.Tournament] = client.search(
    "uefa", entity=esd.sofascore.EntityType.TOURNAMENT
)

for tournament in tournaments:
    print(f"{tournament.id}, {tournament.name}, {tournament.slug}")
    print("---------------------------")

# selecting uefa champions league
uefa = tournaments[0]
seasons: list[esd.sofascore.Season] = client.get_tournament_seasons(uefa.id)

print("Seasons:")
for season in seasons:
    print(f"{season.id}, {season.name}")
