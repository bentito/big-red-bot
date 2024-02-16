#!/usr/bin/env python3
import csv
import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3
import sys


def fetch_cookies_for_domain(db_path, domain):
    """Fetch cookies for a specific domain from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, value FROM moz_cookies WHERE host LIKE ?", ('%' + domain,))
    cookies = {name: value for name, value in cur.fetchall()}
    conn.close()
    return cookies


def fetch_and_parse_url(url, cookies):
    try:
        response = requests.get(url, cookies=cookies, timeout=10)
        response.encoding = response.apparent_encoding  # Determine apparent encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True).lower()
        words = set(text.split())
        return words
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()


def save_unique_words(words, output_file):
    with open(output_file, 'a+', encoding='utf-8') as file:
        file.seek(0)
        existing_words = set(word.strip() for word in file)
        new_words = words - existing_words
        for word in new_words:
            try:
                file.write(word + '\n')
            except UnicodeEncodeError:
                print(f"Failed to encode word: {word}")
    return len(new_words) + len(existing_words)


def get_total_urls(input_csv):
    with open(input_csv, 'r', encoding='utf-8') as file:
        return sum(1 for row in csv.reader(file)) - 1  # Exclude header


def main(debug=False):
    db_path = "../cookies_firefox_copy.sqlite"
    domain = "redhat.com"
    input_csv = "./the_source_de_duped_results.csv"
    output_file = "data/unique_words_list.txt"
    total_urls = get_total_urls(input_csv)
    current_url_number = 0

    # Fetch cookies for the specified domain
    cookies = fetch_cookies_for_domain(db_path, domain)

    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_url_number += 1
            url = row['URL']
            words = fetch_and_parse_url(url, cookies)
            if debug:
                print("Debug mode: URL processed -", url)
                print("First 10 words found:", list(words)[:10])
                break  # Exit after processing the first URL
            else:
                word_count = save_unique_words(words, output_file)
                # Use '\r' to return to the start of the line and 'end' to avoid newline
                sys.stdout.write(f"\rCrawling ({current_url_number}/{total_urls}): {url} - Current word count: {word_count} - Progress: {current_url_number}/{total_urls}")
                sys.stdout.flush()
                time.sleep(random.uniform(0.5, 2.0))  # Be polite with delay

            if debug:
                break  # Exit after the first URL in debug mode

    if not debug:
        print("\nCompleted crawling and word collection.")


if __name__ == "__main__":
    debug_flag = "--debug" in sys.argv
    main(debug=debug_flag)
