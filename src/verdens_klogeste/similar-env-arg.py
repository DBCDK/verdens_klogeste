#!/usr/bin/env python3

import json
import os
from discovery import Discovery
import sys

def warn(*args):
    print(*args, file=sys.stderr)
    sys.stderr.flush()



    
def similar(id_):

    # similarity API explained her
    # https://cloud.ibm.com/docs/discovery?topic=discovery-query-concepts#doc-similarity
    
    # python API:
    # http://watson-developer-cloud.github.io/python-sdk/v4.7.1/apis/ibm_watson.discovery_v1.html
    
    warn("similar, id", id_)
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DISCOVERY_ENV_NAME = 'vktest_env'
    DISCOVERY_COLL_NAME = 'vkgale_coll'
    
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)
    env_id = discovery.find_env_id(DISCOVERY_ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, DISCOVERY_COLL_NAME)
    response = discovery.discovery.query(env_id, coll_id, similar=True, similar_document_ids=id_)
    return response


    
def test(q='trump'):
    # similarity API explained her
    # https://cloud.ibm.com/docs/discovery?topic=discovery-query-concepts#doc-similarity
    
    # python API:
    # http://watson-developer-cloud.github.io/python-sdk/v4.7.1/apis/ibm_watson.discovery_v1.html
    
    warn("similar, id", id_)
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DISCOVERY_ENV_NAME = 'vktest_env'
    DISCOVERY_COLL_NAME = 'vkgale_coll'
    
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)
    env_id = discovery.find_env_id(DISCOVERY_ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, DISCOVERY_COLL_NAME)
    response = discovery.discovery.query(env_id, coll_id, query=q)
    return response


def parse(response, f):
    results = response['result']['results']
    for i, r in enumerate(results):
        print("="* 40, file=f)
        print(i+1, r["metadata"]["title"], file=f)
        print("id:", r["id"], file=f)
        for k in r["metadata"]["keywords"]:
            print("\t", k, file=f)

    
if __name__ == '__main__':
    # pick id from env
    # like:
    # export ID=9b329410-a813-43f2-87b5-dab53ba0d00a 
    id_ = os.environ['ID']
    warn("main, id is", id_)

    # query watson for similar documents:
    response = similar(id_)
    #response = test()

    # save response as json (note str-hack to force json)
    json_file = "%s.json" % (id_)
    warn("save response as", json_file)
    with open(json_file, 'w') as F:
        F.write(str(response))
    
    # we re-read response to force json doc for easy parsing
    with open(json_file) as F:
        doc = json.load(F)

    # and write parsed document to txt-file
    with open("%s.txt" % id_, 'w') as F:
        parse(doc, F)
