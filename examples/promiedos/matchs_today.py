"""
In this example, we will get all the events using PromiedosClient and print them.

The output will be something like:

For Liga Profesional Argentina - today
Argentinos 0 - 0 Aldosivi
Godoy Cruz 0 - 0 San Lorenzo

For Primera Nacional - today
All Boys 0 - 0 San Miguel

and more...

"""

import esd

client = esd.PromiedosClient()

events: list[esd.promiedos.Event] = client.get_events()

for event in events:
    print(f"For {event.league.name} - {event.date}")
    for match in event.matches:
        print(
            f"{match.teams[0].short_name} {match.scores.home} - {match.scores.away} {match.teams[1].short_name}"
        )
    print()
