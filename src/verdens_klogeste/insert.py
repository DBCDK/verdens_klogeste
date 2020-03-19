#!/usr/bin/env python3

import argparse
import glob
import json
import os
from verdens_klogeste.watson import Watson
from verdens_klogeste.discovery import Discovery


DICOVERY_ENV_NAME = 'vktest_env'
DICOVERY_COLL_NAME = 'vktest_coll'

def setup():
    watson_nlu_apikey = os.environ['WATSON_NLU_APIKEY']
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_nlu_url = os.environ['WATSON_NLU_URL']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DICOVERY_ENV_NAME = 'vktest_env'
    DICOVERY_COLL_NAME = 'vktest_coll'

    watson_nlu_url += '/v1/analyze?version=2019-07-12'
    nlu = Watson(watson_nlu_apikey, watson_nlu_url)
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)
    return nlu, discovery


def fetch_text(d, entity):
    res = [x['text'] for x in d[entity]]
    return res
        

def create_neo_meta(metadata, filename):
    keywords = fetch_text(metadata, 'keywords')
    concepts = fetch_text(metadata, 'concepts')
    entities = fetch_text(metadata, 'entities')

    neo_meta = {'keywords': keywords, 'concepts': concepts, 'entitites': entities}
    doc_title = filename.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    neo_meta['url'] = f'https://simple.wikipedia.org/wiki/{doc_title}'
    return neo_meta
                            

def fetch_metadata(nlu, filename):
    with open(filename, 'r') as infile:
        data = infile.read()
        metadata = nlu.query_watson_nlu(data)            
        #print(json.dumps(metadata))
    return create_neo_meta(metadata, filename)


def insert(discovery, metadata, filename):
        doc_info = discovery.upload_doc(filename, metadata, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME)
        return doc_info

    
def run(datadir):
    nlu, discovery = setup()
    
    filenames = glob.glob(f'{datadir}/*.txt')
    for filename in filenames:
        metadata = fetch_metadata(nlu, filename)
        print(doc_info)

        
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='datadir')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = cli()
    run(args.dir)

