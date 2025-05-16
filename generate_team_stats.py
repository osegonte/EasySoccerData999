"""
Simple Football Statistics Generator

This script generates placeholder statistics for teams in upcoming fixtures when
external data sources aren't accessible due to rate limiting or IP blocking.

Features:
- Works with your existing fixture data
- Creates statistical profiles based on team names
- No external API dependencies (works offline)
- Generates a comprehensive CSV with match predictions

Usage:
    python generate_team_stats.py [OPTIONS]

Options:
    --fixtures FILE      Path to fixtures CSV file (default: latest in output dir)
    --output DIR         Directory to save output files (default: 'stats_output')
    --debug              Enable debug logging
"""

import os
import csv
import sys
import hashlib
import logging
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Check for pandas
try:
    import pandas as pd
except ImportError:
    print("Required package not found: pandas")
    print("Please install required packages: pip install pandas")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class TeamStatisticsGenerator:
    """
    Generator for football team statistics based on team name seeds.
    
    This class creates consistent, pseudo-random statistics for teams
    based on their names, ensuring the same team always gets similar
    statistics across different runs.
    """
    
    def __init__(self, variance_factor: float = 0.2):
        """
        Initialize the team statistics generator.
        
        Args:
            variance_factor: How much variation to add to base statistics (0.0 to 1.0)
        """
        self.variance_factor = variance_factor
        
        # Ranges for various statistics
        self.stat_ranges = {
            'goals_scored': (0.5, 3.0),        # Average goals per match
            'goals_conceded': (0.5, 3.0),      # Average goals conceded per match
            'shots': (8.0, 20.0),              # Total shots per match
            'shots_on_target': (3.0, 8.0),     # Shots on target per match
            'possession': (30.0, 70.0),        # Possession percentage
            'pass_accuracy': (65.0, 90.0),     # Pass accuracy percentage
            'corners': (3.0, 10.0),            # Corners per match
            'yellow_cards': (1.0, 3.0),        # Yellow cards per match
            'red_cards': (0.0, 0.3),           # Red cards per match
            'fouls': (8.0, 16.0),              # Fouls committed per match
            'form_factor': (0.2, 0.8)          # Higher = better form
        }
        
        # Form options (W = win, D = draw, L = loss)
        self.form_options = ['W', 'D', 'L']
        
        # Cache for team statistics to ensure consistency
        self.team_stats_cache = {}
    
    def _get_seed_value(self, team_name: str) -> float:
        """
        Get a consistent seed value from 0.0 to 1.0 based on the team name.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Float value from 0.0 to 1.0
        """
        # Create a hash of the team name
        team_hash = hashlib.md5(team_name.lower().encode()).hexdigest()
        
        # Convert first 8 hex characters to integer and normalize to 0.0-1.0
        seed_value = int(team_hash[:8], 16) / 0xffffffff
        return seed_value
    
    def _generate_stat(self, team_name: str, stat_name: str) -> float:
        """
        Generate a statistic for a team based on its name seed.
        
        Args:
            team_name: Name of the team
            stat_name: Name of the statistic to generate
            
        Returns:
            Generated statistic value
        """
        # Get the base seed value for this team
        base_seed = self._get_seed_value(team_name)
        
        # Get additional seed from stat name to differentiate stats
        stat_seed = self._get_seed_value(stat_name)
        
        # Combine seeds to get a unique value for this team+stat
        combined_seed = (base_seed + stat_seed) / 2.0
        
        # Get the range for this statistic
        min_val, max_val = self.stat_ranges.get(stat_name, (0.0, 1.0))
        
        # Generate base value within the range
        base_value = min_val + combined_seed * (max_val - min_val)
        
        # Add some controlled randomness
        if self.variance_factor > 0:
            random.seed(f"{team_name}_{stat_name}_{datetime.now().date()}")
            variance = random.uniform(-self.variance_factor, self.variance_factor)
            adjusted_value = base_value * (1 + variance)
            # Ensure value stays within range
            return max(min_val, min(max_val, adjusted_value))
        
        return base_value
    
    def _generate_form(self, team_name: str, num_matches: int = 5) -> str:
        """
        Generate a form string (e.g., "WDLWW") for a team.
        
        Args:
            team_name: Name of the team
            num_matches: Number of matches to include in form
            
        Returns:
            Form string (W = win, D = draw, L = loss)
        """
        form_factor = self._generate_stat(team_name, 'form_factor')
        form = []
        
        # Set seed based on team name and current date for consistent form
        random.seed(f"{team_name}_form_{datetime.now().date()}")
        
        for _ in range(num_matches):
            # Adjust probabilities based on form factor (higher = better form)
            win_prob = form_factor * 0.8  # Up to 80% win probability for top teams
            draw_prob = 0.3 - (form_factor * 0.2)  # Lower for top teams
            
            # Ensure probabilities are valid
            draw_prob = max(0.1, min(0.3, draw_prob))
            
            # Select result based on probabilities
            r = random.random()
            if r < win_prob:
                form.append('W')
            elif r < win_prob + draw_prob:
                form.append('D')
            else:
                form.append('L')
        
        return ''.join(form)
    
    def generate_match_results(self, team_name: str, num_matches: int = 3) -> List[Dict[str, Any]]:
        """
        Generate recent match results for a team.
        
        Args:
            team_name: Name of the team
            num_matches: Number of matches to generate
            
        Returns:
            List of recent match dictionaries
        """
        # Common opponent templates
        opponent_templates = [
            "United", "City", "FC", "Rovers", "Athletic",
            "Wanderers", "Town", "Rangers", "Albion", "County"
        ]
        
        # Set seed based on team name for consistent opponents
        random.seed(team_name)
        
        # Generate opponent names that don't match the team name
        city_names = ["West", "North", "South", "East", "Royal", "Central", "Metropolitan"]
        
        matches = []
        for i in range(num_matches):
            # Generate a unique opponent
            while True:
                city = random.choice(city_names)
                suffix = random.choice(opponent_templates)
                opponent = f"{city} {suffix}"
                
                # Make sure opponent name doesn't match team name
                if opponent.lower() != team_name.lower():
                    break
            
            # Get match stats
            goals_scored = round(self._generate_stat(team_name, f'goals_scored_{i}'))
            goals_conceded = round(self._generate_stat(team_name, f'goals_conceded_{i}'))
            
            # Determine result (W/D/L)
            if goals_scored > goals_conceded:
                result = 'W'
            elif goals_scored < goals_conceded:
                result = 'L'
            else:
                result = 'D'
            
            # Create match dictionary
            match = {
                'date': (datetime.now().replace(day=datetime.now().day - i - 1)).strftime('%Y-%m-%d'),
                'opponent': opponent,
                'result': result,
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded,
            }
            
            matches.append(match)
        
        return matches
    
    def get_team_stats(self, team_name: str) -> Dict[str, Any]:
        """
        Get statistics for a team. Uses cached values if available.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Dictionary of team statistics
        """
        # Check cache first
        if team_name in self.team_stats_cache:
            return self.team_stats_cache[team_name]
        
        # Generate stats
        avg_stats = {
            'matches_analyzed': 7,  # Default to 7 matches analyzed
            'avg_goals_scored': round(self._generate_stat(team_name, 'goals_scored'), 2),
            'avg_goals_conceded': round(self._generate_stat(team_name, 'goals_conceded'), 2),
            'avg_shots': round(self._generate_stat(team_name, 'shots'), 2),
            'avg_shots_on_target': round(self._generate_stat(team_name, 'shots_on_target'), 2),
            'avg_possession': round(self._generate_stat(team_name, 'possession'), 2),
            'avg_pass_accuracy': round(self._generate_stat(team_name, 'pass_accuracy'), 2),
            'avg_corners': round(self._generate_stat(team_name, 'corners'), 2),
            'avg_yellow_cards': round(self._generate_stat(team_name, 'yellow_cards'), 2),
            'avg_red_cards': round(self._generate_stat(team_name, 'red_cards'), 2),
            'avg_fouls': round(self._generate_stat(team_name, 'fouls'), 2),
            'form_summary': self._generate_form(team_name),
        }
        
        # Calculate win/draw/loss percentages from form
        wins = avg_stats['form_summary'].count('W')
        draws = avg_stats['form_summary'].count('D')
        losses = avg_stats['form_summary'].count('L')
        total = len(avg_stats['form_summary'])
        
        avg_stats['win_percentage'] = round(wins * 100 / total, 2) if total > 0 else 0
        avg_stats['draw_percentage'] = round(draws * 100 / total, 2) if total > 0 else 0
        avg_stats['loss_percentage'] = round(losses * 100 / total, 2) if total > 0 else 0
        
        # Cache the stats
        self.team_stats_cache[team_name] = avg_stats
        
        return avg_stats

