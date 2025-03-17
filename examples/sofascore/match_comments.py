"""
This example shows how to get match comments.

The output will be something like:

0' Match ends, Atletico Madrid 1(2), Real Madrid 0(4).
127' Penalty Shootout ends, Atletico Madrid 1(2), Real Madrid 0(4).
127' Goal! Atletico Madrid 1(2), Real Madrid 0(4). Antonio Rüdiger (Real Madrid) converts the penalty with a right footed shot to the bottom left corner.
127' Kylian Mbappé (Real Madrid) is shown the yellow card.
126' Penalty missed! Still Atletico Madrid 1(2), Real Madrid 0(3). Marcos Llorente (Atletico Madrid) hits the bar with a right footed shot.
and more...
"""

from esd.sofascore import SofascoreClient

client = SofascoreClient()

comments = client.get_match_comments(13511924)

for comment in comments:
    print(f"{comment.time}'", comment.text)
    # see esd.sofascore.Comment for more attributes
