#!/usr/bin/env python3
import os
import subprocess


def main():
    base_path = '../keyword_and_slack_crawl/data/slack_search_manually'
    output_base_path = '../data/external/olm/docs/Slack'
    os.makedirs(output_base_path, exist_ok=True)  # Create the output directory if it doesn't exist

    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            md_file_name = f"{dir_name}.md"
            md_file_path = os.path.join(output_base_path, md_file_name)
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(f"## Question\n{dir_name}\n\n### Answer\n")
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)
                    if file_name.endswith('.txt') or file_name.endswith('.yml'):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            md_file.write(f"\n```yaml\n{file.read()}\n```\n")
                    else:
                        # Use strings for non-text files
                        try:
                            strings_output = subprocess.check_output(['strings', file_path], universal_newlines=True)
                            md_file.write(f"\n```\n{strings_output}\n```\n")
                        except Exception as e:
                            md_file.write(f"\nError processing file {file_name}: {e}\n")


if __name__ == '__main__':
    main()
