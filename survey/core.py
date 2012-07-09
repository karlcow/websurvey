#!/usr/bin/env python2.7
# encoding: utf-8
"""
survey/core.py

Created by Karl Dubost on 2012-07-03.
Copyright (c) 2011 Grange. All rights reserved.
see LICENSE
"""

import urllib2
import urlparse
import requests
import StringIO
from lxml import etree
import cssutils


class UriCheck:
    """Some control about URIs from the file"""

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


class HttpRequests:
    """Servers behave depending on what is asking which URI"""

    def __init__(self):
        self.content = ""
        self.statuscode = ""

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

    def getContent(self, uri):
        r = requests.get(uri)
        return r.text


class Css:
    """Grabing All CSS for one given URI"""

    def __init__(self):
        self.htmltext = ""

    def getCssUriList(self, htmltext, uri):
        """Given an htmltext, get the list of linked CSS"""
        tree = etree.HTML(htmltext)
        sheets = tree.xpath('//link[@rel="stylesheet"]/@href')
        for i, sheet in enumerate(sheets):
            cssurl = urlparse.urljoin(uri, sheet)
            sheets[i] = cssurl
        return sheets


def main():
    TESTURI = 'http://www.opera.com/'
    req = HttpRequests()
    content = req.getContent(TESTURI)
    css = Css()
    print css.getCssUriList(content, TESTURI)

if __name__ == '__main__':
    main()
