"""
This example shows how to get match shots.
In this case, we get the shots of the first PSG vs Liverpool match.

The output will be something like:
H. Elliott 0.14706888794899 0.21466222405434 left-foot 87
O. Dembélé 0.029854614287615 0.37551274895668 left-foot 84
Vitinha 0.026584554463625 0 right-foot 84
and more...
"""

from esd import SofascoreClient, SofascoreTypes

client = SofascoreClient()

match_id = 13511931  # PSG vs Liverpool (first match)
shots: list[SofascoreTypes.Shot] = client.get_match_shots(match_id)

for shot in shots:
    print(shot.player.short_name, shot.xg, shot.xg_got, shot.body_part, shot.time)