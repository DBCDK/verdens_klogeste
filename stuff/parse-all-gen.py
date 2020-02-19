#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if __name__ == "__main__":
    for l in sys.stdin:
        src = l.rstrip()
        target = src.replace('json', 'txt') 
        print("./parse-response.py < %s > %s" % (src, target))



