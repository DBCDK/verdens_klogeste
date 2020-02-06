#!/usr/bin/env python3

import argparse
import glob
import json
import os
from watson import Watson
from discovery import Discovery


def run(datadir):
    watson_nlu_apikey = os.environ['WATSON_NLU_APIKEY']
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_nlu_url = os.environ['WATSON_NLU_URL']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DICOVERY_ENV_NAME = 'vktest_env'
    DICOVERY_COLL_NAME = 'vktest_coll'

    watson_nlu_url += '/v1/analyze?version=2019-07-12'
    nlu = Watson(watson_nlu_apikey, watson_nlu_url)
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)

    filenames = glob.glob(f'{datadir}/*.txt')
    for filename in filenames:
        with open(filename, 'r') as infile:
            data = infile.read()
            metadata = nlu.query_watson_nlu(data)            
            #print(json.dumps(metadata))
        doc_info = discovery.upload_doc(filename, metadata, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME)
        print(doc_info)

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='datadir')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = cli()
    run(args.dir)

