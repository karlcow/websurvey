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
from lxml import etree
import cssutils
import os.path

# CONSTANT - ALL OF THESE will have to be passed as arguements.
# List of URIs, 1 URI by line
SITELIST = os.path.dirname(__file__) + "/../tests/urlist.data"
UAREF = "Opera/9.80 (Macintosh; Intel Mac OS X 10.7.4; U; fr) Presto/2.10.289 Version/12.00"
UATEST = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"


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
        headers = {'User-Agent': uastring}
        r = requests.get(uri, headers=headers)
        statuscode = r.status_code
        responseheaders = r.headers
        history = r.history
        return statuscode, responseheaders, history

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

    def getCssRules(self, uri):
        """Given the URI of a CSS file,
        return the list of all CSS rules,
        including all the imports."""
        stylesheet = cssutils.parseUrl(uri)
        stylesheet = cssutils.resolveImports(stylesheet)
        return stylesheet

    def hasStyleElement(self, htmltext):
        """Given an htmltext,
        check if the style element is available
        return True if yes"""
        tree = etree.HTML(htmltext)
        styleelements = tree.xpath('//style')
        if not styleelements:
            return False
        else:
            return True

    def getStyleElementRules(self, htmltext):
        """Given an htmltext,
        let's return the CSS rules contained in the content"""
        compiledstyle = ""
        tree = etree.HTML(htmltext)
        styleelements = tree.xpath('//style')
        for styleelt in styleelements:
            compiledstyle = compiledstyle + styleelt.text
        cssutils.ser.prefs.indentClosingBrace = False
        cssutils.ser.prefs.keepComments = False
        cssutils.ser.prefs.lineSeparator = u''
        cssutils.ser.prefs.omitLastSemicolon = False
        stylesheet = cssutils.parseString(compiledstyle)
        return stylesheet


def main():
    uc = UriCheck()
    req = HttpRequests()
    with open(SITELIST) as f:
        for uri in f:
            if uri.startswith("#"):
                continue
            if uc.ishttpURI(uri.strip()):
                (statuscode, responseheaders, history) = req.getRequest(uri, UATEST)
                for resp in history:
                    print resp.headers


if __name__ == '__main__':
    main()
