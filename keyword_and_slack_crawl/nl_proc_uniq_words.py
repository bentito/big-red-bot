import logging
import random
import re
import string
import sys
from urllib.parse import urlparse, parse_qs

import nltk
from nltk.corpus import stopwords, words

# Initialize NLTK resources and extend stopwords
nltk.download('stopwords')
nltk.download('words')
english_stopwords = set(stopwords.words('english')) | set(words.words())


# Function to load technical computing terms
def load_tech_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return {word.strip().lower() for word in file}


# Function to clean and extract meaningful parts from URLs
def extract_url_words(url):
    parsed_url = urlparse(url)
    path_parts = re.split(r'\W+', parsed_url.path)
    query_parts = re.split(r'\W+', '&'.join(parse_qs(parsed_url.query).keys()))
    return {part.lower() for part in path_parts + query_parts if part}


# Function to process a single line
def process_line(line, tech_terms, output_words):
    words = set()
    for word in re.split(r'\b|\s|\W+\b|\b\W+', line.strip()):
        original_word = word  # Keep the original word for tech terms check
        word = word.lower()  # Normalize to lowercase
        if word and word not in english_stopwords and word not in output_words:
            if word.isdigit() or all(char in string.punctuation for char in word):
                continue  # Skip purely numeric or punctuation words
            if '_' in word and original_word not in tech_terms:
                words.update(word.split('_'))
            elif '-' in word and original_word not in tech_terms:
                words.update(word.split('-'))
            elif word in tech_terms or not word.isalpha():
                words.add(word)
            elif re.match(r'https?:\/\/', word):
                words.update(extract_url_words(word))
            else:
                words.add(word)
    return words


# Main processing function with parallel execution
def process_file_parallel(input_file, output_file, tech_terms):
    unique_words = set()
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        result = process_line(line, tech_terms, unique_words)
        for word in result:
            if word not in unique_words:  # Check to prevent duplicate prints
                print(word)  # Print each new word to stdout as found
                unique_words.add(word)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word in sorted(unique_words):
            file.write(word + '\n')
    return unique_words


def main():
    debug_mode = '--debug' in sys.argv
    logging.basicConfig(level=logging.DEBUG if debug_mode else logging.INFO)
    tech_terms = load_tech_terms('keyword_and_slack_crawl/data/computing_terms_list.txt')

    logging.info("Starting to process the words...")
    unique_words = process_file_parallel('keyword_and_slack_crawl/data/unique_words_list.txt',
                                         'keyword_and_slack_crawl/data/unique_words_list_proc.txt', tech_terms)
    logging.info("Finished processing. The processed file is 'unique_words_list_proc.txt'.")

    if debug_mode:
        sampled_words = random.sample(unique_words, min(20, len(unique_words)))
        logging.debug(f"Randomly sampled words: {sampled_words}")


if __name__ == "__main__":
    main()
