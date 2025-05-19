#!/usr/bin/env python3
"""
Script to extract all links from an HTML file and format them consistently.
"""
from bs4 import BeautifulSoup
import os
import sys
import re

def extract_links(html_file, output_file):
    """Extract all links from an HTML file and save them to an output file."""
    try:
        # Check if the HTML file exists
        if not os.path.exists(html_file):
            print(f"Error: File '{html_file}' not found.")
            return False
            
        # Parse the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            try:
                soup = BeautifulSoup(f, 'html.parser')
            except Exception as e:
                print(f"Error parsing HTML: {e}")
                return False
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        # Format and write links to output file
        with open(output_file, 'w', encoding='utf-8') as out:
            for link in links:
                href = link.get('href')
                
                # Get link text, handle empty text and clean up whitespace
                text = link.get_text()
                # Replace multiple whitespace chars (including newlines, tabs) with a single space
                text = re.sub(r'\s+', ' ', text).strip()
                if not text:
                    # Use URL as text if no text is available
                    text = href
                
                # Format according to template and write to file
                formatted_link = f'<a href="{href}">{text}</a>\n'
                out.write(formatted_link)
        
        print(f"Successfully extracted {len(links)} links to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    html_file = "index.html"
    output_file = "links.txt"
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    success = extract_links(html_file, output_file)
    if not success:
        sys.exit(1)

