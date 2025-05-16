"""
Full Pipeline for Football Match Analysis.

This script runs the complete pipeline:
1. Scrapes fixtures data from SofaScore for upcoming matches
2. Analyzes team statistics based on recent matches
3. Saves both datasets for further analysis

Usage:
    python full_pipeline.py
"""

import os
import time
from datetime import date, timedelta
from daily_match_scraper import AdvancedSofaScoreScraper
from esd.stats.team_stats import TeamStatsCollector

def test_scraper():
    """Test the scraper functionality"""
    print("=== Testing SofaScore Scraper ===")
    
    # Initialize scraper
    scraper = AdvancedSofaScoreScraper()
    
    # Initialize browser session and get cookies
    success = scraper.initialize_browser_session()
    if not success:
        print("⚠️ Warning: Browser session initialization failed")
    
    # Test a single date to verify API access
    test_date = date.today().strftime("%Y-%m-%d")
    events = scraper.fetch_events_via_api(test_date)
    
    if events:
        print(f"✓ API test successful! Found {len(events)} events for {test_date}")
        return True
    else:
        print("✖ API test failed. Checking browser fallback...")
        events = scraper.fetch_events_via_browser(test_date)
        
        if events:
            print(f"✓ Browser fallback successful! Found {len(events)} events for {test_date}")
            return True
        else:
            print("✖ Browser fallback also failed. Checking FBref...")
            matches = scraper.try_fbref_fallback(test_date)
            
            if matches:
                print(f"✓ FBref fallback successful! Found {len(matches)} matches for {test_date}")
                return True
            else:
                print("✖ All methods failed! Please check your network or try again later.")
                return False

def main():
    """Run the full pipeline"""
    print("=== Football Match Analysis Pipeline ===")
    
    # Optional: Test scraper first
    test_result = test_scraper()
    if not test_result:
        if input("All methods failed. Continue anyway? (y/n): ").lower() != 'y':
            return
    
    # Step 1: Initialize scraper
    print("\n--- Phase 1: Fixture Scraping ---")
    scraper = AdvancedSofaScoreScraper()
    
    # Calculate date range for next week
    today = date.today()
    end_date = today + timedelta(days=7)
    
    print(f"Fetching fixtures from {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Step 2: Fetch matches for the next week
    all_matches, total_matches = scraper.fetch_matches_for_date_range(today, end_date)
    
    # Check if we have matches
    if total_matches == 0:
        print("No upcoming fixtures found. Exiting.")
        return
    
    # Print statistics
    scraper.print_statistics(all_matches)
    
    # Get path to the fixtures file
    fixtures_path = os.path.join(
        scraper.data_dir, 
        f"all_matches_{today.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
    )
    
    if not os.path.exists(fixtures_path):
        print(f"Fixtures file not found at {fixtures_path}. Exiting.")
        return
    
    print(f"Fixtures saved to: {fixtures_path}")
    
    # Step 3: Run the stats collector
    print("\n--- Phase 2: Team Statistics Analysis ---")
    print("This phase will analyze the most recent 7 matches for each team...")
    
    # Wait a bit before starting the next phase
    time.sleep(5)
    
    stats_collector = TeamStatsCollector()
    output_file = stats_collector.run(fixtures_path)
    
    print(f"\n=== Pipeline Complete! ===")
    print(f"Fixtures data: {fixtures_path}")
    print(f"Team statistics: {output_file}")
    print("\nYou can now use these files for further analysis or modeling.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation canceled by user")
    except Exception as e:
        print(f"\n✖ Error in pipeline: {str(e)}")