class FixtureStatisticsGenerator:
    """
    Generate statistics for upcoming fixtures.
    """
    
    def __init__(self, 
                 fixtures_file: Optional[str] = None, 
                 output_dir: str = 'stats_output'):
        """
        Initialize the fixture statistics generator.
        
        Args:
            fixtures_file: Path to fixtures CSV file
            output_dir: Directory to save output files
        """
        self.fixtures_file = fixtures_file
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize statistics generator
        self.stats_generator = TeamStatisticsGenerator()
        
    def find_latest_fixtures_file(self) -> Optional[str]:
        """
        Find the latest fixtures file in the sofascore_data directory.
        
        Returns:
            Path to the latest fixtures file, or None if not found
        """
        try:
            # Look for the all_matches file
            sofascore_dir = 'sofascore_data'
            if not os.path.exists(sofascore_dir):
                logger.warning(f"Directory not found: {sofascore_dir}")
                return None
            
            # Pattern: all_matches_YYYYMMDD_to_YYYYMMDD.csv
            matches_files = [f for f in os.listdir(sofascore_dir) 
                            if f.startswith('all_matches_') and f.endswith('.csv')]
            
            if not matches_files:
                logger.warning(f"No match files found in {sofascore_dir}")
                return None
            
            # Sort by date (in filename) to get the latest
            matches_files.sort(reverse=True)
            latest_file = os.path.join(sofascore_dir, matches_files[0])
            
            logger.info(f"Found latest fixtures file: {latest_file}")
            return latest_file
            
        except Exception as e:
            logger.error(f"Error finding latest fixtures file: {e}")
            return None
    
    def read_fixtures(self, fixtures_file: Optional[str] = None) -> pd.DataFrame:
        """
        Read fixtures from CSV file.
        
        Args:
            fixtures_file: Path to fixtures CSV file
            
        Returns:
            Pandas DataFrame containing fixtures
        """
        if not fixtures_file:
            fixtures_file = self.fixtures_file or self.find_latest_fixtures_file()
            
        if not fixtures_file or not os.path.exists(fixtures_file):
            raise FileNotFoundError(f"Fixtures file not found: {fixtures_file}")
        
        logger.info(f"Reading fixtures from {fixtures_file}")
        
        try:
            # Try to determine the CSV format from the file
            with open(fixtures_file, 'r', encoding='utf-8') as f:
                sample = f.read(2048)
                header = sample.split('\n')[0] if '\n' in sample else sample
            
            # Check if it's the format you provided
            if 'match_date' in header and 'kickoff_time' in header:
                # Your format
                fixtures_df = pd.read_csv(fixtures_file)
                required_columns = ['match_date', 'league', 'home_team', 'away_team']
            elif 'date' in header and 'id' in header:
                # SofaScore scraper format
                fixtures_df = pd.read_csv(fixtures_file)
                # Check if we have the necessary columns for the scraper format
                if 'home_team' in header and 'away_team' in header:
                    pass  # Good, we have what we need
                else:
                    # Try to map columns if they exist with different names
                    if 'home_team_name' in header and 'away_team_name' in header:
                        fixtures_df = fixtures_df.rename(columns={
                            'home_team_name': 'home_team',
                            'away_team_name': 'away_team'
                        })
                
                required_columns = ['date', 'home_team', 'away_team']
            else:
                # Unknown format
                logger.warning(f"Unknown CSV format, trying default pandas read")
                fixtures_df = pd.read_csv(fixtures_file)
                required_columns = []
            
            # Check if required columns exist
            missing_columns = [col for col in required_columns if col not in fixtures_df.columns]
            if missing_columns:
                raise ValueError(f"Required columns missing in fixtures file: {missing_columns}")
            
            # Standardize column names if necessary
            if 'date' in fixtures_df.columns and 'match_date' not in fixtures_df.columns:
                fixtures_df['match_date'] = fixtures_df['date']
            
            logger.info(f"Found {len(fixtures_df)} fixtures")
            return fixtures_df
            
        except Exception as e:
            logger.error(f"Error reading fixtures file: {e}")
            raise
    
    def generate_match_probability(self, home_stats: Dict[str, Any], away_stats: Dict[str, Any]) -> Dict[str, float]:
        """
        Generate match outcome probabilities based on team statistics.
        
        Args:
            home_stats: Home team statistics
            away_stats: Away team statistics
            
        Returns:
            Dictionary of outcome probabilities
        """
        # Factors that influence match outcome
        home_advantage = 1.3  # Home team advantage multiplier
        
        # Calculate team strength scores (0-100)
        home_strength = (
            home_stats['avg_goals_scored'] * 15 +
            (100 - home_stats['avg_goals_conceded'] * 15) +
            home_stats['avg_possession'] * 0.3 +
            home_stats['avg_pass_accuracy'] * 0.2 +
            home_stats['win_percentage'] * 0.5
        ) * home_advantage / 2
        
        away_strength = (
            away_stats['avg_goals_scored'] * 15 +
            (100 - away_stats['avg_goals_conceded'] * 15) +
            away_stats['avg_possession'] * 0.3 +
            away_stats['avg_pass_accuracy'] * 0.2 +
            away_stats['win_percentage'] * 0.5
        ) / 2
        
        # Normalize scores
        total_strength = home_strength + away_strength
        if total_strength > 0:
            home_normalized = home_strength / total_strength
            away_normalized = away_strength / total_strength
        else:
            home_normalized = 0.5
            away_normalized = 0.5
        
        # Calculate outcome probabilities
        home_win_prob = home_normalized * 0.8 + 0.1  # Range: 0.1-0.9
        away_win_prob = away_normalized * 0.8 + 0.1  # Range: 0.1-0.9
        
        # Adjust to ensure total probability is 1.0
        draw_prob = 1 - (home_win_prob + away_win_prob)
        
        # Handle edge cases
        if draw_prob < 0.1:
            # Reduce both win probabilities proportionally
            reduction = (0.1 - draw_prob) / 2
            home_win_prob -= reduction
            away_win_prob -= reduction
            draw_prob = 0.1
        elif draw_prob > 0.5:
            # Cap draw probability at 50%
            overflow = draw_prob - 0.5
            home_win_prob += overflow / 2
            away_win_prob += overflow / 2
            draw_prob = 0.5
        
        # Final normalization to ensure we get exactly 1.0
        total = home_win_prob + away_win_prob + draw_prob
        return {
            'home_win': round(home_win_prob / total * 100, 2),
            'draw': round(draw_prob / total * 100, 2),
            'away_win': round(away_win_prob / total * 100, 2)
        }
    
    def process_fixtures(self) -> List[Dict[str, Any]]:
        """
        Process fixtures and generate statistics for all teams.
        
        Returns:
            List of fixture statistics
        """
        fixture_stats = []
        
        try:
            # Read fixtures
            fixtures_df = self.read_fixtures()
            
            # Process each fixture
            for index, fixture in fixtures_df.iterrows():
                logger.info(f"Processing fixture: {fixture['home_team']} vs {fixture['away_team']}")
                
                # Get match details
                match_details = {
                    'fixture_id': str(index),
                    'match_date': fixture.get('match_date', fixture.get('date', '')),
                    'league': fixture.get('league', fixture.get('tournament_name', '')),
                    'home_team': fixture['home_team'],
                    'away_team': fixture['away_team'],
                    'status': fixture.get('status', 'Scheduled')
                }
                
                # Get home team stats
                home_stats = self.stats_generator.get_team_stats(fixture['home_team'])
                home_recent_matches = self.stats_generator.generate_match_results(fixture['home_team'])
                
                # Get away team stats
                away_stats = self.stats_generator.get_team_stats(fixture['away_team'])
                away_recent_matches = self.stats_generator.generate_match_results(fixture['away_team'])
                
                # Generate match probabilities
                match_probs = self.generate_match_probability(home_stats, away_stats)
                
                # Add to fixture stats
                home_fixture_stats = match_details.copy()
                home_fixture_stats.update({
                    'team_name': fixture['home_team'],
                    'opponent_name': fixture['away_team'],
                    'is_home': True,
                    'win_probability': match_probs['home_win'],
                    'draw_probability': match_probs['draw'],
                    'loss_probability': match_probs['away_win']
                })
                home_fixture_stats.update({f"home_{k}": v for k, v in home_stats.items()})
                
                away_fixture_stats = match_details.copy()
                away_fixture_stats.update({
                    'team_name': fixture['away_team'],
                    'opponent_name': fixture['home_team'],
                    'is_home': False,
                    'win_probability': match_probs['away_win'],
                    'draw_probability': match_probs['draw'],
                    'loss_probability': match_probs['home_win']
                })
                away_fixture_stats.update({f"away_{k}": v for k, v in away_stats.items()})
                
                # Add recent matches
                for i, match in enumerate(home_recent_matches[:3]):
                    prefix = f"home_recent_match_{i+1}"
                    home_fixture_stats.update({
                        f"{prefix}_date": match.get('date', ''),
                        f"{prefix}_opponent": match.get('opponent', ''),
                        f"{prefix}_result": match.get('result', ''),
                        f"{prefix}_score": f"{match.get('goals_scored', 0)}-{match.get('goals_conceded', 0)}"
                    })
                
                for i, match in enumerate(away_recent_matches[:3]):
                    prefix = f"away_recent_match_{i+1}"
                    away_fixture_stats.update({
                        f"{prefix}_date": match.get('date', ''),
                        f"{prefix}_opponent": match.get('opponent', ''),
                        f"{prefix}_result": match.get('result', ''),
                        f"{prefix}_score": f"{match.get('goals_scored', 0)}-{match.get('goals_conceded', 0)}"
                    })
                
                fixture_stats.append(home_fixture_stats)
                fixture_stats.append(away_fixture_stats)
                
        except Exception as e:
            logger.error(f"Error processing fixtures: {e}")
            import traceback
            traceback.print_exc()
        
        return fixture_stats
    
    def save_stats_to_csv(self, stats: List[Dict[str, Any]], output_file: Optional[str] = None) -> str:
        """
        Save generated statistics to a CSV file.
        
        Args:
            stats: List of statistics dictionaries
            output_file: Path to output file or None to generate automatically
            
        Returns:
            Path to the output file
        """
        if not stats:
            logger.warning("No statistics to save")
            return ""
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir, f"team_stats_{timestamp}.csv")
        
        # Get all possible fields from all stats objects
        all_fields = set()
        for stat in stats:
            all_fields.update(stat.keys())
        
        logger.info(f"Saving statistics for {len(stats)} teams to {output_file}")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(list(all_fields)))
                writer.writeheader()
                writer.writerows(stats)
            
            logger.info(f"Successfully saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error saving statistics to CSV: {e}")
            return ""
    
    def run(self) -> Optional[str]:
        """
        Run the fixture statistics generation process.
        
        Returns:
            Path to the output CSV file, or None if failed
        """
        logger.info("Starting fixture statistics generation")
        
        try:
            # Process fixtures
            fixture_stats = self.process_fixtures()
            
            if not fixture_stats:
                logger.warning("No fixture statistics generated")
                return None
            
            # Save statistics to CSV
            output_file = self.save_stats_to_csv(fixture_stats)
            
            if output_file:
                logger.info(f"Statistics generation complete! Results saved to: {output_file}")
                return output_file
            else:
                logger.error("Failed to save statistics to CSV")
                return None
                
        except Exception as e:
            logger.error(f"Error running statistics generation: {e}")
            import traceback
            traceback.print_exc()
            return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Football Statistics Generator')
    parser.add_argument('--fixtures', type=str, help='Path to fixtures CSV file')
    parser.add_argument('--output', type=str, default='stats_output', help='Output directory')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()


def main():
    """Main execution function."""
    print("=== Football Statistics Generator ===")
    print("NOTE: This tool generates placeholder statistics since external data sources aren't accessible")
    
    # Parse arguments
    args = parse_arguments()
    
    # Set logging level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Initialize generator
    generator = FixtureStatisticsGenerator(
        fixtures_file=args.fixtures,
        output_dir=args.output
    )
    
    # Run generation process
    output_file = generator.run()
    
    if output_file:
        print(f"\nProcess complete! Results saved to: {output_file}")
    else:
        print("\nProcess failed. Check the logs for details.")


if __name__ == "__main__":
    main()