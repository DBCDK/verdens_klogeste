#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def plist(name, l):
    #print("-"* 80)
    print("## %s" % (name))
    for e in l:
        print("*", e)
    
if __name__ == "__main__":
    s = sys.stdin.read()
    doc = json.loads(s)
    results = doc['result']['results']
    for i, r in enumerate(results):
        #print("-"* 80)
        print("# [%d]" % (i+1), r["extracted_metadata"]["filename"])
        entities = r['enriched_text']["entities"]
        plist("Entities", [e['text'] for e in entities[:5]])
        concepts = r['enriched_text']["concepts"]
        plist("Concepts", [e['text'] for e in concepts[:5]])
        keywords = r['metadata']["keywords"]
        plist("Keywords", [e['text'] for e in keywords[:5]])
        cats = r['enriched_text']["categories"]
        plist("Categories", [e['label'] for e in cats[:5]])
        
