#!/usr/bin/env python3


import json
import os
import requests

from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class Discovery():

    def __init__(self, api_key, watson_url, version='2019-04-30'):
        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version=version,
            authenticator=authenticator
        )
        discovery.set_service_url(watson_url)
        self.discovery = discovery

    def create_env(self, name, description):
        env_info = self.discovery.create_environment(name=name, description=description)
        return env_info

    def create_collection(self, env_id, name):
        # if we dont give a configuration_id the default configuration will be used.
        coll_info = self.discovery.create_collection(env_id, name)
        return coll_info

    def find_env_id(self, name):
        env_id = ''
        envs = self.discovery.list_environments()
        for env in envs.result['environments']:
            if env['name'] == name:
                env_id = env['environment_id']
        return env_id

    def find_coll_id(self, env_id, name):
        coll_id = ''
        colls = self.discovery.list_collections(env_id)
        for coll in colls.result['collections']:
            if coll['name'] == name:
                coll_id = coll['collection_id']
        return coll_id

    def upload_doc(self, filename, metadata, env_name, coll_name):
        env_id = self.find_env_id(env_name)
        coll_id = self.find_coll_id(env_id, coll_name)
        with open(filename, 'r') as f:
            add_doc = self.discovery.add_document(
                env_id,
                coll_id,
                file=f,
                file_content_type='text/html',
                metadata=json.dumps(metadata),
            ).get_result()
        return add_doc

    def delete_doc(self, doc_id, env_name, coll_name):
        env_id = self.find_env_id(env_name)
        coll_id = self.find_coll_id(env_id, coll_name)
        response = self.discovery.delete_document(env_id, coll_id, doc_id)
        return response
        
    def setup_env_coll(self, env_name, env_description, coll_name):
        env_info = self.create_env(env_name, env_description)
        print(env_info)
        env_id = self.find_env_id(env_name)
        coll_info = self.create_collection(env_id, coll_name)
        print(coll_info)

    def delete_coll(self, env_name, coll_name):
        env_id = self.find_env_id(env_name)
        coll_id = self.find_coll_id(env_id, coll_name)
        self.discovery.delete_collection(env_id, coll_id)

def chain(url, apikey, version):
    
    ENV_NAME = 'vktest_env'
    COLL_NAME = 'vktest_coll'
    DOC_FILENAME = 'data/Sean_Astin.txt'
    ENV_DESC = 'Environment til Verdens Klogeste test'
    # NOTICE: Watson Discovery does not accept documents in txt-format
    # The document has just been renamed to .html in order to be accepted.

    discovery = Discovery(apikey, url)

    # discovery.delete_coll(ENV_NAME, COLL_NAME)

    # UNCOMMENT TO SETUP
    # discovery.setup_env_coll(ENV_NAME, ENV_DESC, COLL_NAME)
    # OR TO ONLY CREATE COLL:
    # env_id = discovery.find_env_id(ENV_NAME)
    # discovery.create_collection(env_id, COLL_NAME)

    # UNCOMMONT TO UPLOAD DOCUMENT
    #doc_info = discovery.upload_doc(DOC_FILENAME, ENV_NAME, COLL_NAME)
    #print(doc_info)

    # doc_id = '480ddd55-9bd4-4e3b-a35e-40c54b3bd0c1'
    env_id = discovery.find_env_id(ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, COLL_NAME)
    result = discovery.discovery.query(env_id, coll_id, query='Sean')
    print(result)


    
if __name__ == '__main__':
    apikey = os.environ['WATSON_DISCOVERY_APIKEY']
    url = 'https://api.eu-de.discovery.watson.cloud.ibm.com/instances/bf6c71cc-bd28-4cb1-9883-8dae849e7bd7'
    version = '2019-04-30'
    chain(url, apikey, version)
