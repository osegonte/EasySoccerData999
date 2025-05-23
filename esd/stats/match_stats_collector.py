from esd import SofascoreClient
import pandas as pd
import os
import time
import csv
from datetime import datetime

class TeamStatsCollector:
    def __init__(self, data_dir="match_stats"):
        """Initialize the stats collector with SofaScore client"""
        self.client = SofascoreClient()
        self.data_dir = data_dir
        
        # Create directory for saving data if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def read_upcoming_fixtures(self, fixtures_path):
        """Read upcoming fixtures from CSV file generated by the scraper"""
        return pd.read_csv(fixtures_path)
    
    def get_team_recent_matches(self, team_id, limit=7):
        """Get a team's recent matches (up to a limit)"""
        matches = self.client.get_team_events(team_id, upcoming=False, page=0)
        return matches[:limit] if len(matches) > limit else matches
    
    def get_match_statistics(self, match_id, team_id):
        """Get statistics for a specific match for a specific team"""
        match_stats = self.client.get_match_stats(match_id)
        
        # Determine if the team is home or away
        match = self.client.get_event(match_id)
        is_home = match.home_team.id == team_id
        
        # Extract the relevant statistics
        stats = self._extract_team_stats(match_stats, is_home)
        return stats
    
    def _extract_team_stats(self, match_stats, is_home):
        """Extract the specified statistics for a team"""
        # Get the key that corresponds to the team we want
        key_prefix = "home" if is_home else "away"
        
        stats = {}
        
        # Extract the statistics we want
        if match_stats.all is not None:
            # Goals scored/conceded
            stats['goals_scored'] = getattr(match_stats.all.match_overview.expected_goals, f"{key_prefix}_value", 0)
            stats['goals_conceded'] = getattr(match_stats.all.match_overview.expected_goals, 
                                             f"{'away' if is_home else 'home'}_value", 0)
            
            # Shots
            stats['shots_on_target'] = getattr(match_stats.all.shots.shots_on_goal, f"{key_prefix}_value", 0)
            stats['total_shots'] = getattr(match_stats.all.shots.total_shots_on_goal, f"{key_prefix}_value", 0)
            
            # Possession
            stats['possession'] = getattr(match_stats.all.match_overview.ball_possession, f"{key_prefix}_value", 0)
            
            # Pass accuracy
            accurate_passes = getattr(match_stats.all.passes.accurate_passes, f"{key_prefix}_value", 0)
            total_passes = getattr(match_stats.all.match_overview.passes, f"{key_prefix}_value", 0)
            stats['pass_accuracy'] = (accurate_passes / total_passes * 100) if total_passes > 0 else 0
            
            # Corners
            stats['corners'] = getattr(match_stats.all.match_overview.corner_kicks, f"{key_prefix}_value", 0)
            
            # Cards
            stats['yellow_cards'] = getattr(match_stats.all.match_overview.yellow_cards, f"{key_prefix}_value", 0)
            stats['red_cards'] = 0  # Need to check if this is available in match_stats
            
            # Fouls
            stats['fouls'] = getattr(match_stats.all.match_overview.fouls, f"{key_prefix}_value", 0)
        
        return stats
    
    def collect_stats_for_teams(self, fixtures_df):
        """Collect statistics for all teams in upcoming fixtures"""
        all_team_stats = []
        
        # Process each fixture
        for idx, fixture in fixtures_df.iterrows():
            print(f"Processing fixture: {fixture['home_team']} vs {fixture['away_team']}")
            
            # Process home team
            home_team_stats = self._process_team(fixture['home_team'], fixture['id'], is_home=True)
            if home_team_stats:
                home_team_stats['fixture_id'] = fixture['id']
                home_team_stats['fixture_date'] = fixture.get('date', 'Unknown')
                home_team_stats['team_name'] = fixture['home_team']
                home_team_stats['opponent_name'] = fixture['away_team']
                home_team_stats['is_home'] = True
                all_team_stats.append(home_team_stats)
            
            # Process away team
            away_team_stats = self._process_team(fixture['away_team'], fixture['id'], is_home=False)
            if away_team_stats:
                away_team_stats['fixture_id'] = fixture['id']
                away_team_stats['fixture_date'] = fixture.get('date', 'Unknown')
                away_team_stats['team_name'] = fixture['away_team']
                away_team_stats['opponent_name'] = fixture['home_team']
                away_team_stats['is_home'] = False
                all_team_stats.append(away_team_stats)
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        return all_team_stats
    
    def _process_team(self, team_name, fixture_id, is_home):
        """Process statistics for a single team"""
        try:
            # Search for the team
            teams = self.client.search(team_name, entity="teams")
            if not teams:
                print(f"No team found for name: {team_name}")
                return None
            
            team = teams[0]  # Take the first result
            team_id = team.id
            print(f"Found team: {team.name} (ID: {team_id})")
            
            # Get recent matches
            recent_matches = self.get_team_recent_matches(team_id)
            if not recent_matches:
                print(f"No recent matches found for team: {team_name}")
                return None
            
            print(f"Found {len(recent_matches)} recent matches for {team_name}")
            
            # Calculate average statistics
            stats_sum = {
                'goals_scored': 0,
                'goals_conceded': 0,
                'shots_on_target': 0,
                'total_shots': 0,
                'possession': 0,
                'pass_accuracy': 0,
                'corners': 0,
                'yellow_cards': 0,
                'red_cards': 0,
                'fouls': 0,
                'matches_analyzed': 0
            }
            
            # Process each match
            for match in recent_matches:
                try:
                    match_stats = self.get_match_statistics(match.id, team_id)
                    
                    # Add to running totals
                    for key, value in match_stats.items():
                        if key in stats_sum:
                            stats_sum[key] += value
                    
                    stats_sum['matches_analyzed'] += 1
                    
                except Exception as e:
                    print(f"Error processing match {match.id}: {str(e)}")
                    continue
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            
            # Calculate averages
            avg_stats = {}
            if stats_sum['matches_analyzed'] > 0:
                for key, value in stats_sum.items():
                    if key != 'matches_analyzed':
                        avg_stats[f'avg_{key}'] = value / stats_sum['matches_analyzed']
                
                avg_stats['matches_analyzed'] = stats_sum['matches_analyzed']
                return avg_stats
            else:
                print(f"No valid matches analyzed for team: {team_name}")
                return None
            
        except Exception as e:
            print(f"Error processing team {team_name}: {str(e)}")
            return None
    
    def save_stats_to_csv(self, stats, output_file=None):
        """Save collected statistics to a CSV file"""
        if not stats:
            print("No statistics to save")
            return
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.data_dir, f"team_stats_{timestamp}.csv")
        
        # Get all possible fields from all stats objects
        all_fields = set()
        for stat in stats:
            all_fields.update(stat.keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(list(all_fields)))
            writer.writeheader()
            writer.writerows(stats)
        
        print(f"Saved statistics for {len(stats)} teams to {output_file}")
    
    def run(self, fixtures_path):
        """Main method to run the statistics collection process"""
        print(f"Reading fixtures from {fixtures_path}")
        fixtures_df = self.read_upcoming_fixtures(fixtures_path)
        
        print(f"Found {len(fixtures_df)} upcoming fixtures")
        team_stats = self.collect_stats_for_teams(fixtures_df)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.data_dir, f"team_stats_{timestamp}.csv")
        self.save_stats_to_csv(team_stats, output_file)
        
        return output_file