#!/usr/bin/env python3

import argparse
import json
import logging

import tornado
from tornado.ioloop import IOLoop

import rrflow.utils
from dbc_pyutils import BaseHandler
from dbc_pyutils import StatusHandler
from dbc_pyutils import build_info

from .clustering import cluster

logger = rrflow.utils.setup_logging()

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    return parser.parse_args()

class QueryHandler(BaseHandler):
    def post(self):
        data = self.request.body.decode("utf8")
        n_results = self.get_argument("results-count", 50)
        clusters = cluster.query(data, n_results)
        response = {"clusters": clusters}
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
