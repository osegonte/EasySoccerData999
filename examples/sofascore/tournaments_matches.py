"""
This example shows how to get tournament matches.
In this case, we get the matches of the UEFA Champions League 24/25.
If you want to get another tournament, you can use the
search method to get the tournament id and season id.
"""

from esd.sofascore import SofascoreClient

client = SofascoreClient()

uefacl_id = 7
last_season = 61644

# Get upcoming matches
events = client.get_tournament_events(uefacl_id, last_season, upcoming=True)
print("Upcoming matches")
for event in events:
    print(event.id, event.slug)

# Get last matches (page 0)
events = client.get_tournament_events(uefacl_id, last_season)
print("Last matches")
for event in events:
    print(event.id, event.slug)

# Get last last matches (page 1, ...)
events = client.get_tournament_events(uefacl_id, last_season, page=1)
print("Last last matches")
for event in events:
    print(event.id, event.slug)
