"""
This example shows how to get match lineups.
In this case, we get the first live match and print the confirmed lineups.

The output will be something like:

İstanbulspor vs Boluspor
Confirmed lineups: True
FORMATION Boluspor : 4-2-3-1

Çağlar Şahin Akbaba | G | 0
-------------------
Ali Ülgen | D | 0
-------------------
Fethi Özer | D | 0
-------------------
Onur Ulas | D | 0
-------------------
Enes Alic  | D | 0
-------------------
Mário Balbúrdia | M | 0
-------------------
Oğuz Kağan Güçtekin | M | 0
-------------------
Florent Hasani | M | 0
-------------------
Jefferson Junior | M | 0
-------------------
Paul Mukairu | M | 0
-------------------
Eren Erdoğan | F | 0
-------------------

FORMATION İstanbulspor : 4-2-3-1
Isa Dogan | G | 1
-------------------
Yunus Bahadir | D | 2
-------------------
Okan Erdoğan | D | 23
-------------------
Fatih Tultak | D | 4
-------------------
Racine Coly | D | 13
-------------------
Kubilay Sönmez | M | 14
-------------------
Kerem Şen | M | 16
-------------------
David Sambissa | D | 7
-------------------
Florian Loshaj | M | 34
-------------------
Gaoussou Diarra | M | 19
-------------------
Mario Krstovski | F | 77
-------------------
"""

import esd

client = esd.SofascoreClient()
matchs = client.get_events(live=True)
match = matchs[0]

print(match.away_team.name, "vs", match.home_team.name)

lineups = client.get_match_lineups(match.id)
print("Confirmed lineups:", lineups.confirmed)

print("FORMATION", match.home_team.name, ":", lineups.home.formation)
home_players = lineups.home.players
for player in home_players:
    info: esd.sofascore.Player = player.info
    if player.substitute:
        # ignore substitutes
        continue
    print(info.name, "|", info.position, "|", info.shirt_number)
    print("-------------------")

print("FORMATION", match.away_team.name, ":", lineups.away.formation)
away_players = lineups.away.players
for player in away_players:
    info: esd.sofascore.Player = player.info
    if player.substitute:
        # ignore substitutes
        continue
    print(info.name, "|", info.position, "|", player.info.jersey_number)
    print("-------------------")
