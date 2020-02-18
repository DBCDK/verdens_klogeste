#!/usr/bin/env python3

import os
from discovery import Discovery

def run(query):
    watson_discovery_apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    watson_discovery_url = os.environ['WATSON_DISCOVERY_URL']

    DISCOVERY_ENV_NAME = 'vktest_env'
    DISCOVERY_COLL_NAME = 'vktest_coll'
    
    discovery = Discovery(watson_discovery_apikey, watson_discovery_url)
    env_id = discovery.find_env_id(DISCOVERY_ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, DISCOVERY_COLL_NAME)
    response = discovery.discovery.query(env_id, coll_id, query=query)
    return response

    
if __name__ == '__main__':
    query = 'actor'
    response = run(query)
    print(response)
