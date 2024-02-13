#!/usr/bin/env python3

def filter_uri_lines(input_file_path):
    # Define the output file path
    output_file_path = input_file_path.replace('.txt', '_uri.txt')

    # Open the input file and read lines
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Filter lines that start with "/"
    uri_lines = [line for line in lines if line.startswith('/')]

    # Write filtered lines to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(uri_lines)

    print(f"Filtered URIs written to {output_file_path}")


def main():
    input_file_path = "/Users/btofel/Downloads/The_Source_search_results_the_paste.txt"
    filter_uri_lines(input_file_path)


if __name__ == "__main__":
    main()
