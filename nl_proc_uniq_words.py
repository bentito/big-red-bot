#!/usr/bin/env python3
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import nltk

# Configuration
DEBUG = "--debug" in sys.argv
input_file = 'unique_words_list.txt'  # Update this path to your unique words list file
output_file = 'unique_words_list_proc.txt'  # Update this path to where you want the processed file

# Ensure NLTK resources are downloaded
nltk.download('words')
nltk.download('stopwords')

# Load NLTK resources
from nltk.corpus import words, stopwords


def load_nltk_resources():
    """Load resources from NLTK."""
    english_words = set(words.words())
    common_stopwords = set(stopwords.words('english'))
    return english_words, common_stopwords


def process_word(word, technical_terms, common_stopwords):
    """Clean and filter individual words."""
    # If the word looks like a file path (contains slashes but is not a URL), keep slashes
    if '/' in word and not re.match(r'https?://', word):
        cleaned_word = re.sub(r'[^a-zA-Z0-9/]', '', word).lower()  # Remove all but alphanumeric and slashes
    elif re.match(r'https?://', word):  # If the word is a URL, process accordingly
        try:
            parsed_url = urlparse(word)
            word = parsed_url.path.replace('-', ' ').strip()  # Retain slashes in URLs, replace other special characters
        except ValueError:
            word = re.sub(r'https?://|www\.', '', word).replace('-', ' ').strip()
        cleaned_word = re.sub(r'[^a-zA-Z0-9 ]', '', word).lower()  # Remove all but alphanumeric and space for URLs
    else:
        # For other text, remove punctuation and lowercase
        cleaned_word = re.sub(r'[!\"#$%&\'()*+,./:;<=>?@\[\\\]^_`{|}~]', '', word).lower()

    # Retain the word if it's a technical term or not a common English word
    return cleaned_word if cleaned_word not in common_stopwords or cleaned_word in technical_terms else None


def main():
    # Load English dictionary and common stopwords
    english_words, common_stopwords = load_nltk_resources()
    technical_terms = english_words - common_stopwords  # Presumed technical terms

    # Read the unique words from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        original_words = [line.strip() for line in f]

    total_words = len(original_words)
    processed_words = []

    # Set up ThreadPoolExecutor to use multiple threads
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_word = {executor.submit(process_word, word, technical_terms, common_stopwords): word for word in
                          original_words}

        for future in as_completed(future_to_word):
            processed_word = future.result()
            if processed_word:
                processed_words.append(processed_word)
            sys.stdout.write(f"\rProcessing word {len(processed_words)}/{total_words}")
            sys.stdout.flush()

    if DEBUG:
        # Print out 20 random words for debugging
        sample_words = random.sample(processed_words, min(20, len(processed_words)))
        print("\nSample processed words:", sample_words)
    else:
        # Write the processed, unique words to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in processed_words:
                f.write(f"{word}\n")
        print(f"\nCompleted: Processed and unique words written to {output_file}")


if __name__ == "__main__":
    main()
