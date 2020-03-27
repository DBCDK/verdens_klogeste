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

logger = rrflow.utils.setup_logging()

AUTHKEY = os.environ["AUTHKEY"]

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    return parser.parse_args()

class QueryHandler(BaseHandler):
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
        response = cluster.query(query, n_results, n_clusters)
        #response = {"clusters": clusters}
        self.write(f"{json.dumps(response)}\n")

def main():
    args = setup_args()
    info = build_info.get_info("verdens_klogeste")
    tornado_app = tornado.web.Application([
        ("/query", QueryHandler),
        ("/status", StatusHandler, {"ab_id": 1, "info": info}),
    ])
    tornado_app.listen(args.port)
    IOLoop.current().start()
