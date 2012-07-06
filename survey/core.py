#!/usr/bin/env python2.7
# encoding: utf-8
"""
survey/core.py

Created by Karl Dubost on 2012-07-03.
Copyright (c) 2011 Grange. All rights reserved.
see LICENSE
"""

import urllib2


class UriCheck:

    def __init__(self):
        self.uri = ""

    def ishttpURI(self, uri):
        req = urllib2.Request(uri)
        if req.get_type() in ['http', 'https']:
            return True
        else:
            return False


def main():
    pass

if __name__ == '__main__':
    pass
