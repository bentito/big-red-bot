#!/usr/bin/env python3
import csv
from bs4 import BeautifulSoup


def extract_urls_from_html(input_file_path):
    # Define the output CSV file path
    output_file_path = input_file_path.replace('.html', '_url.csv')

    # Read the HTML content
    with open(input_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract URLs from <a> tags
    urls = [a['href'] for a in soup.find_all('a', href=True)]

    # Write URLs to a CSV file
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL'])  # Write header
        for url in urls:
            writer.writerow([url])

    print(f"URLs extracted to {output_file_path}")


def main():
    input_file_path = "/Users/btofel/Downloads/The_Source_search_results_rhel_webpg.html"
    extract_urls_from_html(input_file_path)


if __name__ == "__main__":
    main()
