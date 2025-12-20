#!/usr/bin/env python3
"""
Jmix UI Samples Scraper for Context7
Fetches UI samples documentation from https://demo.jmix.io/ui-samples/doc
"""

import os
import shutil
import argparse
import requests
from pathlib import Path
import time


class JmixUISamplesScraper:
    def __init__(self, base_url="https://demo.jmix.io/ui-samples/doc", output_dir="jmix_ui_samples"):
        """
        Initialize the UI samples scraper.

        Args:
            base_url: Base URL for UI samples documentation
            output_dir: Directory to save markdown files
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def create_output_dir(self):
        """Create output directory. Clear it if not empty."""
        if os.path.exists(self.output_dir):
            print(f"Clearing existing directory: {self.output_dir}")
            shutil.rmtree(self.output_dir)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir}")

    def fetch_paths(self):
        """
        Fetch the JSON array of paths from the base URL.

        Returns:
            List of paths or None if failed
        """
        try:
            print(f"Fetching paths from: {self.base_url}")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            paths = response.json()

            if not isinstance(paths, list):
                print(f"Error: Expected JSON array, got {type(paths)}")
                return None

            print(f"Found {len(paths)} paths")
            return paths
        except Exception as e:
            print(f"Error fetching paths: {e}")
            return None

    def fetch_document(self, path):
        """
        Fetch a document from the given path.

        Args:
            path: Path to append to base URL

        Returns:
            Text content or None if failed
        """
        url = f"{self.base_url}/{path}"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def sanitize_filename(self, path):
        """
        Convert a path to a valid filename.

        Args:
            path: Path string (e.g., "avatar" or "button/basic")

        Returns:
            Sanitized filename with .md extension
        """
        # Replace slashes and other problematic characters
        filename = path.replace('/', '_').replace('\\', '_')

        # Remove or replace other potentially problematic characters
        filename = filename.replace(' ', '_')

        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'

        return filename

    def save_document(self, content, filename):
        """
        Save document content to a file.

        Args:
            content: Text content to save
            filename: Name of the file
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

    def scrape(self):
        """Main scraping process."""
        print("Starting Jmix UI Samples scraper...")

        # Create output directory
        self.create_output_dir()

        # Fetch the list of paths
        paths = self.fetch_paths()
        if not paths:
            print("Failed to fetch paths. Exiting.")
            return

        # Process each path
        print(f"\nProcessing {len(paths)} documents...")
        for i, path in enumerate(paths, 1):
            print(f"\n[{i}/{len(paths)}] Processing: {path}")

            # Fetch the document
            content = self.fetch_document(path)
            if not content:
                continue

            # Generate filename and save
            filename = self.sanitize_filename(path)
            self.save_document(content, filename)

            # Be nice to the server
            time.sleep(0.3)

        print(f"\n✓ Scraping completed! Files saved to: {self.output_dir}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape Jmix UI Samples documentation and prepare it for Context7'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for scraped UI samples documentation'
    )
    parser.add_argument(
        '--base-url',
        default='https://demo.jmix.io/ui-samples/doc',
        help='Base URL of Jmix UI Samples (default: https://demo.jmix.io/ui-samples/doc)'
    )

    args = parser.parse_args()

    scraper = JmixUISamplesScraper(
        base_url=args.base_url,
        output_dir=args.output_dir
    )
    scraper.scrape()


if __name__ == "__main__":
    main()
