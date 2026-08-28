#!/usr/bin/env python3
"""
Data Scraper – Internship Submission
Author: Suresh Das
Date: 2026-08-28

Description:
    Scrapes quotes, authors, and tags from http://quotes.toscrape.com
    and saves the data to a CSV file.

Features:
    - Pagination support (scrapes multiple pages)
    - Respectful delays (1 second between requests)
    - User‑Agent spoofing to avoid blocking
    - Retry mechanism for transient failures
    - Command‑line arguments for flexibility
    - Error handling for network/parsing issues
    - Saves to CSV with proper quoting

Usage:
    python scraper.py --url http://quotes.toscrape.com --output quotes.csv --pages 5
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import argparse
import sys
from typing import List, Dict, Optional
from urllib.parse import urljoin


class QuoteScraper:
    """
    A web scraper that extracts quotes from quotes.toscrape.com.
    Handles pagination, retries, and data extraction.
    """

    BASE_URL = "http://quotes.toscrape.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    REQUEST_TIMEOUT = 10
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2
    REQUEST_DELAY = 1  # seconds between requests (be polite)

    def __init__(self, start_url: str = BASE_URL):
        self.start_url = start_url
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch the HTML content of a URL and return a BeautifulSoup object.
        Implements retry logic on failure.
        """
        for attempt in range(1, self.RETRY_ATTEMPTS + 1):
            try:
                response = self.session.get(url, timeout=self.REQUEST_TIMEOUT)
                response.raise_for_status()
                return BeautifulSoup(response.text, "lxml")
            except (requests.RequestException, ConnectionError) as e:
                print(f"⚠️ Attempt {attempt} failed for {url}: {e}")
                if attempt < self.RETRY_ATTEMPTS:
                    time.sleep(self.RETRY_DELAY * attempt)
                else:
                    print(f"❌ Failed to fetch {url} after {self.RETRY_ATTEMPTS} attempts.")
                    return None
        return None

    def parse_page(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract quotes, authors, and tags from a single page.
        Returns a list of dictionaries.
        """
        quotes_data = []
        quote_divs = soup.find_all("div", class_="quote")
        for quote in quote_divs:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            quotes_data.append({
                "quote": text,
                "author": author,
                "tags": ", ".join(tags)  # store as comma‑separated string
            })
        return quotes_data

    def scrape(self, max_pages: int = 10) -> List[Dict[str, str]]:
        """
        Scrape up to `max_pages` from the start URL (including pagination).
        Returns a list of all quote dictionaries.
        """
        all_quotes = []
        current_url = self.start_url
        page_count = 0

        while current_url and page_count < max_pages:
            print(f"📄 Scraping page {page_count + 1}: {current_url}")
            soup = self.fetch_page(current_url)
            if not soup:
                break

            # Extract data from current page
            page_data = self.parse_page(soup)
            all_quotes.extend(page_data)
            print(f"   Found {len(page_data)} quotes on this page.")

            # Check for "Next" button
            next_tag = soup.find("li", class_="next")
            if next_tag and next_tag.find("a"):
                next_url = next_tag.find("a")["href"]
                current_url = urljoin(self.start_url, next_url)
            else:
                current_url = None  # no more pages

            page_count += 1
            # Be polite: delay before next request
            if current_url and page_count < max_pages:
                time.sleep(self.REQUEST_DELAY)

        print(f"✅ Total quotes scraped: {len(all_quotes)}")
        return all_quotes

    def save_to_csv(self, data: List[Dict[str, str]], filename: str) -> None:
        """
        Write the scraped data to a CSV file with headers.
        """
        if not data:
            print("⚠️ No data to save.")
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
                writer.writeheader()
                writer.writerows(data)
            print(f"💾 Data saved to {filename}")
        except IOError as e:
            print(f"❌ Failed to write CSV: {e}")
            sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape quotes from quotes.toscrape.com and save to CSV."
    )
    parser.add_argument(
        "--url",
        default=QuoteScraper.BASE_URL,
        help=f"Starting URL (default: {QuoteScraper.BASE_URL})"
    )
    parser.add_argument(
        "--output",
        default="quotes.csv",
        help="Output CSV file name (default: quotes.csv)"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Maximum number of pages to scrape (default: 10)"
    )
    args = parser.parse_args()

    scraper = QuoteScraper(start_url=args.url)
    data = scraper.scrape(max_pages=args.pages)
    scraper.save_to_csv(data, args.output)


if __name__ == "__main__":
    main()