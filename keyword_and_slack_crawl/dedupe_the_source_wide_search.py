#!/usr/bin/env python3
import csv


def is_valid_url(url):
    """Basic validation to check if a URL is valid."""
    return url.startswith('http://') or url.startswith('https://')


def de_duplicate_csv_files(csv_files, output_file):
    unique_urls = set()
    entries = []

    # Process each file
    for file_path in csv_files:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            initial_count = 0
            for row in reader:
                initial_count += 1
                url = row['URL']
                if url not in unique_urls and is_valid_url(url):
                    unique_urls.add(url)
                    entries.append(row)
            print(f"Processed {file_path}: {initial_count} lines")

    # Write unique entries to a new file
    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        if entries:
            fieldnames = ['URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow({'URL': entry['URL']})

    print(f"Total unique entries written to {output_file}: {len(entries)}")


def main():
    csv_files = [
        "/Users/btofel/Downloads/The_Source_search_results_openshift_webpg_url.csv",
        "/Users/btofel/Downloads/The_Source_search_results_rhel_webpg_url.csv",
        "/Users/btofel/Downloads/The_Source_search_results_the_webpg_url.csv"
    ]

    output_file = "../the_source_de_duped_results.csv"
    de_duplicate_csv_files(csv_files, output_file)


if __name__ == "__main__":
    main()
