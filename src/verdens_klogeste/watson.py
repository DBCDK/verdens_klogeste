#!/usr/bin/env python3

import json

import requests

class Watson(object):
    def __init__(self, api_key, watson_url):
        self.api_key = api_key
        self.watson_url = watson_url

    def query_watson_nlu(self, text):
        data = {
            "text": text,
            "features": {
                "concepts": {
                    "limit": 10
                },
                "entities": {
                    "emotion": True,
                    "sentiment": True,
                    "limit": 10
                },
                "keywords": {
                    "sentiment": True,
                    "emotion": True,
                    "limit": 10
                },
            }
        }
        response = requests.post(self.watson_url, auth=("apikey", self.api_key),
            data=json.dumps(data).encode("utf8"),
            headers={"content-type": "application/json"})
        response.raise_for_status()
        return response.json()
