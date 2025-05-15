"""
Example of using TeamStatsCollector to collect team statistics.

This example shows how to collect statistics for teams in upcoming fixtures
using a CSV file of fixtures as input.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path to allow importing esd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from esd.stats import TeamStatsCollector

def main():
    """Main function to demonstrate the TeamStatsCollector."""
    print("=== Team Statistics Collector Example ===")
    
    # Path to your fixtures CSV file
    fixtures_path = input("Enter the path to your fixtures CSV file: ")
    
    if not os.path.exists(fixtures_path):
        print(f"Error: File not found at {fixtures_path}")
        return
    
    # Initialize the stats collector
    collector = TeamStatsCollector(data_dir="output_stats")
    
    # Run the collector
    output_file = collector.run(fixtures_path)
    
    print("\nStatistics collection complete!")
    if output_file:
        print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()