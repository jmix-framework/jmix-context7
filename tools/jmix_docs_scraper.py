#!/usr/bin/env python3
"""
Jmix Documentation Scraper for Context7
Scrapes Jmix documentation from https://docs.jmix.io/jmix and prepares it for Context7.
"""

import os
import re
import shutil
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time


class JmixDocsScraper:
    def __init__(self, base_url="https://docs.jmix.io/jmix/", output_dir="jmix_docs"):
        """
        Initialize the scraper.

        Args:
            base_url: Base URL of the Jmix documentation
            output_dir: Directory to save processed HTML files
        """
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
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

    def fetch_page(self, url):
        """
        Fetch a page from the given URL.

        Args:
            url: URL to fetch

        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_nav_links(self, soup, base_url):
        """
        Extract all navigation links from the page using a.nav-link selector.

        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL to resolve relative links

        Returns:
            List of absolute URLs
        """
        links = []
        nav_links = soup.select('a.nav-link')

        for link in nav_links:
            href = link.get('href')
            if href:
                # Convert relative URL to absolute
                absolute_url = urljoin(base_url, href)
                # Remove fragments
                absolute_url = absolute_url.split('#')[0]
                if absolute_url not in links:
                    links.append(absolute_url)

        print(f"Found {len(links)} navigation links")
        return links

    def process_page(self, soup):
        """
        Process a page: extract article.doc content and remove unwanted elements.

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            Tuple of (processed HTML content, page title) or (None, None) if article.doc not found
        """
        # Find the article.doc element
        article = soup.select_one('article.doc')

        if not article:
            print("Warning: article.doc not found on page")
            return None, None

        # Remove nav.pagination elements
        for pagination in article.select('nav.pagination'):
            pagination.decompose()

        # Remove div.feedback-form elements
        for feedback_form in article.select('div.feedback-form'):
            feedback_form.decompose()

        # Extract page title
        title_tag = soup.find('title')
        page_title = title_tag.string if title_tag else "Jmix Documentation"

        return str(article), page_title

    def wrap_in_html(self, content, title="Jmix Documentation"):
        """
        Wrap content in a valid HTML document structure.

        Args:
            content: HTML content to wrap
            title: Page title

        Returns:
            Complete HTML document string
        """
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>"""
        return html_template

    def get_path_and_filename_from_url(self, url):
        """
        Extract directory path and filename from URL.

        Args:
            url: URL to parse

        Returns:
            Tuple of (directory_path, filename)
        """
        parsed = urlparse(url)
        path = parsed.path

        # Remove base path prefix if present (e.g., /jmix/)
        if path.startswith('/jmix/'):
            path = path[6:]  # Remove '/jmix/'
        elif path.startswith('/jmix'):
            path = path[5:]  # Remove '/jmix'

        # Remove leading/trailing slashes
        path = path.strip('/')

        # Split into directory and filename
        if '/' in path:
            parts = path.split('/')
            filename = parts[-1]
            directory = '/'.join(parts[:-1])
        else:
            filename = path
            directory = ''

        # Handle cases where there's no filename or it's a directory
        if not filename or not '.' in filename:
            if filename:
                directory = os.path.join(directory, filename) if directory else filename
            filename = 'index.html'

        # Ensure .html extension
        if not filename.endswith('.html'):
            filename += '.html'

        return directory, filename

    def save_html(self, content, directory, filename):
        """
        Save HTML content to a file in the appropriate subdirectory.

        Args:
            content: HTML content to save
            directory: Subdirectory path relative to output_dir
            filename: Name of the file
        """
        # Create full directory path
        if directory:
            full_dir = os.path.join(self.output_dir, directory)
        else:
            full_dir = self.output_dir

        # Create directory if it doesn't exist
        Path(full_dir).mkdir(parents=True, exist_ok=True)

        # Save the file
        filepath = os.path.join(full_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            relative_path = os.path.join(directory, filename) if directory else filename
            print(f"Saved: {relative_path}")
        except Exception as e:
            print(f"Error saving {filepath}: {e}")

    def scrape(self):
        """Main scraping process."""
        print("Starting Jmix documentation scraper...")

        # Create output directory
        self.create_output_dir()

        # Start with intro.html
        intro_url = urljoin(self.base_url, 'intro.html')
        print(f"\nFetching initial page: {intro_url}")

        soup = self.fetch_page(intro_url)
        if not soup:
            print("Failed to fetch initial page. Exiting.")
            return

        # Extract navigation links
        nav_links = self.extract_nav_links(soup, self.base_url)

        if not nav_links:
            print("No navigation links found. Exiting.")
            return

        # Process each link
        print(f"\nProcessing {len(nav_links)} pages...")
        for i, url in enumerate(nav_links, 1):
            print(f"\n[{i}/{len(nav_links)}] Processing: {url}")

            # Fetch the page
            page_soup = self.fetch_page(url)
            if not page_soup:
                continue

            # Process the page
            processed_content, page_title = self.process_page(page_soup)
            if not processed_content:
                continue

            # Wrap content in valid HTML document
            html_document = self.wrap_in_html(processed_content, page_title)

            # Extract directory path and filename
            directory, filename = self.get_path_and_filename_from_url(url)

            # Save the file
            self.save_html(html_document, directory, filename)

            # Be nice to the server
            time.sleep(0.5)

        print(f"\n✓ Scraping completed! Files saved to: {self.output_dir}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape Jmix documentation and prepare it for Context7'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for scraped documentation'
    )
    parser.add_argument(
        '--base-url',
        default='https://docs.jmix.io/jmix',
        help='Base URL of Jmix documentation (default: https://docs.jmix.io/jmix)'
    )

    args = parser.parse_args()

    scraper = JmixDocsScraper(
        base_url=args.base_url,
        output_dir=args.output_dir
    )
    scraper.scrape()


if __name__ == "__main__":
    main()
