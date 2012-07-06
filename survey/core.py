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
        """Given a URI,
        returns True if http or https
        returns False if not http or https"""
        req = urllib2.Request(uri)
        if req.get_type() in ['http', 'https']:
            return True
        else:
            return False

    def getRequest(self, uri, uastring):
        """Given a URI and a UA String,
        returns a list with uri, newlocation, statuscode, content"""
        # [uri, newlocation, statuscode,  content]
        pass

    def compareUriContent(self, uri1, uri2):
        """Given two URIs,
        compare if the content is the same."""
        # Useful when evolution along a parameter (time, uastring, etc.)
        pass


def main():
    pass

if __name__ == '__main__':
    pass
