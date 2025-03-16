"""
In this example, we will get all the events using PromiedosClient and print them.

The output will be something like:

League name: MLS - today
San Jose Earthquakes 1 - 2 Colorado Rapids
Status: Segundo Tiempo - 90+5'
Goal: Cristian Arango (45'+1, is penalty: False)
Goal: Cole Bassett (38', is penalty: False)
Goal: Calvin Harris (71', is penalty: False)
-----------------
San Diego FC 1 - 1 Columbus Crew
Status: Segundo Tiempo - 90+2'
Goal: Onni Valakari (69', is penalty: False)
Goal: Max Arfsten (13', is penalty: False)
-----------------
Portland Timbers 0 - 0 Los Angeles Galaxy
Status: Prog. -
-----------------
Atlanta United 0 - 0 Inter Miami
Status: Prog. -
-----------------

and more...

"""

import esd

client = esd.PromiedosClient()
events = client.get_events()

for event in events:
    print(f"League name: {event.league.name} - {event.date}")
    for match in event.matches:
        print(
            f"{match.home_team.name} {match.scores.home} - {match.scores.away} {match.away_team.name}"
        )

        print(f"Status: {match.status.name} - {match.time_to_display}")
        goals = match.home_team.goals + match.away_team.goals
        if goals:
            for goal in goals:
                print(
                    f"Goal: {goal.full_name} ({goal.time_to_display}, is penalty: {goal.is_penalty})"
                )
        print("-----------------")
    print()
