#!/usr/bin/env python3

import argparse
import json
import os
import requests
import urllib.parse
from verdens_klogeste.insert import setup, fetch_metadata
from verdens_klogeste.wikipedia.fetch_links import write_to_dir


def main(article_filename, path):
    wiki_files_path = f'{path}/wikipedia'
    outpath = f'{path}/metadata'

    nlu, _ = setup()
    error_count = 0
    with open(article_filename, 'r') as infile:
        for i, line in enumerate(infile):
            articlename = urllib.parse.unquote(line.strip())
            article_first_letter = articlename[0]
            wiki_file_path = f'{wiki_files_path}/{article_first_letter}/{articlename}.txt'
            meta_path = f'{outpath}/{article_first_letter}'
            meta_file_path = f'{meta_path}/{articlename}.json'
            if os.path.isfile(meta_file_path):
                print(f'metadata exists: {articlename}')
                continue
            print(f'[{i}]: {articlename}')
            try:
                metadata = fetch_metadata(nlu, wiki_file_path)
            except requests.exceptions.HTTPError:
                print(f'Error (404) when fetching {articlename}')
                error_count += 1
                continue
            write_to_dir(json.dumps(metadata), meta_file_path, meta_path)
    if error_count:
        print(f'There where {error_count} error(s). You should rerun.')
            

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='article_filename', required=True, help='file containing article-names to get metadata for.')
    parser.add_argument('-p', dest='path', required=True, help='toplevel directory for data for discovery')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cli()
    main(args.article_filename, args.path)
