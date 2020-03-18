#!/usr/bin/env python3


import argparse
import json
import os
import urllib.parse
import time
from verdens_klogeste.insert import setup, insert
from verdens_klogeste.wikipedia.fetch_links import write_to_dir


def read_metadata(meta_file_path):
    with open(meta_file_path, 'r') as f:
        return json.load(f)
    

def main(article_filename, path):
    wiki_files_path = f'{path}/wikipedia'
    meta_files_path = f'{path}/metadata'
    outpath = f'{path}/discovery'
    _, discovery = setup()
    errors = False
    with open(article_filename, 'r') as infile:
        for i, line in enumerate(infile):
            articlename = urllib.parse.unquote(line.strip())
            article_first_letter = articlename[0]
            wiki_file_path = f'{wiki_files_path}/{article_first_letter}/{articlename}.txt'
            meta_file_path = f'{meta_files_path}/{article_first_letter}/{articlename}.json'
            if not os.path.isfile(meta_file_path):
                print(f'No metadata exists: {articlename}')
                continue
            discovery_path = f'{outpath}/{article_first_letter}'
            discovery_file_path = f'{outpath}/{article_first_letter}/{articlename}.json'
            if os.path.isfile(discovery_file_path):
                print(f'discovery exists: {articlename}')
                continue
            metadata = read_metadata(meta_file_path)
            with open(wiki_file_path, 'r') as infile:
                data = infile.read()
            document_size = len(data)
            if document_size < 1024:
                print(f'Document size to small for {articlename} ({document_size})')
                continue
            print(f'[{i}]: {articlename}')
            #print(metadata)
            try:
                discovery_data = insert(discovery, metadata, wiki_file_path)
            except:
                print(f'Error when inserting document: {articlename}')
                errors = True
                print('Sleeping')
                time.sleep(5)
                continue
            write_to_dir(json.dumps(discovery_data), discovery_file_path, discovery_path)
    if errors:
        print('There where errors. You should rerun')


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='article_filename', required=True, help='file containing article-names to get metadata for.')
    parser.add_argument('-p', dest='path', required=True, help='toplevel directory for data for discovery')
    #parser.add_argument('--wiki_path', dest='wiki_files_path', required=True, help='Directory containing wikipedia text-files')
    #parser.add_argument('--meta_path', dest='meta_files_path', required=True, help='Directory containing metadata json-files')
    #parser.add_argument('--outpath', required=True, help='Path to where discovery-json-files are written.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cli()
    #main(args.article_filename, args.wiki_files_path, args.meta_files_path, args.outpath)
    main(args.article_filename, args.path)
