"""
In this example, we will get all players and lineups from a match in progress.
Note, this example is using the PromiedosClient.

The output will be something like:

Audax Italiano 0 - 1 U. de Chile
Segundo Tiempo - 46'
Goals:
Di Yorio (40)
Audax Italiano formation: 4-2-3-1
Tomás Ahumada - Arquero
Esteban Matus - Defensor
Germán Guiffrey - Defensor
Enzo Ferrario - Defensor
Jorge Espejo - Defensor
Marco Collao - Mediocampista
Oliver Rojas - Defensor
Nicolás Orellana - Delantero
Leonardo Valencia - Mediocampista
Michael Fuentes - Delantero
Luis Riveros - Delantero
Substitutes:
Gonzalo Collao - Arquero
Gaston Gil Romero - Mediocampista
Paolo Guajardo - Delantero
Cristóbal Muñoz - Defensor
Lautaro Palacios - Delantero
Mario Sandoval - Mediocampista
Franco Troyansky - Delantero

U. de Chile formation: 3-5-2
Gabriel Castellón - Arquero
Matias Zaldivia - Defensor
Franco Calderón - Defensor
Nicolás Ramírez - Defensor
Matias Sepúlveda - Mediocampista
Charles Aránguiz - Mediocampista
Marcelo Diaz - Mediocampista
Israel Poblete - Mediocampista
Nicolas Fernandez - Defensor
Nicolas Guerra - Delantero
Lucas Di Yorio - Delantero
Substitutes:
Lucas Assadi - Mediocampista
Rodrigo Contreras - Delantero
Antonio Díaz - Defensor
Leandro Fernandez - Delantero
Gonzalo Montes - Mediocampista
Ignacio Tapia - Defensor
Cristopher Toselli - Arquero

"""

import esd


def find_match_in_progress() -> esd.promiedos.Match:
    client = esd.PromiedosClient()
    events = client.get_events()
    target_match = None
    for event in events:
        for match in event.matches:
            if match.status.enum == 2:  # In progress
                target_match = match
                break
    if target_match is not None:
        return client.get_match(target_match.id)
    return None


def show_lineup_and_players(team: esd.promiedos.Team, lineup: esd.promiedos.LineupTeam):
    print(f"{team.short_name} formation: {lineup.formation}")
    for player in lineup.starting:
        print(player.name, "-", player.position)
    print("Substitutes:")
    for player in lineup.bench:
        print(player.name, "-", player.position)


if __name__ == "__main__":
    match = find_match_in_progress()

    home = match.teams[0]
    away = match.teams[1]

    print(
        f"{home.short_name} {match.scores.home} - {match.scores.away} {away.short_name}"
    )
    print(f"{match.status.name} - {match.time_to_display}")

    if len(match.tv_networks) > 0:
        print("Watch on:")
        for tv in match.tv_networks:
            print(tv.name)

    goals = home.goals + away.goals
    if len(goals) > 0:
        print("Goals: ")
        for goal in goals:
            print(f"{goal.short_name} ({goal.time})")

    show_lineup_and_players(home, match.players.lineups.home_team)
    print()
    show_lineup_and_players(away, match.players.lineups.away_team)

