"""
Simplified Pipeline for Football Match Analysis.

This script runs a simplified pipeline focusing on the FBref fallback:
1. Scrapes fixtures data primarily from FBref for upcoming matches
2. Analyzes team statistics based on recent matches
3. Saves both datasets for further analysis

Usage:
    python simplified_pipeline.py
"""

import os
import time
from datetime import date, timedelta
from daily_match_scraper import AdvancedSofaScoreScraper
from esd.stats.team_stats import TeamStatsCollector

def main():
    """Run the simplified pipeline"""
    print("=== Simplified Football Match Analysis Pipeline ===")
    
    # Step 1: Initialize scraper
    print("\n--- Phase 1: Fixture Scraping (Using FBref Fallback) ---")
    scraper = AdvancedSofaScoreScraper()
    
    # Get cookies, but we know API will likely fail
    scraper.initialize_browser_session()
    
    # Calculate date range for next week
    today = date.today()
    end_date = today + timedelta(days=7)
    
    print(f"Fetching fixtures from {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Create an all_matches_by_date dictionary
    all_matches_by_date = {}
    total_matches = 0
    
    # Process each date - going straight to FBref
    for current_date in [today + timedelta(days=i) for i in range(8)]:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"\nProcessing date: {date_str}")
        
        # Skip the SofaScore API and browser attempts, go straight to FBref
        matches = scraper.try_fbref_fallback(date_str)
        
        if matches:
            # Save matches for this date
            date_file = os.path.join(scraper.daily_dir, f"matches_{date_str}.csv")
            scraper.save_matches_to_csv(matches, date_file)
            
            # Add to overall collection
            all_matches_by_date[date_str] = matches
            total_matches += len(matches)
            
            print(f"  ✓ Processed {len(matches)} matches for {date_str}")
        else:
            print(f"  ✖ No matches found for {date_str}")
    
    # Save all matches to a single CSV
    all_matches = []
    for date_str, matches in all_matches_by_date.items():
        for match in matches:
            match['date'] = date_str
            all_matches.append(match)
    
    if all_matches:
        all_file = os.path.join(scraper.data_dir, f"all_matches_{today.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv")
        
        # Extended fieldnames for combined file
        fieldnames = [
            'date', 'id', 'home_team', 'away_team', 'league', 'country',
            'start_timestamp', 'start_time', 'status', 'venue', 'round', 'source'
        ]
        
        with open(all_file, 'w', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for match in all_matches:
                writer.writerow(match)
        
        print(f"\n✓ Saved {len(all_matches)} total matches to {all_file}")
    
    # Print statistics
    scraper.print_statistics(all_matches_by_date)
    
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