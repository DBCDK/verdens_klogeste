#!/usr/bin/env python3

import argparse
import json
import os
from verdens_klogeste.insert import fetch_metadata, setup
from verdens_klogeste.insert import insert as discovery_insert

def generator(filename):
    with open(filename, 'r') as f:
        for line in f:
            item = json.loads(line)
            yield item



            
def lprint(txt):
    print(txt, end='', flush=True)
    

def insert(filename, nlu, discovery, logfile, done_ids, tmp_dir='./tmp'):
    for i, item in enumerate(generator(filename)):
        docid = item['docid']
        if docid in done_ids:
            print(f'[{i}] Skipping id - already inserted: {docid}')
            continue
        title = item['title']
        lprint(f'[{i}] {title} - ')
        tmp_file = f'{tmp_dir}/{title}.txt'
        try:
            lprint(f'tmp-file')
            with open(tmp_file, 'w') as tf:
                tf.write(item['text'])
            lprint('..done ')
            lprint(f' metadata:{docid}')
            metadata = fetch_metadata(nlu, tmp_file, docid)
            lprint('..done')
            lprint(' discovery-insert')
            doc_info = discovery_insert(discovery, metadata, tmp_file)
            lprint('..done')
        except:
            print(f'\n\nAn error occured while processing: {docid}')
            log = {'docid': docid, 'status': 'ERROR'}
            json.dump(log, logfile)
            logfile.write('\n')
            continue
        lprint('  cleanup')
        os.remove(tmp_file)
        lprint('..done')
        lprint('  logging')
        log = {'docid': docid, 'metadata': metadata, 'docinfo': doc_info}
        json.dump(log, logfile)
        logfile.write('\n')
        print('..done')


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--if', dest='infile', required=True, help='infile')
    parser.add_argument('--tmp-dir', dest='tmpdir', required=True, help='tmp dir for writing files')
    parser.add_argument('--log-file', dest='logfile', required=True, help='file for logging progress')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cli()
    insert_done = False

    nlu, discovery = setup()
    done_ids = set()
    with open(args.logfile, 'r') as inlogfile:
        for line in inlogfile:
            d = json.loads(line)
            done_ids.add(d['docid'])
            #print(len(done_ids))
    with open(args.logfile, 'a') as logfile:
        insert(args.infile, nlu, discovery, logfile, done_ids)
    
            
