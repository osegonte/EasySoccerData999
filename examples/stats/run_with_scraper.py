"""
Example of using TeamStatsCollector with the AdvancedSofaScoreScraper.

This example demonstrates how to:
1. First run the scraper to get upcoming fixtures
2. Then use the TeamStatsCollector to analyze team statistics
"""

import os
import sys
from datetime import date, timedelta

# Add the project root to the Python path to allow importing esd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the scraper (assuming it's in the project root directory)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

try:
    from daily_match_scraper import AdvancedSofaScoreScraper
except ImportError:
    print("Cannot import AdvancedSofaScoreScraper. Please ensure it's in the correct location.")
    sys.exit(1)

from esd.stats import TeamStatsCollector

def main():
    """Main function to demonstrate integration with the scraper."""
    print("=== Football Match Statistics Integration Example ===")
    
    # Step 1: Run the fixture scraper to get upcoming matches
    scraper = AdvancedSofaScoreScraper()
    
    today = date.today()
    end_date = today + timedelta(days=7)
    
    print(f"Fetching fixtures from {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    all_matches, total_matches = scraper.fetch_matches_for_date_range(today, end_date)
    
    # Check if we have matches
    if total_matches == 0:
        print("No upcoming fixtures found. Exiting.")
        return
    
    # Step 2: Use the latest fixtures file
    fixtures_path = os.path.join(
        scraper.data_dir, 
        f"all_matches_{today.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
    )
    
    if not os.path.exists(fixtures_path):
        print(f"Fixtures file not found at {fixtures_path}. Exiting.")
        return
    
    print(f"Found fixtures file: {fixtures_path}")
    
    # Step 3: Run the stats collector
    print("\nCollecting statistics for teams in upcoming fixtures...")
    stats_collector = TeamStatsCollector()
    output_file = stats_collector.run(fixtures_path)
    
    print(f"\nProcess complete!")
    if output_file:
        print(f"Statistics saved to: {output_file}")

if __name__ == "__main__":
    main()