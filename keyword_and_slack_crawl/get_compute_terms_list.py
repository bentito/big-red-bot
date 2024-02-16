#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# Base URL of the computer terms glossary
base_url = 'https://www.computerhope.com/'
index_url = base_url + 'jargon.htm'


def scrape_terms_from_letter_page(url):
    """Scrapes computing terms from a single alphabet page."""
    terms = []
    try:
        print(f"Fetching terms from: {url}")  # Debugging line
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming terms are listed directly within <a> tags in paragraphs or lists
        # This might need adjustment based on actual page content structure
        term_elements = soup.find_all('a', href=True)
        for term_element in term_elements:
            # Filter out non-jargon links; adjust as necessary
            if '/jargon/' in term_element['href']:
                term = term_element.get_text().strip()
                if term:
                    terms.append(term)

        # Debugging: Print out the first few terms to check
        print(f"First few terms from {url}: {terms[:5]}")  # Debugging line
    except requests.RequestException as e:
        print(f"Error scraping terms from {url}: {e}")
    return terms


def main():
    all_terms = []
    try:
        print(f"Fetching index page: {index_url}")  # Debugging line
        response = requests.get(index_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links for the jargon index pages
        alphabet_links = [link['href'] for link in soup.select('#atoz ul li a')]
        print(f"Alphabet links found: {alphabet_links}")  # Debugging line

        # Iterate over each alphabet page to scrape terms
        for link in alphabet_links:
            page_url = base_url + link
            terms = scrape_terms_from_letter_page(page_url)
            all_terms.extend(terms)
            print(f"Scraped {len(terms)} terms from {page_url}")

        # Remove duplicates and sort the terms
        unique_terms = sorted(set(all_terms))
        print(f"Total unique terms collected: {len(unique_terms)}")  # Debugging line

        # Save to file
        output_file = 'data/computing_terms_list.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            for term in unique_terms:
                file.write(f"{term}\n")

        print(f"Saved {len(unique_terms)} unique computing terms to {output_file}")

    except requests.RequestException as e:
        print(f"Error fetching index page {index_url}: {e}")


if __name__ == "__main__":
    main()
