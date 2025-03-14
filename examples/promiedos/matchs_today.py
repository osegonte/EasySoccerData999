"""
In this example, we will get all the events using PromiedosClient and print them.

The output will be something like:

League name: Liga Profesional Argentina - today
Argentinos Juniors 0 - 0 Aldosivi
Status: Prog. -
-------------------
Godoy Cruz 0 - 0 San Lorenzo
Status: Prog. -
-------------------

League name: LaLiga - today
Las Palmas 0 - 1 Alavés
Status: Entretiempo - 45'
Formations -> 4-2-3-1 - 4-4-2
-------------------

League name: Serie A - today
Genoa 2 - 0 Lecce
Status: Segundo Tiempo - 51'
Formations -> 4-2-3-1 - 4-2-3-1
-------------------

and more...

"""

import esd

client = esd.PromiedosClient()
events = client.get_events()

for event in events:
    print(f"League name: {event.league.name} - {event.date}")
    for match in event.matches:
        home_team = match.teams[0]
        away_team = match.teams[1]
        print(
            f"{home_team.name} {match.scores.home} - {match.scores.away} {away_team.name}"
        )
        print(f"Status: {match.status.name} - {match.time_to_display}")
        if match.status.enum == 2:  # In progress,
            details = client.get_match(match.id)
            print(
                f"Formations -> {details.players.lineups.home_team.formation} - {details.players.lineups.away_team.formation}"
            )
        print("-------------------")
    print()
