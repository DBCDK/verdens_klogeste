#!/usr/bin/env python3

import json
import csv
from operator import itemgetter

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            l = json.loads(line)
            if 'status' in l and l['status'] == 'ERROR':
                continue
            galeid = l['docid']
            title = l['metadata']['title']
            d = {'galeid': galeid, 'title': title}
            data.append(d)
    return data


def dump_json(dump_filename, data):
    with open(f'{dump_filename}.json', 'w') as f:
        json.dump(data, f)


def normalize(text):
    remove = '()"\''
    text = ''.join(c for c in text if c not in remove)
    return text


def dump_text(dump_filename, data):
    with open(f'{dump_filename}.txt', 'w') as f:
        # normalize
        triples = []
        for d in data:
            triple = (d['galeid'], d['title'], normalize(d['title']))
            triples.append(triple)
        sort_data = sorted(triples, key=itemgetter(2))
        for triple in sort_data:
            text = f'{triple[0]}\t{triple[1]}\n'
            f.write(text)


def dump_csv(dump_filename, data):
    with open(f'{dump_filename}.csv', 'w') as f:
        fieldnames = ['galeid', 'title']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        
            
def main(infile, dump_filename_without_extension):
    data = read_data(infile)
    dump_json(dump_filename_without_extension, data)
    dump_text(dump_filename_without_extension, data)
    dump_csv(dump_filename_without_extension, data)    

    
if __name__ == '__main__':
    # these could be made into cli-parameters.
    infile = 'gale-log.json'
    dump_filename_without_extension = 'gale_list'
    
    main(infile, dump_filename_without_extension)
