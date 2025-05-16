"""
Advanced Football Match Statistics Collector

This script:
1. Fetches upcoming football fixtures using the AdvancedSofaScoreScraper
2. Collects performance statistics for teams in those fixtures using TeamStatsCollector
3. Outputs a CSV file with comprehensive statistics for match analysis

Usage:
    python run_stats_collector.py [OPTIONS]

Options:
    --days N             Number of days to look ahead for fixtures (default: 7)
    --output DIR         Directory to save output files (default: 'stats_output')
    --max-retries N      Maximum number of retries for API calls (default: 3)
    --retry-delay N      Delay between retries in seconds (default: 5)
    --skip-stats         Skip collecting statistics (just fetch fixtures)
    --fixtures-only      Only collect fixtures data, not player stats
    --use-proxy          Use proxy rotation if available

Troubleshooting:
    If you're experiencing "403 Forbidden" errors from SofaScore API:
    1. Try using a VPN or proxy with the --use-proxy flag
    2. Consider using the --fixtures-only flag to just collect fixtures
    3. Increase --retry-delay to avoid rate limiting
"""

import os
import sys
import time
import argparse
import platform
import subprocess
import random
from datetime import date, timedelta
from importlib.util import find_spec

def check_environment():
    """Check if the environment is properly set up to run the script."""
    print("Checking environment...")
    
    # Operating system info
    print(f"Operating System: {platform.system()} {platform.version()}")
    print(f"Python Version: {platform.python_version()}")
    
    # Check if running in virtual environment
    in_venv = sys.prefix != sys.base_prefix
    print(f"Running in virtual environment: {in_venv}")
    
    # Check for Chrome
    chrome_paths = {
        'Darwin': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'Windows': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'Linux': '/usr/bin/google-chrome'
    }
    
    default_path = chrome_paths.get(platform.system())
    if default_path and os.path.exists(default_path):
        print(f"Chrome found at: {default_path}")
    else:
        print("WARNING: Default Chrome path not found. Will attempt auto-detection.")
    
    # Check required libraries
    required_packages = [
        'httpx', 'lxml', 'pandas', 'playwright',
        'selenium', 'webdriver_manager'
    ]
    
    missing_packages = []
    for package in required_packages:
        if not find_spec(package):
            missing_packages.append(package)
    
    if missing_packages:
        print(f"WARNING: Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install " + " ".join(missing_packages))
        return False
    
    # Check Playwright installation
    try:
        # Try importing playwright to see if it's installed
        import playwright
        from playwright.sync_api import sync_playwright
        
        # Get Playwright version from the installed package
        try:
            playwright_version = subprocess.check_output(
                [sys.executable, '-m', 'pip', 'show', 'playwright'], 
                text=True
            )
            for line in playwright_version.split('\n'):
                if line.startswith('Version:'):
                    version = line.split(':', 1)[1].strip()
                    print(f"Playwright version: {version}")
                    break
        except subprocess.SubprocessError:
            print("Playwright is installed, but version couldn't be determined")
            
        # Check if browsers are installed
        try:
            with sync_playwright() as p:
                if p.chromium:
                    print("Playwright browsers are installed")
                else:
                    print("WARNING: Playwright browsers may not be properly installed")
        except Exception as e:
            print(f"WARNING: Error checking Playwright browsers: {e}")
            print("You may need to run: playwright install")
            
    except ImportError:
        print("WARNING: Playwright module could not be imported properly")
        return False
    
    print("Environment check completed.")
    return True
    
def get_random_delay(min_seconds=1, max_seconds=3):
    """Generate a random delay to avoid rate limiting."""
    return min_seconds + random.random() * (max_seconds - min_seconds)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Football Match Statistics Collector')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look ahead')
    parser.add_argument('--output', type=str, default='stats_output', help='Output directory')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retries for API calls')
    parser.add_argument('--retry-delay', type=int, default=5, help='Delay between retries in seconds')
    parser.add_argument('--skip-stats', action='store_true', help='Skip collecting statistics (just fetch fixtures)')
    parser.add_argument('--fixtures-only', action='store_true', help='Only collect fixtures data, not player stats')
    parser.add_argument('--use-proxy', action='store_true', help='Use proxy rotation if available')
    return parser.parse_args()

