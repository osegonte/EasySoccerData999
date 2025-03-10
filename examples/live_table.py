import esd


def clear_screen():
    print("\033[H\033[J")


def update_table() -> list[esd.Event]:
    client = esd.SofascoreClient()
    live_events = client.get_events(live=True)

    print("Found", len(live_events), "live events.")
    for index, event in enumerate(live_events):
        print(
            str(index).ljust(5),
            event.home_team.name.ljust(22),
            event.home_score.current,
            "vs",
            event.away_score.current,
            event.away_team.name.ljust(20),
        )
    return live_events


if __name__ == "__main__":
    client = esd.SofascoreClient()
    while True:
        clear_screen()
        events = update_table()
        choice = input(
            "Enter the index for more details (or q to quit, r to refresh): "
        )
        if choice == "q":
            break
        if choice == "r":
            continue

        try:
            index = int(choice)
            event = events[index]
            details: esd.MatchStats = client.get_match_stats(event.id)
            clear_screen()
            print(event.home_team.name, "vs", event.away_team.name)
            print("Score:", event.home_score.current, "-", event.away_score.current)
            print("Status:", event.status.description)
            print(
                "Win probability:",
                details.win_probability.home,
                "% -",
                details.win_probability.away,
                "%",
            )
            if details.all is None:
                print("No detailed information available.")
                input("Press Enter to continue...")
                continue
            print(
                "Ball possession:",
                details.all.match_overview.ball_possession.home_value,
                "% -",
                details.all.match_overview.ball_possession.away_value,
                "%",
            )
            print(
                "Shots on goal:",
                details.all.shots.shots_on_goal.home_value,
                "-",
                details.all.shots.shots_on_goal.away_value,
            )
            input("Press Enter to continue...")
        except ValueError:
            print("Invalid input.")
