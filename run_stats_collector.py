import os
from datetime import date, timedelta
from daily_match_scraper import AdvancedSofaScoreScraper
from esd.stats.match_stats_collector import TeamStatsCollector

def main():
    print("=== Football Match Statistics Collector ===")
    
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
    print(f"Statistics saved to: {output_file}")

if __name__ == "__main__":
    main()