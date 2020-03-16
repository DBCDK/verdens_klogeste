#!/usr/bin/env python3

import argparse
import os.path
from pathlib import Path
import time
import urllib.parse
import wikipediaapi


def fetch_wiki_page(page_name):
    """
    Takes a page name as in the wikipedia-url (with underscores)
    Returns the raw text stripped for tags and delimiters (except \n)
    """
    wiki = wikipediaapi.Wikipedia('simple')
    page = wiki.page(page_name)
    # remove empty lines:
    lines = page.text.split('\n')
    text = '\n'.join([line for line in lines if line.split()])
    return text


def write_to_dir(text, filepath, path):
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as out_file:
        out_file.write(text)
    

def main(input_filename, output_directory, sleep_time=1):
    with open(input_filename, 'r') as infile:
        for i, line in enumerate(infile):
            article_name = urllib.parse.unquote(line.strip())
            # Setting up the path as: {path}/{first_letter_of_article_name}/
            path = f'{output_directory}/{article_name[0]}'
            filepath = f'{path}/{article_name}.txt'
            # ignore if file already exists:
            if os.path.isfile(filepath):
                print(f'Article exists: {article_name}')
                continue
            print(f'[{i}]: {article_name}')
            text = fetch_wiki_page(article_name)
            write_to_dir(text, filepath, path)
            # Courtesy sleep to not seem to pushy.
            time.sleep(sleep_time)
            

def cli():
    parser = argparse.ArgumentParser('Fetches wikipedia articles from a file containing article names')
    parser.add_argument('-f', dest='links_filename', required=True, help='File containing article names. One name per line.')
    parser.add_argument('-o', dest='output_dir', default='wiki_data', help='Output directory for fetched files.')
    args = parser.parse_args()
    return args


if __name__== '__main__':
    args = cli()
    main(args.links_filename, args.output_dir)
