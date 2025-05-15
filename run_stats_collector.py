#!/usr/bin/env python3
"""
Football Match Statistics Collector
This script collects football match data and analyzes team statistics for upcoming fixtures.
"""

import os
import sys
from datetime import date, timedelta
from pathlib import Path
import platform

# Try to import the required modules
try:
    from daily_match_scraper import AdvancedSofaScoreScraper
except ImportError:
    print("Error: Could not import AdvancedSofaScoreScraper. Make sure the file is in the correct location.")
    sys.exit(1)

try:
    from esd.stats.match_stats_collector import TeamStatsCollector
except ImportError:
    print("Error: Could not import TeamStatsCollector. Make sure EasySoccerData is installed correctly.")
    sys.exit(1)

def check_environment():
    """Check if the environment is properly set up"""
    print("Checking environment...")
    
    # Get system info
    system = platform.system()
    print(f"Operating System: {system} {platform.version()}")
    print(f"Python Version: {platform.python_version()}")
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    print(f"Running in virtual environment: {in_venv}")
    
    # For macOS, check Chrome location
    if system == "Darwin":
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            f"/Users/{os.getlogin()}/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"Chrome found at: {path}")
                chrome_found = True
                break
        
        if not chrome_found:
            print("Warning: Could not find Chrome at standard locations.")
            print("You may need to install Chrome or specify the browser path manually.")
    
    # Check if playwright is installed
    try:
        import playwright
        print(f"Playwright version: {playwright.__version__}")
    except ImportError:
        print("Warning: Playwright not installed. Installing it might resolve browser issues.")
        print("You can install it with: pip install playwright && python -m playwright install")
    
    print("Environment check complete.\n")

def main():
    """Main function to run the statistics collection process"""
    print("=== Football Match Statistics Collector ===")
    
    # Check environment first
    check_environment()
    
    # Step 1: Run the fixture scraper to get upcoming matches
    print("Initializing match scraper...")
    scraper = AdvancedSofaScoreScraper()
    
    today = date.today()
    end_date = today + timedelta(days=7)
    
    print(f"Fetching fixtures from {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    try:
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
        
        if output_file:
            print(f"\nProcess complete!")
            print(f"Statistics saved to: {output_file}")
        else:
            print("\nError: Failed to generate statistics file.")
            
    except RuntimeError as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting suggestions:")
        print("1. Make sure Chrome or another Chromium browser is installed on your system")
        print("2. If you're on macOS, check if Chrome is in your Applications folder")
        print("3. Try installing playwright browsers with: python -m playwright install")
        print("4. If problems persist, try modifying the SofascoreService.py file to manually specify your browser path")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")

if __name__ == "__main__":
    main()