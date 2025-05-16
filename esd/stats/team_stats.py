"""
Team statistics collector module for EasySoccerData.
"""

from __future__ import annotations
import os
import time
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

from ..sofascore import SofascoreClient
from ..sofascore.types import Event, Team


class TeamStatsCollector:
    """
    Collects and analyzes statistics for teams in upcoming fixtures.
    
    This class retrieves recent match statistics for teams and calculates
    averages for key performance metrics.
    """

    def __init__(self, data_dir: str = "match_stats") -> None:
        """
        Initialize the statistics collector.
        
        Args:
            data_dir (str): Directory to save output files
        """
        self.client = SofascoreClient()
        self.data_dir = data_dir
        
        # Create directory for saving data if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def read_upcoming_fixtures(self, fixtures_path: str) -> pd.DataFrame:
        """
        Read upcoming fixtures from CSV file.
        
        Args:
            fixtures_path (str): Path to the CSV file with fixtures
            
        Returns:
            pd.DataFrame: DataFrame containing the fixtures
        """
        return pd.read_csv(fixtures_path)
    
    def get_team_recent_matches(self, team_id: int, limit: int = 7) -> List[Event]:
        """
        Get a team's recent matches.
        
        Args:
            team_id (int): SofaScore team ID
            limit (int): Maximum number of matches to retrieve
            
        Returns:
            List[Event]: List of recent match events
        """
        matches = self.client.get_team_events(team_id, upcoming=False, page=0)
        return matches[:limit] if len(matches) > limit else matches
    
    def get_match_statistics(self, match_id: int, team_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specific match for a specific team.
        
        Args:
            match_id (int): SofaScore match ID
            team_id (int): SofaScore team ID
            
        Returns:
            Dict[str, Any]: Dictionary of statistics for the team
        """
        match_stats = self.client.get_match_stats(match_id)
        
        # Determine if the team is home or away
        match = self.client.get_event(match_id)
        is_home = match.home_team.id == team_id
        
        # Extract the relevant statistics
        stats = self._extract_team_stats(match_stats, is_home, match)
        
        # Add match details
        stats['match_id'] = match_id
        stats['match_date'] = datetime.fromtimestamp(match.start_timestamp).strftime('%Y-%m-%d')
        stats['opponent'] = match.away_team.name if is_home else match.home_team.name
        stats['opponent_id'] = match.away_team.id if is_home else match.home_team.id
        stats['tournament'] = match.tournament.name
        
        return stats
    
    def _extract_team_stats(self, match_stats, is_home: bool, match: Event) -> Dict[str, float]:
        """
        Extract the specified statistics for a team.
        
        Args:
            match_stats: Match statistics object
            is_home (bool): Whether the team is the home team
            match (Event): Match event object
            
        Returns:
            Dict[str, float]: Dictionary of extracted statistics
        """
        # Get the key that corresponds to the team we want
        key_prefix = "home" if is_home else "away"
        
        # Initialize stats dictionary with zeros
        stats = {
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
            'expected_goals': 0,
            'big_chances_created': 0,
            'goalkeeper_saves': 0,
        }
        
        # Get actual scores from the match
        if is_home:
            stats['goals_scored'] = match.home_score.current
            stats['goals_conceded'] = match.away_score.current
        else:
            stats['goals_scored'] = match.away_score.current
            stats['goals_conceded'] = match.home_score.current
        
        # Extract the statistics if available
        if match_stats.all is not None:
            # Expected goals
            stats['expected_goals'] = getattr(match_stats.all.match_overview.expected_goals, f"{key_prefix}_value", 0)
            
            # Shots
            stats['shots_on_target'] = getattr(match_stats.all.shots.shots_on_goal, f"{key_prefix}_value", 0)
            stats['total_shots'] = getattr(match_stats.all.shots.total_shots_on_goal, f"{key_prefix}_value", 0)
            
            # Possession
            stats['possession'] = getattr(match_stats.all.match_overview.ball_possession, f"{key_prefix}_value", 0)
            
            # Pass accuracy
            if match_stats.all.passes:
                passes_total = getattr(match_stats.all.match_overview.passes, f"{key_prefix}_value", 0)
                passes_accurate = getattr(match_stats.all.passes.accurate_passes, f"{key_prefix}_value", 0)
                
                if passes_total > 0:
                    stats['pass_accuracy'] = (passes_accurate / passes_total) * 100
            
            # Corners
            stats['corners'] = getattr(match_stats.all.match_overview.corner_kicks, f"{key_prefix}_value", 0)
            
            # Cards
            stats['yellow_cards'] = getattr(match_stats.all.match_overview.yellow_cards, f"{key_prefix}_value", 0)
            
            # Fouls
            stats['fouls'] = getattr(match_stats.all.match_overview.fouls, f"{key_prefix}_value", 0)
            
            # Big chances
            stats['big_chances_created'] = getattr(match_stats.all.match_overview.big_chance_created, f"{key_prefix}_value", 0)
            
            # Goalkeeper saves
            stats['goalkeeper_saves'] = getattr(match_stats.all.match_overview.goalkeeper_saves, f"{key_prefix}_value", 0)
        
        return stats
    
    def collect_stats_for_teams(self, fixtures_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Collect statistics for all teams in upcoming fixtures.
        
        Args:
            fixtures_df (pd.DataFrame): DataFrame containing upcoming fixtures
            
        Returns:
            List[Dict[str, Any]]: List of team statistics dictionaries
        """
        all_team_stats = []
        
        # Process each fixture
        for idx, fixture in fixtures_df.iterrows():
            print(f"Processing fixture: {fixture['home_team']} vs {fixture['away_team']}")
            
            # Process home team
            home_team_stats = self._process_team(fixture['home_team'], fixture, is_home=True)
            if home_team_stats:
                home_team_stats['fixture_id'] = fixture.get('id', f"fixture_{idx}")
                home_team_stats['fixture_date'] = fixture.get('date', 'Unknown')
                home_team_stats['team_name'] = fixture['home_team']
                home_team_stats['opponent_name'] = fixture['away_team']
                home_team_stats['is_home'] = True
                all_team_stats.append(home_team_stats)
            
            # Process away team
            away_team_stats = self._process_team(fixture['away_team'], fixture, is_home=False)
            if away_team_stats:
                away_team_stats['fixture_id'] = fixture.get('id', f"fixture_{idx}")
                away_team_stats['fixture_date'] = fixture.get('date', 'Unknown')
                away_team_stats['team_name'] = fixture['away_team']
                away_team_stats['opponent_name'] = fixture['home_team']
                away_team_stats['is_home'] = False
                all_team_stats.append(away_team_stats)
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        return all_team_stats
    
    def _process_team(self, team_name: str, fixture: pd.Series, is_home: bool) -> Optional[Dict[str, Any]]:
        """
        Process statistics for a single team.
        
        Args:
            team_name (str): Name of the team
            fixture (pd.Series): Fixture row
            is_home (bool): Whether the team is the home team
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary of team statistics or None if an error occurred
        """
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
            recent_matches = self.get_team_recent_matches(team_id, limit=7)  # Get last 7 matches
            if not recent_matches:
                print(f"No recent matches found for team: {team_name}")
                return None
            
            print(f"Found {len(recent_matches)} recent matches for {team_name}")
            
            # Calculate average statistics
            all_stats = []
            
            # Process each match
            for match in recent_matches:
                try:
                    match_stats = self.get_match_statistics(match.id, team_id)
                    all_stats.append(match_stats)
                    print(f"  Processed match {match.id}: {match_stats['match_date']} vs {match_stats['opponent']}")
                    
                except Exception as e:
                    print(f"Error processing match {match.id}: {str(e)}")
                    continue
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            
            # Calculate averages from all collected match stats
            avg_stats = self._calculate_average_stats(all_stats)
            avg_stats['matches_analyzed'] = len(all_stats)
            
            # Add form metrics (wins, draws, losses in last matches)
            form_stats = self._calculate_form_stats(all_stats)
            avg_stats.update(form_stats)
            
            # Add recent match details
            for i, match_stat in enumerate(all_stats[:5]):  # Include up to 5 recent matches
                prefix = f"recent_match_{i+1}"
                avg_stats[f"{prefix}_date"] = match_stat['match_date']
                avg_stats[f"{prefix}_opponent"] = match_stat['opponent']
                avg_stats[f"{prefix}_goals_scored"] = match_stat['goals_scored']
                avg_stats[f"{prefix}_goals_conceded"] = match_stat['goals_conceded']
                avg_stats[f"{prefix}_tournament"] = match_stat['tournament']
            
            return avg_stats
            
        except Exception as e:
            print(f"Error processing team {team_name}: {str(e)}")
            return None
    
    def _calculate_form_stats(self, all_stats: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate form statistics (wins, draws, losses).
        
        Args:
            all_stats (List[Dict[str, Any]]): List of match statistics
            
        Returns:
            Dict[str, int]: Form statistics
        """
        if not all_stats:
            return {'wins': 0, 'draws': 0, 'losses': 0}
        
        wins = draws = losses = 0
        
        for match in all_stats:
            goals_scored = match['goals_scored']
            goals_conceded = match['goals_conceded']
            
            if goals_scored > goals_conceded:
                wins += 1
            elif goals_scored == goals_conceded:
                draws += 1
            else:
                losses += 1
        
        return {
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'points': wins * 3 + draws
        }
    
    def _calculate_average_stats(self, all_stats: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate average statistics from a list of match statistics.
        
        Args:
            all_stats (List[Dict[str, Any]]): List of match statistics
            
        Returns:
            Dict[str, float]: Dictionary of average statistics
        """
        if not all_stats:
            return {}
        
        # Define which stats to average
        stats_to_avg = [
            'goals_scored',
            'goals_conceded',
            'shots_on_target',
            'total_shots',
            'possession',
            'pass_accuracy',
            'corners',
            'yellow_cards',
            'red_cards',
            'fouls',
            'expected_goals',
            'big_chances_created',
            'goalkeeper_saves'
        ]
        
        avg_stats = {}
        matches_count = len(all_stats)
        
        for stat in stats_to_avg:
            # Sum up the values
            total = sum(match.get(stat, 0) for match in all_stats)
            # Calculate the average
            avg_stats[f'avg_{stat}'] = total / matches_count if matches_count > 0 else 0
        
        # Add derived statistics
        avg_stats['avg_goal_diff'] = avg_stats['avg_goals_scored'] - avg_stats['avg_goals_conceded']
        avg_stats['avg_shots_conversion'] = (avg_stats['avg_goals_scored'] / avg_stats['avg_total_shots'] * 100) if avg_stats['avg_total_shots'] > 0 else 0
        
        return avg_stats
    
    def save_stats_to_csv(self, stats: List[Dict[str, Any]], output_file: Optional[str] = None) -> str:
        """
        Save collected statistics to a CSV file.
        
        Args:
            stats (List[Dict[str, Any]]): List of team statistics dictionaries
            output_file (Optional[str]): Path to output file or None to generate automatically
            
        Returns:
            str: Path to the output file
        """
        if not stats:
            print("No statistics to save")
            return ""
        
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
        return output_file
    
    def run(self, fixtures_path: str) -> str:
        """
        Main method to run the statistics collection process.
        
        Args:
            fixtures_path (str): Path to the CSV file with fixtures
            
        Returns:
            str: Path to the output CSV file
        """
        print(f"Reading fixtures from {fixtures_path}")
        fixtures_df = self.read_upcoming_fixtures(fixtures_path)
        
        print(f"Found {len(fixtures_df)} upcoming fixtures")
        team_stats = self.collect_stats_for_teams(fixtures_df)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.data_dir, f"team_stats_{timestamp}.csv")
        self.save_stats_to_csv(team_stats, output_file)
        
        return output_file