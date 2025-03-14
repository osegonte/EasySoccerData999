"""
In this example, we will get all players from a match.

The output will be something like:

and more...

"""

import esd

client = esd.PromiedosClient()
events = client.get_events()


target_match = None

# let's find a match in progress
for event in events:
    for match in event.matches:
        if match.status.enum == 2:  # In progress
            target_match = match
            break

if target_match is None:
    print("No matches in progress.")
else:
    details = client.get_match(target_match.id)
    for player in details.players:
        print(player)
        print("-------------------")
