"""
This example shows how to search for teams.
In this case, we search for teams that contain the word "Liverpool".

The output will be something like:

44, Liverpool, liverpool
---------------------------
66774, Liverpool FC Women, liverpool-fc-women
---------------------------
6879, Liverpool UY, liverpool-uy
---------------------------
.......
"""

import esd

client = esd.SofascoreClient()
teams: list[esd.sofascore.Team] = client.search("Liverpool", entity=esd.sofascore.EntityType.TEAM)

for team in teams:
    print(f"{team.id}, {team.name}, {team.slug}")
    print("---------------------------")
