#!/usr/bin/env python3
"""
Link Checker - A Python CLI tool to check for broken links in HTML files.

This script accepts one or more HTML files as command line arguments, extracts
all hyperlinks from them, and verifies whether those links are valid by sending
HTTP requests. It reports broken links along with their status codes.

Usage:
    python linkchecker.py file1.html file2.html ...
    python linkchecker.py --verbose file.html
    python linkchecker.py --timeout 10 file.html
    python linkchecker.py --workers 8 file.html
"""

import argparse
import concurrent.futures
import os
import sys
import time
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


class LinkChecker:
    """Class to check for broken links in HTML files."""

    def __init__(self, timeout: int = 5, verbose: bool = False, max_workers: int = 10):
        """
        Initialize the LinkChecker.

        Args:
            timeout: Timeout for HTTP requests in seconds
            verbose: Whether to print verbose output
            max_workers: Maximum number of concurrent workers for link checking
        """
        self.timeout = timeout
        self.verbose = verbose
        self.max_workers = max_workers
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Store results for reporting
        self.successful_links: Dict[str, List[str]] = {}
        self.broken_links: Dict[str, Dict[str, Tuple[str, int, str]]] = {}
        self.skipped_links: Dict[str, Set[str]] = {}

    def _log(self, message: str):
        """Print a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def _extract_links(self, html_content: str, base_url: str = "") -> List[Tuple[str, str]]:
        """
        Extract all links from HTML content.
        
        Args:
            html_content: HTML content to parse
            base_url: Base URL for resolving relative links

        Returns:
            List of tuples containing (link, link_text)
        """
        links = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all anchor tags with href attribute
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                link_text = anchor.get_text(strip=True) or href
                
                # Skip empty links, javascript:, and mailto: links
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:')):
                    continue
                    
                # Handle relative URLs
                if base_url and not urlparse(href).netloc:
                    href = urljoin(base_url, href)
                    
                links.append((href, link_text))
                
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            
        return links
        
    def _check_link(self, url: str, link_text: str) -> Tuple[str, bool, int, str]:
        """
        Check if a link is valid by sending a HEAD request.
        
        Args:
            url: URL to check
            link_text: Text of the link for reporting

        Returns:
            Tuple of (url, is_valid, status_code, error_message)
        """
        headers = {'User-Agent': self.user_agent}
        try:
            # Skip checking non-HTTP URLs
            if not url.startswith(('http://', 'https://')):
                return url, False, 0, "Skipped: Non-HTTP URL"
                
            # Try HEAD request first (faster)
            response = requests.head(url, timeout=self.timeout, headers=headers, allow_redirects=True)
            
            # If HEAD request fails, try GET request
            if response.status_code >= 400:
                response = requests.get(url, timeout=self.timeout, headers=headers, allow_redirects=True)
                
            if response.status_code < 400:
                self._log(f"✓ {url} ({response.status_code})")
                return url, True, response.status_code, ""
            else:
                self._log(f"✗ {url} ({response.status_code})")
                return url, False, response.status_code, f"HTTP Error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            self._log(f"✗ {url} (Timeout)")
            return url, False, 0, f"Timeout after {self.timeout} seconds"
        except requests.exceptions.SSLError:
            self._log(f"✗ {url} (SSL Error)")
            return url, False, 0, "SSL Certificate Error"
        except requests.exceptions.ConnectionError:
            self._log(f"✗ {url} (Connection Error)")
            return url, False, 0, "Connection Error"
        except Exception as e:
            self._log(f"✗ {url} (Error: {str(e)})")
            return url, False, 0, str(e)

    def check_file(self, file_path: str) -> bool:
        """
        Check all links in an HTML file.
        
        Args:
            file_path: Path to the HTML file

        Returns:
            True if all links are valid, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return False
            
        try:
            # Initialize collections for this file
            self.successful_links[file_path] = []
            self.broken_links[file_path] = {}
            self.skipped_links[file_path] = set()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Extract links from the HTML file
            print(f"\nChecking links in {file_path}...")
            links = self._extract_links(html_content)
            print(f"Found {len(links)} links to check")
            
            # Use a thread pool to check links concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                for url, link_text in links:
                    futures.append(executor.submit(self._check_link, url, link_text))
                    
                # Process results as they complete
                for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                    url, is_valid, status_code, error_message = future.result()
                    
                    # Print progress
                    if self.verbose:
                        print(f"Progress: {i}/{len(links)}")
                    else:
                        sys.stdout.write(f"\rChecking links: {i}/{len(links)}")
                        sys.stdout.flush()
                        
                    # Store results
                    if not url.startswith(('http://', 'https://')):
                        self.skipped_links[file_path].add(url)
                    elif is_valid:
                        self.successful_links[file_path].append(url)
                    else:
                        self.broken_links[file_path][url] = (
                            next((text for link, text in links if link == url), ""),
                            status_code,
                            error_message
                        )
            
            print("\nLink checking completed.")
            return len(self.broken_links[file_path]) == 0
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return False

    def report(self):
        """Generate a report of broken links."""
        total_files = len(self.broken_links)
        total_broken = sum(len(broken) for broken in self.broken_links.values())
        total_valid = sum(len(valid) for valid in self.successful_links.values())
        total_skipped = sum(len(skipped) for skipped in self.skipped_links.values())
        
        print("\n" + "=" * 80)
        print(f"LINK CHECKER REPORT")
        print("=" * 80)
        print(f"Total files checked: {total_files}")
        print(f"Total links checked: {total_valid + total_broken}")
        print(f"Valid links: {total_valid}")
        print(f"Broken links: {total_broken}")
        print(f"Skipped links: {total_skipped}")
        print("=" * 80)
        
        if total_broken > 0:
            print("\nBROKEN LINKS DETAILS:")
            print("-" * 80)
            
            for file_path, broken in self.broken_links.items():
                if broken:
                    print(f"\nIn file: {file_path}")
                    print("-" * 40)
                    
                    for url, (link_text, status_code, error_message) in broken.items():
                        print(f"✗ {url}")
                        print(f"  Text: {link_text[:60] + '...' if len(link_text) > 60 else link_text}")
                        print(f"  Error: {error_message}")
                        print()
        else:
            print("\nAll links are valid! 🎉")
            
        if total_skipped > 0 and self.verbose:
            print("\nSKIPPED LINKS:")
            print("-" * 80)
            
            for file_path, skipped in self.skipped_links.items():
                if skipped:
                    print(f"\nIn file: {file_path}")
                    for url in skipped:
                        print(f"- {url}")


def main():
    """Main function to parse arguments and run the link checker."""
    parser = argparse.ArgumentParser(
        description="Check for broken links in HTML files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "files", nargs="+", help="HTML files to check"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=5,
        help="Timeout for HTTP requests in seconds"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Print verbose output"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=10,
        help="Maximum number of concurrent workers"
    )
    
    args = parser.parse_args()
    
    # Create a link checker instance
    checker = LinkChecker(
        timeout=args.timeout,
        verbose=args.verbose,
        max_workers=args.workers
    )
    
    # Check each file
    start_time = time.time()
    results = []
    
    for file_path in args.files:
        result = checker.check_file(file_path)
        results.append(result)
    
    # Generate report
    checker.report()
    
    # Print execution time
    execution_time = time.time() - start_time
    print(f"\nExecution time: {execution_time:.2f} seconds")
    
    # Return exit code: 0 if all links are valid, 1 otherwise
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

