"""
In this example, we will get all match events for a specific match.
The match ID is "ediedag" that corresponds to the match "Liverpool vs PSG".

The output will be something like:

Liverpool 0 - 1 PSG
Por penales - 124.0'

First Half:
EventItem(time="12'", is_home=False, details='Ousmane Dembélé', event_type=<EventType.GOAL: 1>)
...

Second Half:
EventItem(time="46'", is_home=False, details='Marquinhos', event_type=<EventType.YELLOW_CARD: 4>)
...

Extra Time:
EventItem(time="101'", is_home=False, details=Substitution(player_in='Lee Kang-in', player_out='Khvicha Kvaratskhelia'), event_type=<EventType.SUBSTITUTION: 15>)
....

Penalties:
EventItem(time='1', is_home=True, details='Mohamed Salah', event_type=<EventType.PENALTY_SCORED: 3>)
EventItem(time='1', is_home=False, details='Vitinha', event_type=<EventType.PENALTY_SCORED: 3>)
....

"""

import esd

client = esd.PromiedosClient()

match = client.get_match("ediedag")

print(
    f"{match.home_team.short_name} {match.scores.home} - {match.scores.away} {match.away_team.short_name}"
)
print(f"{match.status.name} - {match.current_time}'")

print("First Half:")
for event in match.events.first_half:
    print(event)

print("Second Half:")
for event in match.events.second_half:
    print(event)

print("Extra Time:")
for event in match.events.extra_time:
    print(event)

print("Penalties:")
for event in match.events.penalties:
    print(event)
