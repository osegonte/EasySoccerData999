"""
FBref Statistics Collector

A standalone tool to collect team statistics from FBref for upcoming fixtures.

This script:
1. Reads upcoming fixtures from a CSV file
2. Uses FBref to collect statistics for each team's recent matches
3. Outputs a CSV with team statistics for analysis

Statistics collected:
- Goals scored
- Goals conceded
- Shots on target
- Total shots
- Possession
- Pass accuracy
- Corners
- Yellow cards
- Red cards
- Fouls committed

Usage:
    python fbref_stats_collector.py [OPTIONS]

Options:
    --fixtures FILE      Path to fixtures CSV file (default: latest in output dir)
    --output DIR         Directory to save output files (default: 'stats_output')
    --matches N          Number of recent matches to analyze (default: 7)
    --debug              Enable debug logging
"""

import os
import csv
import sys
import time
import random
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union

# Import FBref client from esd if available
try:
    from esd.fbref import FBrefClient
    USE_ESD_CLIENT = True
except ImportError:
    USE_ESD_CLIENT = False
    print("EasySoccerData package not found. Using built-in FBref scraper.")

# Import required packages
try:
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import lxml
except ImportError as e:
    print(f"Required package not found: {e}")
    print("Please install required packages: pip install pandas requests beautifulsoup4 lxml")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class FBrefStatsFetcher:
    """A class to fetch and process team statistics from FBref."""
    
    def __init__(self, max_matches: int = 7, delay_range: Tuple[float, float] = (1.0, 3.0)):
        """
        Initialize the FBref statistics fetcher.
        
        Args:
            max_matches: Maximum number of recent matches to analyze
            delay_range: Range of delay between requests (min, max) in seconds
        """
        self.max_matches = max_matches
        self.delay_min, self.delay_max = delay_range
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://fbref.com/'
        })
        
        # If EasySoccerData is available, use its client
        if USE_ESD_CLIENT:
            self.fbref_client = FBrefClient()
        
        # Cache for team URLs to avoid duplicated searches
        self.team_url_cache = {}
        
    def random_delay(self) -> None:
        """Add a random delay to avoid rate limiting."""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _clean_team_name(self, team_name: str) -> str:
        """Clean team name for better search results."""
        return team_name.strip().lower().replace("fc", "").replace("  ", " ").strip()
    
    def search_team(self, team_name: str) -> Optional[str]:
        """
        Search for a team on FBref and return the team URL.
        
        Args:
            team_name: Name of the team to search for
            
        Returns:
            URL to the team page if found, None otherwise
        """
        # Check cache first
        clean_name = self._clean_team_name(team_name)
        if clean_name in self.team_url_cache:
            return self.team_url_cache[clean_name]
        
        logger.info(f"Searching for team: {team_name}")
        
        try:
            # Try to find the team directly if using ESD client
            if USE_ESD_CLIENT:
                try:
                    # Use the client to get matches which should list team names
                    matches = self.fbref_client.get_matchs()
                    # Look for the team in home or away teams
                    for match in matches:
                        home_team_clean = self._clean_team_name(match.home_team)
                        away_team_clean = self._clean_team_name(match.away_team)
                        
                        if clean_name in home_team_clean:
                            # If we find a match, construct the URL based on the match ID
                            if match.id and "/matches/" in match.id:
                                parts = match.id.split("/")
                                team_id_idx = parts.index("matches") - 1
                                if team_id_idx >= 0:
                                    team_url = f"https://fbref.com/en/squads/{parts[team_id_idx]}/all_comps/Match-Logs-All-Competitions"
                                    self.team_url_cache[clean_name] = team_url
                                    return team_url
                        
                        if clean_name in away_team_clean:
                            if match.id and "/matches/" in match.id:
                                parts = match.id.split("/")
                                team_id_idx = parts.index("matches") - 1
                                if team_id_idx >= 0:
                                    team_url = f"https://fbref.com/en/squads/{parts[team_id_idx]}/all_comps/Match-Logs-All-Competitions"
                                    self.team_url_cache[clean_name] = team_url
                                    return team_url
                except Exception as e:
                    logger.warning(f"Error searching team with ESD client: {e}")
            
            # Fallback to direct search on FBref
            search_url = f"https://fbref.com/en/search/search.fcgi?search={team_name.replace(' ', '+')}"
            
            self.random_delay()
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Look for search results with the team name
            search_results = soup.select('.search-item-name')
            team_urls = []
            
            for result in search_results:
                result_text = result.get_text().lower()
                link = result.find('a')
                
                if not link:
                    continue
                
                href = link.get('href')
                if not href:
                    continue
                
                # Check if this is likely a team (contains "/squads/")
                if "/squads/" in href and clean_name in self._clean_team_name(result_text):
                    team_url = f"https://fbref.com{href}"
                    team_urls.append(team_url)
            
            if team_urls:
                # Choose the first match
                team_url = team_urls[0]
                
                # Modify URL to get match logs for all competitions
                if "/squads/" in team_url:
                    team_id = team_url.split("/squads/")[1].split("/")[0]
                    stats_url = f"https://fbref.com/en/squads/{team_id}/all_comps/Match-Logs-All-Competitions"
                    self.team_url_cache[clean_name] = stats_url
                    return stats_url
            
            logger.warning(f"Team not found: {team_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error searching for team {team_name}: {e}")
            return None

    def parse_match_stats(self, row_element, is_won: bool = None) -> Dict[str, Any]:
        """
        Parse a match row from FBref and extract statistics.
        
        Args:
            row_element: HTML row element containing match data
            is_won: Override to indicate if the match was won
            
        Returns:
            Dictionary of match statistics
        """
        match_stats = {
            'date': '',
            'opponent': '',
            'result': '',
            'goals_scored': 0,
            'goals_conceded': 0,
            'shots': 0,
            'shots_on_target': 0,
            'possession': 0.0,
            'pass_accuracy': 0.0,
            'corners': 0,
            'yellow_cards': 0,
            'red_cards': 0,
            'fouls': 0
        }
        
        try:
            # Get all cells in the row
            cells = row_element.find_all(['th', 'td'])
            
            # Extract basic match information
            if len(cells) > 9:
                match_stats['date'] = cells[0].get_text().strip()
                
                # Determine opponent (home or away)
                venue_cell = cells[3].get_text().strip()
                if venue_cell == 'Home':
                    match_stats['opponent'] = cells[5].get_text().strip()
                else:
                    match_stats['opponent'] = cells[4].get_text().strip()
                
                # Get match result
                score_text = cells[6].get_text().strip()
                if ':' in score_text:
                    score_parts = score_text.split(':')
                    if len(score_parts) == 2:
                        # If home match, first number is goals scored
                        if venue_cell == 'Home':
                            match_stats['goals_scored'] = int(score_parts[0].strip())
                            match_stats['goals_conceded'] = int(score_parts[1].strip())
                        else:
                            match_stats['goals_scored'] = int(score_parts[1].strip())
                            match_stats['goals_conceded'] = int(score_parts[0].strip())
                
                # Determine result (W/L/D)
                result_cell = cells[7].get_text().strip()
                match_stats['result'] = result_cell
                
                # Extract detailed statistics if available
                stats_start_idx = 8
                if len(cells) > stats_start_idx:
                    # The indexes might vary depending on the FBref table structure
                    try:
                        # Try to extract stats from different possible columns
                        for i, cell in enumerate(cells[stats_start_idx:]):
                            stat_text = cell.get_text().strip()
                            stat_name = cell.get('data-stat', '').lower()
                            
                            if stat_name == 'shots' or 'sh' in stat_name:
                                match_stats['shots'] = int(stat_text) if stat_text.isdigit() else 0
                            elif stat_name == 'shots_on_target' or 'sot' in stat_name:
                                match_stats['shots_on_target'] = int(stat_text) if stat_text.isdigit() else 0
                            elif stat_name == 'possession' or 'poss' in stat_name:
                                if '%' in stat_text:
                                    stat_text = stat_text.replace('%', '')
                                try:
                                    match_stats['possession'] = float(stat_text)
                                except ValueError:
                                    pass
                            elif stat_name == 'passes_pct' or 'pass_acc' in stat_name:
                                if '%' in stat_text:
                                    stat_text = stat_text.replace('%', '')
                                try:
                                    match_stats['pass_accuracy'] = float(stat_text)
                                except ValueError:
                                    pass
                            elif stat_name == 'corners' or 'ck' in stat_name:
                                match_stats['corners'] = int(stat_text) if stat_text.isdigit() else 0
                            elif stat_name == 'cards_yellow' or 'yel' in stat_name:
                                match_stats['yellow_cards'] = int(stat_text) if stat_text.isdigit() else 0
                            elif stat_name == 'cards_red' or 'red' in stat_name:
                                match_stats['red_cards'] = int(stat_text) if stat_text.isdigit() else 0
                            elif stat_name == 'fouls' or 'fls' in stat_name:
                                match_stats['fouls'] = int(stat_text) if stat_text.isdigit() else 0
                    except Exception as e:
                        logger.debug(f"Error extracting detailed stats: {e}")
        
        except Exception as e:
            logger.error(f"Error parsing match row: {e}")
        
        return match_stats

    def get_team_recent_matches(self, team_name: str) -> List[Dict[str, Any]]:
        """
        Get recent match statistics for a team.
        
        Args:
            team_name: Name of the team
            
        Returns:
            List of match statistics dictionaries
        """
        matches = []
        
        # Try to find the team
        team_url = self.search_team(team_name)
        if not team_url:
            logger.warning(f"Could not find team URL for {team_name}")
            return matches
        
        try:
            logger.info(f"Fetching match stats for {team_name}")
            
            # Get team match logs
            self.random_delay()
            response = self.session.get(team_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find the match log table
            match_table = soup.select_one('table.stats_table')
            if not match_table:
                logger.warning(f"No match table found for {team_name}")
                return matches
            
            # Get all match rows (skip header row)
            match_rows = match_table.select('tbody tr')
            
            # Process only the most recent matches up to max_matches
            count = 0
            for row in match_rows:
                # Skip empty or header rows
                if 'spacer' in row.get('class', []) or 'thead' in row.get('class', []):
                    continue
                    
                # Skip matches without scores (future matches)
                score_cell = row.select_one('td[data-stat="score"]')
                if not score_cell or not score_cell.get_text().strip():
                    continue
                
                # Parse match statistics
                match_stats = self.parse_match_stats(row)
                if match_stats.get('date'):  # Only add if we got valid data
                    matches.append(match_stats)
                    count += 1
                
                # Stop after reaching max_matches
                if count >= self.max_matches:
                    break
            
            logger.info(f"Found {len(matches)} recent matches for {team_name}")
            
        except Exception as e:
            logger.error(f"Error getting recent matches for {team_name}: {e}")
        
        return matches
    
    def calculate_team_averages(self, recent_matches: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate average statistics from recent matches.
        
        Args:
            recent_matches: List of match statistics
            
        Returns:
            Dictionary of average statistics
        """
        if not recent_matches:
            return {
                'matches_analyzed': 0,
                'avg_goals_scored': 0.0,
                'avg_goals_conceded': 0.0,
                'avg_shots': 0.0,
                'avg_shots_on_target': 0.0,
                'avg_possession': 0.0,
                'avg_pass_accuracy': 0.0,
                'avg_corners': 0.0,
                'avg_yellow_cards': 0.0,
                'avg_red_cards': 0.0,
                'avg_fouls': 0.0,
                'win_percentage': 0.0,
                'draw_percentage': 0.0,
                'loss_percentage': 0.0,
                'form_summary': ''
            }
        
        # Initialize counters
        stats_sum = {
            'goals_scored': 0,
            'goals_conceded': 0,
            'shots': 0,
            'shots_on_target': 0,
            'possession': 0.0,
            'pass_accuracy': 0.0,
            'corners': 0,
            'yellow_cards': 0,
            'red_cards': 0,
            'fouls': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0
        }
        
        # Sum up all statistics
        for match in recent_matches:
            stats_sum['goals_scored'] += match['goals_scored']
            stats_sum['goals_conceded'] += match['goals_conceded']
            stats_sum['shots'] += match['shots']
            stats_sum['shots_on_target'] += match['shots_on_target']
            stats_sum['possession'] += match['possession']
            stats_sum['pass_accuracy'] += match['pass_accuracy']
            stats_sum['corners'] += match['corners']
            stats_sum['yellow_cards'] += match['yellow_cards']
            stats_sum['red_cards'] += match['red_cards']
            stats_sum['fouls'] += match['fouls']
            
            # Count results
            if match['result'] == 'W':
                stats_sum['wins'] += 1
            elif match['result'] == 'D':
                stats_sum['draws'] += 1
            elif match['result'] == 'L':
                stats_sum['losses'] += 1
        
        # Calculate averages
        num_matches = len(recent_matches)
        avg_stats = {
            'matches_analyzed': num_matches,
            'avg_goals_scored': round(stats_sum['goals_scored'] / num_matches, 2),
            'avg_goals_conceded': round(stats_sum['goals_conceded'] / num_matches, 2),
            'avg_shots': round(stats_sum['shots'] / num_matches, 2),
            'avg_shots_on_target': round(stats_sum['shots_on_target'] / num_matches, 2),
            'avg_possession': round(stats_sum['possession'] / num_matches, 2),
            'avg_pass_accuracy': round(stats_sum['pass_accuracy'] / num_matches, 2),
            'avg_corners': round(stats_sum['corners'] / num_matches, 2),
            'avg_yellow_cards': round(stats_sum['yellow_cards'] / num_matches, 2),
            'avg_red_cards': round(stats_sum['red_cards'] / num_matches, 2),
            'avg_fouls': round(stats_sum['fouls'] / num_matches, 2),
            'win_percentage': round(stats_sum['wins'] * 100 / num_matches, 2),
            'draw_percentage': round(stats_sum['draws'] * 100 / num_matches, 2),
            'loss_percentage': round(stats_sum['losses'] * 100 / num_matches, 2),
        }
        
        # Create form summary (e.g., "WDLWW")
        form_summary = ''
        for match in recent_matches[:5]:  # Last 5 matches
            if match['result']:
                form_summary += match['result'][0]  # First letter of result (W/D/L)
        avg_stats['form_summary'] = form_summary
        
        return avg_stats

class FixtureStatsCollector:
    """Class to collect and process statistics for upcoming fixtures."""
    
    def __init__(self, 
                 fixtures_file: Optional[str] = None, 
                 output_dir: str = 'stats_output',
                 max_matches: int = 7):
        """
        Initialize the fixture statistics collector.
        
        Args:
            fixtures_file: Path to fixtures CSV file
            output_dir: Directory to save output files
            max_matches: Number of recent matches to analyze
        """
        self.fixtures_file = fixtures_file
        self.output_dir = output_dir
        self.max_matches = max_matches
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize statistics fetcher
        self.stats_fetcher = FBrefStatsFetcher(max_matches=max_matches)
        
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
            
            # Check if it's the FBref source format or the format you provided
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
                logger.warning(f"Unknown CSV format: {header}")
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
    
    def collect_team_stats(self, team_name: str) -> Tuple[Dict[str, float], List[Dict[str, Any]]]:
        """
        Collect statistics for a team.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Tuple of (average stats, recent matches)
        """
        logger.info(f"Collecting stats for {team_name}")
        
        try:
            # Get recent matches
            recent_matches = self.stats_fetcher.get_team_recent_matches(team_name)
            
            # Calculate averages
            avg_stats = self.stats_fetcher.calculate_team_averages(recent_matches)
            
            return avg_stats, recent_matches
            
        except Exception as e:
            logger.error(f"Error collecting stats for {team_name}: {e}")
            return {}, []
    
    def process_fixtures(self) -> List[Dict[str, Any]]:
        """
        Process fixtures and collect statistics for all teams.
        
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
                home_avg_stats, home_recent_matches = self.collect_team_stats(fixture['home_team'])
                
                # Get away team stats
                away_avg_stats, away_recent_matches = self.collect_team_stats(fixture['away_team'])
                
                # Add to fixture stats
                home_fixture_stats = match_details.copy()
                home_fixture_stats.update({
                    'team_name': fixture['home_team'],
                    'opponent_name': fixture['away_team'],
                    'is_home': True
                })
                home_fixture_stats.update({f"home_{k}": v for k, v in home_avg_stats.items()})
                
                away_fixture_stats = match_details.copy()
                away_fixture_stats.update({
                    'team_name': fixture['away_team'],
                    'opponent_name': fixture['home_team'],
                    'is_home': False
                })
                away_fixture_stats.update({f"away_{k}": v for k, v in away_avg_stats.items()})
                
                # Add recent matches (up to 3)
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
        
        return fixture_stats
    
    def save_stats_to_csv(self, stats: List[Dict[str, Any]], output_file: Optional[str] = None) -> str:
        """
        Save collected statistics to a CSV file.
        
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
            output_file = os.path.join(self.output_dir, f"fbref_team_stats_{timestamp}.csv")
        
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
        Run the fixture statistics collection process.
        
        Returns:
            Path to the output CSV file, or None if failed
        """
        logger.info("Starting fixture statistics collection")
        
        try:
            # Process fixtures
            fixture_stats = self.process_fixtures()
            
            if not fixture_stats:
                logger.warning("No fixture statistics collected")
                return None
            
            # Save statistics to CSV
            output_file = self.save_stats_to_csv(fixture_stats)
            
            if output_file:
                logger.info(f"Statistics collection complete! Results saved to: {output_file}")
                return output_file
            else:
                logger.error("Failed to save statistics to CSV")
                return None
                
        except Exception as e:
            logger.error(f"Error running statistics collection: {e}")
            import traceback
            traceback.print_exc()
            return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='FBref Statistics Collector')
    parser.add_argument('--fixtures', type=str, help='Path to fixtures CSV file')
    parser.add_argument('--output', type=str, default='stats_output', help='Output directory')
    parser.add_argument('--matches', type=int, default=7, help='Number of recent matches to analyze')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()


def main():
    """Main execution function."""
    print("=== FBref Statistics Collector ===")
    
    # Parse arguments
    args = parse_arguments()
    
    # Set logging level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Initialize collector
    collector = FixtureStatsCollector(
        fixtures_file=args.fixtures,
        output_dir=args.output,
        max_matches=args.matches
    )
    
    # Run collection process
    output_file = collector.run()
    
    if output_file:
        print(f"\nProcess complete! Results saved to: {output_file}")
    else:
        print("\nProcess failed. Check the logs for details.")


if __name__ == "__main__":
    main()