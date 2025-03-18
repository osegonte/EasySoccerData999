"""
This example shows how to get the top players of a tournament.
In this case, we get the top goal scorers of the last season of the UEFA Champions League.

Example output:

1. Raphinha - 11
2. Harry Kane - 10
3. Serhou Guirassy - 10
4. Robert Lewandowski - 9
5. Erling Haaland - 8
6. Ousmane Dembélé - 7
7. Vinícius Júnior - 7
and more...

"""

from esd.sofascore import SofascoreClient

client = SofascoreClient()

uefacl_id = 7
last_season = 61644
top = client.get_tournament_top_players(uefacl_id, last_season)

for index, item in enumerate(top.goals):
    print(f"{index + 1}. {item.player.name} - {item.stat.value}")

"""
Available top attributes:
top.rating 
top.goals
top.expected_goals
top.assists
top.expected_assists
top.goals_assists_sum
top.penalty_goals
top.free_kick_goals
top.scoring_frequency
top.total_shots
top.shots_on_target
top.big_chances_missed
top.big_chances_created
top.accurate_passes
top.key_passes
top.accurate_long_balls
top.successful_dribbles
top.penalty_won
top.tackles
top.interceptions
top.clearances
top.possession_lost
top.yellow_cards 
top.red_cards
top.saves
top.goals_prevented
top.most_conceded
top.least_conceded
top.clean_sheet
"""
