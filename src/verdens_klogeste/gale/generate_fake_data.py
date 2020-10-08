#!/usr/bin/env python3

import argparse
import json
import random

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--inputfile', help='json-file used for inserting gale-documents into watson.')
    parser.add_argument('-g', '--galelist', help='json-file with list of galeids')
    return parser.parse_args()

def get_galeids(galelistfile):
    with open(galelistfile, 'r') as f:
        return set([e['galeid'] for e in json.load(f)])
    

def run(inputfile, galelistfile):
    random.seed(42)
    galeids = get_galeids(galelistfile)

    data = {}
    with open(inputfile, 'r') as f:
        for line in f:
            d = json.loads(line)
            gid = d['docid']
            if gid not in galeids:
                continue
            filename = d['filename']
            collection = filename.split('/')[3]
            data[gid] = {
                'gale-collection': collection,
                'gale-fake-level': random.randint(0,99),
                'gale-fake-waiting': random.randint(0,99),
            }
            
    print(f'#galeids: {len(galeids)}  #dict: {len(data)}')
    with open('gale-fake-data.json', 'w') as of:
        json.dump(data, of)
        
def main():
    args = cli()
    run(args.inputfile, args.galelist)

if __name__ == '__main__':
    main()
