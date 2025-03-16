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

        home_team = match.teams[0]
        away_team = match.teams[1]

        print(
            f"{home_team.name} {match.scores.home} - {match.scores.away} {away_team.name}"
        )
        print(f"Status: {match.status.name} - {match.time_to_display}")

        # get the match details
        details = client.get_match(match.id)

        print(
            f"Formations -> {details.players.lineups.home_team.formation} - {details.players.lineups.away_team.formation}"
            + "\n"
            f"Possession -> {details.stats.possession.home_value} - {details.stats.possession.away_value}"
            + "\n"
            f"Shots -> {details.stats.total_shots.home_value} - {details.stats.total_shots.away_value}"
            + "\n"
            f"Yellow/Red cards -> {details.stats.yellow_cards.home_value}/{details.stats.red_cards.home_value} - {details.stats.yellow_cards.away_value}/{details.stats.red_cards.away_value}"
        )
        print("-------------------")
