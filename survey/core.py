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
import logging

# CONSTANT - ALL OF THESE will have to be passed as arguements.
# List of URIs, 1 URI by line
SITELIST = os.path.dirname(__file__) + "/../tests/urlist.data"
UAREF = "Opera/9.80 (Macintosh; Intel Mac OS X 10.7.4; U; fr) Presto/2.10.289 Version/12.00"
UATEST = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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
        """Return the content associated with an uri"""
        r = requests.get(uri)
        return r.text

    def parseHttpLink(self, linkhttpheader):
        """Link HTTP headers are a CSV list
        Link: <uri>; rel=next, <uri2>; rel=stylesheet
        {'next': 'uri', 'stylesheet': 'uri2'}
        TODO check the spec on Web Linking"""
        httplinkdict = {}
        linkitems = str.split(linkhttpheader, ',')
        for linkitem in linkitems:
            value = str.split(linkitem, ';')
            httplinkdict[value[0]] = value[1]
        return httplinkdict


class Css:
    """Grabing All CSS for one given URI"""

    def __init__(self):
        self.htmltext = ""

    def getCssUriList(self, htmltext, uri):
        """Given an htmltext, get the list of linked CSS"""
        cssurilist = []
        tree = etree.HTML(htmltext)
        csspathlist = tree.xpath('//link[@rel="stylesheet"]/@href')
        for i, csspath in enumerate(csspathlist):
            cssurl = urlparse.urljoin(uri, csspath)
            cssurilist.append(cssurl)
        return cssurilist

    def getCssHttpUriList(self, httpheadersdict, uri):
        """Given HTTP headers dictionary for a URI, extract the list of linked CSS"""
        # parse HTTP header for Link: <uri>;rel=stylesheet
        # requests returns something such as:
        # 'link': '</foo.css>;rel=stylesheet, </>;rel=next'
        # httplib might return a list of csv for a header.
        cssurilist = []
        req = HttpRequests()
        linkhttp = httpheadersdict['link']
        csspathlist = req.parseHttpLink(linkhttp)
        for i, csspath in enumerate(csspathlist):
            cssurl = urlparse.urljoin(uri, csspath)
            cssurilist.append(cssurl)
        return cssurilist

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

    def hasVendorProperty(self, vendorname, propertyname, declarationslist):
        """Given a declarationslist, a vendor name, and propertyname,
        verify that the the property name for this vendor name exists
        return True"""
        expectedproperty = "-%s-%s" % (vendorname, propertyname)
        propertynamelist = declarationslist.keys()
        try:
            propertynamelist.index(expectedproperty)
            return True
        except ValueError:
            return False

    def hasProperty(self, propertyname, declarationslist):
        """Given a declarationslist, a propertyname,
        verify that the the property name exists
        return True"""
        propertynamelist = declarationslist.keys()
        try:
            propertynamelist.index(propertyname)
            return True
        except ValueError:
            return False


def main():
    cssutils.log.setLevel(logging.FATAL)
    uc = UriCheck()
    req = HttpRequests()
    css = Css()
    with open(SITELIST) as f:
        for uri in f:
            # remove leading, trailing spaces
            uri = uri.strip()
            if uri.startswith("#"):
                continue
            if uc.ishttpURI(uri):
                htmltext = req.getContent(uri)
                # if css.hasStyleElement(htmltext):
                #     styleeltrule = css.getStyleElementRules(htmltext)
                #     if styleeltrule != "":
                #         logging.info("There is a style element at %s" % (uri))
                cssurislist = css.getCssUriList(htmltext, uri)
                for cssuri in cssurislist:
                    cssruleslist = css.getCssRules(cssuri)
                    for cssrule in cssruleslist:
                        if cssrule.type == 1:
                            # This is a rule, we process
                            # Reminder cssrule.type == 0 -> comment
                            score = 0
                            propertydetectedlist = []
                            propertyname = "transition"
                            if css.hasVendorProperty("o", propertyname, cssrule.style):
                                propertydetectedlist.append("-%s-%s" % ("o", propertyname))
                                score += 1
                            if css.hasVendorProperty("webkit", propertyname, cssrule.style):
                                propertydetectedlist.append("-%s-%s" % ("webkit", propertyname))
                                score += 2
                            if css.hasProperty(propertyname, cssrule.style):
                                propertydetectedlist.append("%s" % (propertyname))
                                score += 4
                            if score > 0:
                                print "SCORE: %d, LIST: %s At %s for %s, CSS: %s" % (score, propertydetectedlist, uri, propertyname, cssuri)
                            # for declaration in cssrule.style:
                            #     print declaration
                                # this is the property list -> rules.style
                                # I need to segregate each groups.
                                # if declaration.name.startswith("-webkit-"):
                                #     score = score + 1
                                # if declaration.name.startswith("-o-"):
                                #     score = score + 2
                        # if score != 0:
                        #     print score, rules.selectorText

                    # logging.info(responseheaders)

if __name__ == '__main__':
    main()
