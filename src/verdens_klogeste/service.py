#!/usr/bin/env python3

import argparse
import json
import logging
import os

import tornado
from tornado.ioloop import IOLoop

import rrflow.utils
from dbc_pyutils import BaseHandler
from dbc_pyutils import StatusHandler
from dbc_pyutils import build_info

from .clustering import cluster

from verdens_klogeste.insert import setup, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME

logger = rrflow.utils.setup_logging()

AUTHKEY = os.environ["AUTHKEY"]

_, discovery = setup()
env_id = discovery.find_env_id(DICOVERY_ENV_NAME)
coll_id = discovery.find_coll_id(env_id, DICOVERY_COLL_NAME)
disc = {'discovery': discovery, 'env_id': env_id, 'coll_id': coll_id}



def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument("--fake-gale-file", default='./src/verdens_klogeste/data/gale-fake-data.json')
    return parser.parse_args()

class QueryHandler(BaseHandler):

    def initialize(self, gale_fake_data):
        self.gale_fake_data = gale_fake_data

    def insert_fake_data(self, response):
        for result in response['results']:
            logger.info(result['metadata'])
            if 'metadata' in result and 'docid' in result['metadata']:
                docid = result['metadata']['docid']
                if docid in self.gale_fake_data:
                    result['metadata']['gale'] = self.gale_fake_data[docid]
        return response

    def post(self):
        data = json.loads(self.request.body.decode("utf8"))
        if "query" not in data or "key" not in data:
            self.set_status(415)
            return self.write("Request body must contain a \"query\" and a \"key\" key.")
        query = data["query"]
        key = data["key"]
        if key != AUTHKEY:
            return self.set_status(401)
        n_results = int(self.get_argument("results-count", 50))
        n_clusters = int(self.get_argument("num-clusters", 3))
        response = cluster.query(query, disc, n_results, n_clusters)
        response = self.insert_fake_data(response)
        #response = {"clusters": clusters}
        self.write(f"{json.dumps(response)}\n")

def main():
    args = setup_args()
    info = build_info.get_info("verdens_klogeste")
    logger.info('Loading fake-gale-data')
    with open(args.fake_gale_file) as galefile:
        gale_fake_data = json.load(galefile)

    tornado_app = tornado.web.Application([
        ("/query", QueryHandler, {'gale_fake_data': gale_fake_data}),
        ("/status", StatusHandler, {"ab_id": 1, "info": info}),
    ])
    tornado_app.listen(args.port)
    IOLoop.current().start()
