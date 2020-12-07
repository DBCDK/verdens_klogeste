#!/usr/bin/env python3

import json
import os
from discovery import Discovery
import sys

def warn(*args):
    print(*args, file=sys.stderr)
    sys.stderr.flush()

def similar(id_='cb01b8a0-d7a3-46c4-acfe-193676483c77'):
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DISCOVERY_ENV_NAME = 'vktest_env'
    DISCOVERY_COLL_NAME = 'vkgale_coll'
    
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)
    env_id = discovery.find_env_id(DISCOVERY_ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, DISCOVERY_COLL_NAME)
    response = discovery.discovery.query(env_id, coll_id, similar=True, similar_document_id=id_)
    return response

def parse(response, f):
    results = response['result']['results']
    for i, r in enumerate(results):
        print("="* 40, file=f)
        print(i+1, r["metadata"]["title"], file=f)
        for k in r["metadata"]["keywords"]:
            print("\t", k, file=f)


    
if __name__ == '__main__':
    id_ = os.environ['ID']
    #warn("query", query)
    response = similar()
    json_file = "%s.json" % (id_) 
    with open(json_file, 'w') as F:
        F.write(str(response))
    with open(json_file) as F:
        doc = json.load(F)
    with open("%s.txt" % id_, 'w') as F:
        parse(doc, F)
