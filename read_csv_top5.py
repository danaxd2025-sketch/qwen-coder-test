#!/usr/bin/env python3
"""
Script to read a CSV file and print the top 5 rows.

Usage: python script.py <csv_file_path>
"""

import sys
import csv


def print_top_5_rows(csv_file_path):
    """Read a CSV file and print the top 5 rows."""
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            print(f"Top 5 rows from '{csv_file_path}':\n")
            
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                print(f"Row {i + 1}: {row}")
                
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    print_top_5_rows(csv_file_path)
