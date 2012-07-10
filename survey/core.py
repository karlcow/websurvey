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


def main():
    TESTURI = 'http://lagrange.test.site/tmp/toto.html'
    req = HttpRequests()
    content = req.getContent(TESTURI)
    css = Css()
    cssutils.ser.prefs.lineNumbers = True
    cssutils.ser.prefs.resolveVariables = True
    cssurilist = css.getCssUriList(content, TESTURI)
    # for stylesheeturi in cssurilist:
    #     stylesheet = css.getCssRules(stylesheeturi)
    #     rules = (rule for rule in stylesheet if rule.type == rule.STYLE_RULE)
    #     for rule in rules:
    #         print rule.cssText

if __name__ == '__main__':
    main()
