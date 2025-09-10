#!/usr/bin/env python3
"""
Script to parse links.txt into two columns: URL and Description.
The result is saved in parsed-links.txt.
"""
import re
from pathlib import Path

def parse_links(input_file, output_file):
    # Regular expression to extract URL and description from anchor tags
    link_pattern = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        links_content = f.read()
    
    # Find all matches
    matches = link_pattern.findall(links_content)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("URL\tDescription\n")
        f.write("-" * 50 + "\t" + "-" * 30 + "\n")
        
        # Write data rows
        for url, description in matches:
            f.write(f"{url}\t{description}\n")
    
    return len(matches)

if __name__ == "__main__":
    input_file = Path("links.txt")
    output_file = Path("parsed-links.txt")
    
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found.")
        exit(1)
    
    link_count = parse_links(input_file, output_file)
    print(f"Successfully parsed {link_count} links from '{input_file}' to '{output_file}'.")

