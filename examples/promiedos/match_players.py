"""
In this example, we will get all players and lineups from a match in progress.
Note, this example is using the PromiedosClient.

The output will be something like:

Real Madrid 2 - 1 Atlético
Finalizado -
Goals:
Rodrygo (4)
Diaz (55)
Álvarez (32)
Real Madrid formation: 4-4-2
Thibaut Courtois - Arquero
Ferland Mendy - Defensor
Antonio Rüdiger - Defensor
Raúl Asencio - Defensor
Federico Valverde - Mediocampista
Brahim Diaz - Mediocampista
Eduardo Camavinga - Mediocampista
Aurélien Tchouaméni - Mediocampista
Rodrygo - Delantero
Vinicius Júnior - Delantero
Kylian Mbappe - Delantero
Substitutes:
Luka Modric - Mediocampista
Endrick - Delantero
Lucas Vázquez - Defensor
Francisco Garcia - Defensor
Fran González - Arquero
Arda Güler - Delantero
Andriy Lunin - Arquero
David Alaba - Defensor

Atlético formation: 4-4-2
Jan Oblak - Arquero
Javier Galán - Defensor
Clément Lenglet - Defensor
José María Giménez - Defensor
Marcos Llorente - Mediocampista
Samuel Lino - Delantero
Pablo Barrios - Mediocampista
Rodrigo De Paul - Mediocampista
Giuliano Simeone - Delantero
Antoine Griezmann - Delantero
Julián Álvarez - Delantero
Substitutes:
Angel Correa - Delantero
Conor Gallagher - Mediocampista
Robin Le Normand - Defensor
Nahuel Molina - Defensor
Alexander Sorloth - Delantero
Antonio Gomís - Arquero
Reinildo Mandava - Defensor
Axel Witsel - Mediocampista
Thomas Lemar - Mediocampista
Juan Musso - Arquero
Rodrigo Riquelme - Delantero

"""

import esd


def show_lineup_and_players(team: esd.promiedos.Team, lineup: esd.promiedos.LineupTeam):
    print(f"{team.short_name} formation: {lineup.formation}")
    for player in lineup.starting:
        print(player.name, "-", player.position)
    print("Substitutes:")
    for player in lineup.bench:
        print(player.name, "-", player.position)


if __name__ == "__main__":

    client = esd.PromiedosClient()
    match = client.get_match("ediecjh")

    home = match.home_team
    away = match.away_team

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
