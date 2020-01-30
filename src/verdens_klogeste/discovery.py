#!/usr/bin/env python3


import json
import os
import requests

from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def auth_discovery(url, apikey, version):

    authenticator = IAMAuthenticator(f'{apikey}')
    discovery = DiscoveryV1(
        version=f'{version}',
        authenticator=authenticator
    )

    discovery.set_service_url(f'{url}')
    return discovery

    
def create_env(discovery, name, description):
    env_info = discovery.create_environment(name=name, description=description)
    return env_info


def find_env_id(discovery, name):
    env_id = ''
    envs = discovery.list_environments()
    for env in envs.result['environments']:
        if env['name'] == name:
            env_id = env['environment_id']
    return env_id


def create_collection(discovery, env_id, name):
    # if we dont give a configuration_id the default configuration will be used.
    coll_info = discovery.create_collection(env_id, name)
    return coll_info


def find_coll_id(discovery, env_id, name):
    coll_id = ''
    colls = discovery.list_collections(env_id)
    for coll in colls.result['collections']:
        if coll['name'] == name:
            coll_id = coll['collection_id']
    return coll_id


def upload_doc(discovery, env_id, coll_id, doc_filename):
    with open(doc_filename) as fileinfo:
        add_doc = discovery.add_document(
            env_id,
            coll_id,
            file=fileinfo).get_result()
    return add_doc


def chain(url, apikey, version):
    
    ENV_NAME = 'vktest_env'
    COLL_NAME = 'vktest_coll'
    DOC_FILENAME = 'data/Sean_Astin.html'
    # NOTICE: Watson Discovery does not accept documents in txt-format
    # The document has just been renamed to .html in order to be accepted.

    discovery = auth_discovery(url, apikey, version)
    
    # UNCOMMENT TO CREATE ENVIRONMENT
    #env_info = create_env(discovery, ENV_NAME, 'Environment til Verdens Klogeste test')
    #print(env_info)
    
    # find vktest_env identifier:
    env_id = find_env_id(discovery, ENV_NAME)
    print(f'Environment id: {env_id}')

    # UNCOMMENT TO CREATE COLLECTION
    #coll_info = create_collection(discovery, env_id, COLL_NAME)
    #print(coll_info)

    coll_id = find_coll_id(discovery, env_id, COLL_NAME)
    print(f'Collection id:  {coll_id}')

    # UNCOMMONT TO UPLOAD DOCUMENT
    #doc_info = upload_doc(discovery, env_id, coll_id, DOC_FILENAME)
    #print(doc_info)

    # doc_id = '480ddd55-9bd4-4e3b-a35e-40c54b3bd0c1'
    result = discovery.query(env_id, coll_id, query='Sean')
    print(result)

    
if __name__ == '__main__':
    apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    url = 'https://api.eu-de.discovery.watson.cloud.ibm.com/instances/bf6c71cc-bd28-4cb1-9883-8dae849e7bd7'
    version = '2019-04-30'
    chain(url, apikey, version)