def process_fixture_collection(scraper, days, output_dir):
    """Run the fixture collection process."""
    today = date.today()
    end_date = today + timedelta(days=days)
    
    print(f"Fetching fixtures from {today.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    try:
        all_matches, total_matches = scraper.fetch_matches_for_date_range(today, end_date)
        
        # Check if we have matches
        if total_matches == 0:
            print("No upcoming fixtures found. Exiting.")
            return None
        
        # Get the latest fixtures file
        fixtures_path = os.path.join(
            scraper.data_dir, 
            f"all_matches_{today.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        )
        
        if not os.path.exists(fixtures_path):
            print(f"Fixtures file not found at {fixtures_path}. Exiting.")
            return None
        
        print(f"Found fixtures file: {fixtures_path}")
        return fixtures_path
    
    except Exception as e:
        print(f"ERROR: Failed to collect fixtures: {e}")
        import traceback
        traceback.print_exc()
        return None

def process_stats_collection(fixtures_path, output_dir, max_retries=3, retry_delay=5):
    """Run the stats collection process."""
    from esd.stats import TeamStatsCollector
    
    try:
        print("\nCollecting statistics for teams in upcoming fixtures...")
        stats_collector = TeamStatsCollector(data_dir=output_dir)
        
        # Override the get_match_statistics method to add retry logic
        original_get_match_statistics = stats_collector.get_match_statistics
        
        def get_match_statistics_with_retry(match_id, team_id):
            """Wrapper around get_match_statistics with retry logic."""
            for attempt in range(max_retries):
                try:
                    return original_get_match_statistics(match_id, team_id)
                except Exception as e:
                    if "403" in str(e) or "Forbidden" in str(e):
                        print(f"  Received 403 Forbidden when getting match stats (attempt {attempt+1}/{max_retries})")
                    else:
                        print(f"  Error getting match stats: {e} (attempt {attempt+1}/{max_retries})")
                    
                    if attempt < max_retries - 1:
                        actual_delay = retry_delay + get_random_delay()
                        print(f"  Retrying in {actual_delay:.1f} seconds...")
                        time.sleep(actual_delay)
                    else:
                        print("  Max retries reached. Returning empty stats.")
                        return {}
        
        # Replace the method with our retry version
        stats_collector.get_match_statistics = get_match_statistics_with_retry
        
        output_file = stats_collector.run(fixtures_path)
        
        if output_file:
            print(f"Statistics saved to: {output_file}")
            return output_file
        else:
            print("Failed to save statistics.")
            return None
            
    except Exception as e:
        print(f"ERROR: Failed to collect stats: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main execution function."""
    print("=== Football Match Statistics Collector ===")
    
    args = parse_arguments()
    
    # Check environment first
    if not check_environment():
        print("Environment check failed. Please fix the issues and try again.")
        return
    
    # Import the required modules
    try:
        from daily_match_scraper import AdvancedSofaScoreScraper
    except ImportError as e:
        print(f"ERROR: Failed to import daily_match_scraper: {e}")
        print("Make sure the daily_match_scraper.py file is in the correct location.")
        return
    
    # Step 1: Run the fixture scraper to get upcoming matches
    try:
        # Initialize the scraper with proxy settings if requested
        scraper_args = {}
        if args.use_proxy:
            # Add your proxy configuration here if you have it
            print("Using proxy rotation for API requests")
            # Example: scraper_args['proxies'] = [{'http': 'http://proxy1:8080', 'https': 'https://proxy1:8080'}]
        
        scraper = AdvancedSofaScoreScraper(**scraper_args)
        
        # Get fixtures
        fixtures_path = process_fixture_collection(scraper, args.days, args.output)
        if not fixtures_path:
            return
        
        # Step 2: If we have fixtures and user hasn't requested to skip stats, collect stats
        if not args.skip_stats and not args.fixtures_only:
            process_stats_collection(
                fixtures_path, 
                args.output,
                max_retries=args.max_retries,
                retry_delay=args.retry_delay
            )
        else:
            print("\nSkipping statistics collection as requested.")
            print(f"Fixtures data is available at: {fixtures_path}")
        
        print("\nProcess complete!")
        
    except Exception as e:
        print(f"ERROR: An exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()