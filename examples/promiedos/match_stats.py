"""
In this example, we will get all matchs stats using the PromiedosClient.

The output will be something like:

League name: Liga MX - today
Atlas 0 - 0 Club América
Status: Entretiempo - 45'
Formations -> 3-1-4-2 - 4-2-3-1
Possession -> 38% - 62%
Shots -> 9 - 11
Yellow/Red cards -> 0/0 - 1/0
-------------------
League name: MLS - today
San Jose Earthquakes 1 - 2 Colorado Rapids
Status: Segundo Tiempo - 90'
Formations -> 4-2-3-1 - 4-3-3
Possession -> 64% - 36%
Shots -> 22 - 8
Yellow/Red cards -> 1/0 - 1/0

and more...

"""

import esd

client = esd.PromiedosClient()
events = client.get_events()

for event in events:
    for match in event.matches:

        # ignore matches that are not in progress
        if match.status.value != esd.promiedos.MatchStatus.IN_PROGRESS:
            continue

        print(f"League name: {event.league.name} - {event.date}")

        print(
            f"{match.home_team.name} {match.scores.home} - {match.scores.away} {match.away_team.name}"
        )
        print(f"Status: {match.status.name} - {match.time_to_display}")

        # now we get all the match detailss
        match = client.get_match(match.id)

        print(
            f"Formations -> {match.players.lineups.home_team.formation} - {match.players.lineups.away_team.formation}"
            + "\n"
            f"Possession -> {match.stats.possession.home_value} - {match.stats.possession.away_value}"
            + "\n"
            f"Shots -> {match.stats.total_shots.home_value} - {match.stats.total_shots.away_value}"
            + "\n"
            f"Yellow/Red cards -> {match.stats.yellow_cards.home_value}/{match.stats.red_cards.home_value} - {match.stats.yellow_cards.away_value}/{match.stats.red_cards.away_value}"
        )
        print("-------------------")
