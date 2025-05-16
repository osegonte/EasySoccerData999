import os
import time
from datetime import date, timedelta
from daily_match_scraper import AdvancedSofaScoreScraper
from esd.stats.team_stats import TeamStatsCollector

def test_api_access(scraper):
    """Test if the API is accessible"""
    print("Running API access test...")
    test_date = date.today().strftime("%Y-%m-%d")
    test_events = scraper.fetch_events_via_api(test_date)
    if test_events:
        print(f"✓ API test successful! Found {len(test_events)} events.")
        return True
    else:
        print("✖ API test failed.")
        return False

def main():
    print("=== Football Match Statistics Pipeline ===")
    
    # Step 1: Initialize scraper
    scraper = AdvancedSofaScoreScraper()
    
    # Initialize browser session and test API access
    print("Initializing browser session...")
    session_success = scraper.initialize_browser_session()
    if not session_success:
        print("⚠️ Browser session initialization failed, but continuing anyway...")
    
    # Test API access
    api_access = test_api_access(scraper)
    if not api_access:
        print("⚠️ API access test failed, but will attempt to continue with fallback methods.")
    
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
    
    # Step 3: Use the latest fixtures file
    fixtures_path = os.path.join(
        scraper.data_dir, 
        f"all_matches_{today.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
    )
    
    if not os.path.exists(fixtures_path):
        print(f"Fixtures file not found at {fixtures_path}. Exiting.")
        return
    
    print(f"Found fixtures file: {fixtures_path}")
    
    # Step 4: Run the stats collector
    print("\nWaiting 10 seconds before collecting statistics...")
    time.sleep(10)  # Give some time between scraping and analysis
    
    print("Collecting statistics for teams in upcoming fixtures...")
    stats_collector = TeamStatsCollector()
    output_file = stats_collector.run(fixtures_path)
    
    print(f"\nProcess complete!")
    print(f"Statistics saved to: {output_file}")

if __name__ == "__main__":
    main()