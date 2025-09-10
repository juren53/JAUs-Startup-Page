#!/usr/bin/env python3
"""
Version Checker for JAU's Startup Page
Compares local Startup.html version with the GitHub repository version.

Usage:
    python3 tools/version_checker.py
    python3 tools/version_checker.py --file /path/to/Startup.html
    python3 tools/version_checker.py --verbose
"""

import argparse
import os
import sys
import requests
from datetime import datetime
from pathlib import Path
import re
from typing import Tuple, Optional

# Add parent directory to path for importing project modules if needed
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

class VersionChecker:
    """Check version of local Startup.html against GitHub repository."""
    
    def __init__(self, local_file_path: str = None, verbose: bool = False):
        self.verbose = verbose
        self.local_file_path = local_file_path or os.path.join(parent_dir, 'Startup.html')
        self.github_raw_url = "https://raw.githubusercontent.com/juren53/JAUs-Startup-Page/main/Startup.html"
        
    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def extract_version_info(self, html_content: str) -> dict:
        """Extract version metadata from HTML content."""
        version_info = {}
        
        # Extract version meta tag
        version_match = re.search(r'<meta name="version" content="([^"]*)"', html_content)
        if version_match:
            version_info['version'] = version_match.group(1)
        
        # Extract last-modified meta tag
        modified_match = re.search(r'<meta name="last-modified" content="([^"]*)"', html_content)
        if modified_match:
            version_info['last_modified'] = modified_match.group(1)
        
        # Extract github-repo meta tag
        repo_match = re.search(r'<meta name="github-repo" content="([^"]*)"', html_content)
        if repo_match:
            version_info['github_repo'] = repo_match.group(1)
        
        return version_info
    
    def get_local_version_info(self) -> dict:
        """Get version information from local Startup.html file."""
        self.log(f"Reading local file: {self.local_file_path}")
        
        if not os.path.exists(self.local_file_path):
            raise FileNotFoundError(f"Local file not found: {self.local_file_path}")
        
        with open(self.local_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        version_info = self.extract_version_info(content)
        
        # Add file stats
        stat = os.stat(self.local_file_path)
        version_info['file_size'] = stat.st_size
        version_info['file_mtime'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        self.log(f"Local version: {version_info.get('version', 'Unknown')}")
        return version_info
    
    def get_remote_version_info(self) -> dict:
        """Get version information from GitHub repository."""
        self.log(f"Fetching remote file from: {self.github_raw_url}")
        
        try:
            response = requests.get(self.github_raw_url, timeout=30)
            response.raise_for_status()
            
            version_info = self.extract_version_info(response.text)
            version_info['content_length'] = len(response.text)
            
            self.log(f"Remote version: {version_info.get('version', 'Unknown')}")
            return version_info
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch remote version: {e}")
    
    def compare_versions(self, local_info: dict, remote_info: dict) -> dict:
        """Compare local and remote version information."""
        comparison = {
            'is_up_to_date': False,
            'local': local_info,
            'remote': remote_info,
            'differences': []
        }
        
        # Compare version strings
        local_version = local_info.get('version', '')
        remote_version = remote_info.get('version', '')
        
        if local_version != remote_version:
            comparison['differences'].append(f"Version: {local_version} → {remote_version}")
        
        # Compare last modified dates
        local_modified = local_info.get('last_modified', '')
        remote_modified = remote_info.get('last_modified', '')
        
        if local_modified != remote_modified:
            comparison['differences'].append(f"Modified: {local_modified} → {remote_modified}")
        
        # Compare file sizes
        local_size = local_info.get('file_size', 0)
        remote_size = remote_info.get('content_length', 0)
        
        if abs(local_size - remote_size) > 100:  # Allow small differences
            comparison['differences'].append(f"Size: {local_size} → {remote_size} bytes")
        
        # Determine if up to date
        comparison['is_up_to_date'] = (
            local_version == remote_version and 
            local_modified == remote_modified and
            len(comparison['differences']) == 0
        )
        
        return comparison
    
    def check_version(self) -> dict:
        """Perform complete version check."""
        self.log("Starting version check...")
        
        try:
            local_info = self.get_local_version_info()
            remote_info = self.get_remote_version_info()
            comparison = self.compare_versions(local_info, remote_info)
            
            self.log(f"Version check complete. Up to date: {comparison['is_up_to_date']}")
            return comparison
            
        except Exception as e:
            self.log(f"Version check failed: {e}", "ERROR")
            raise

def print_version_report(comparison: dict, verbose: bool = False):
    """Print a formatted version check report."""
    print("📄 JAU's Startup Page - Version Check Report")
    print("=" * 50)
    
    local = comparison['local']
    remote = comparison['remote']
    
    print(f"Local Version:  {local.get('version', 'Unknown')}")
    print(f"Remote Version: {remote.get('version', 'Unknown')}")
    print()
    
    if comparison['is_up_to_date']:
        print("✅ Status: UP TO DATE")
        print("Your local copy matches the latest version on GitHub.")
    else:
        print("⚠️  Status: UPDATE AVAILABLE")
        print("Your local copy differs from the GitHub version.")
        print("\nDifferences found:")
        for diff in comparison['differences']:
            print(f"  • {diff}")
        
        repo_url = remote.get('github_repo', 'https://github.com/juren53/JAUs-Startup-Page')
        print(f"\n🔗 Get the latest version: {repo_url}")
    
    if verbose:
        print("\n" + "─" * 30)
        print("Detailed Information:")
        print(f"Local file size:    {local.get('file_size', 'Unknown')} bytes")
        print(f"Remote content size: {remote.get('content_length', 'Unknown')} bytes")
        print(f"Local modified:     {local.get('last_modified', 'Unknown')}")
        print(f"Remote modified:    {remote.get('last_modified', 'Unknown')}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check if local Startup.html is up to date with GitHub repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/version_checker.py
  python3 tools/version_checker.py --file /path/to/Startup.html
  python3 tools/version_checker.py --verbose
        """
    )
    
    parser.add_argument('--file', '-f', 
                       help='Path to local Startup.html file (default: ./Startup.html)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        checker = VersionChecker(args.file, args.verbose)
        comparison = checker.check_version()
        print_version_report(comparison, args.verbose)
        
        # Exit code: 0 if up to date, 1 if update available
        sys.exit(0 if comparison['is_up_to_date'] else 1)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(2)
    except ConnectionError as e:
        print(f"❌ Network Error: {e}")
        sys.exit(3)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
