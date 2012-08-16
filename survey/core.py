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
from datetime import datetime

# CONSTANT - ALL OF THESE will have to be passed as arguements.
# List of URIs, 1 URI by line
SITELIST = os.path.dirname(__file__) + "/../doc/urlist-top1000.data"
# SITELIST = os.path.dirname(__file__) + "/../tests/urlist.data"
# UAREF = "Opera/9.80 (Macintosh; Intel Mac OS X 10.8.0) Presto/2.12.363 Version/12.50"
UAREF = "Opera/9.80 (Android 2.3.5; Linux; Opera Mobi/ADR-1202082305; U; en) Presto/2.10.254 Version/12.00"
logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# UATEST = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"
logging.basicConfig(filename='log-survey.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
VENDORPREFIX = ['moz', 'ms', 'o', 'webkit']
PROPERTYTOCHECK = ['transition', 'transform', 'animation', 'background-size']


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

    def getContent(self, uri, useragentstring):
        """Return the content associated with an uri"""
        headers = {'User-Agent': useragentstring}
        r = requests.get(uri, headers=headers)
        # r.history contains a list of the different redirections
        # if needed later.
        finaluri = r.url
        responsetext = r.text
        # first test if it's a string
        try:
            isinstance(responsetext, basestring)
        # Log type errors
        except TypeError as e:
            logging.debug("getContent - %s - %s" % (uri, e.message))
        else:
            # then test if it's unicode and convert it
            if isinstance(responsetext, unicode):
                htmltext = responsetext.encode('utf-8')
            # or if not it is just the common text
            elif isinstance(responsetext, str):
                htmltext = responsetext
        return htmltext, finaluri


class Css:
    """Grabing All CSS for one given URI"""

    def __init__(self):
        self.htmltext = ""

    def getCssUriList(self, htmltext, uri):
        """Given an htmltext, get the list of linked CSS"""
        cssurilist = []
        myparser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(htmltext, parser=myparser)
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
        IMPORT_FLAG = False
        stylesheet = ""
        # requests is more robust for encoding errors
        headers = {'User-Agent': UAREF}
        r = requests.get(uri, headers=headers)
        stylesheet = cssutils.parseString(r.text)
        for cssrule in stylesheet:
            if cssrule.type == 3:
                IMPORT_FLAG = True
        # ResolveImports only if there is a rule
        if IMPORT_FLAG:
            stylesheet2 = cssutils.resolveImports(stylesheet)
        else:
            stylesheet2 = stylesheet
        return stylesheet2

    def hasStyleElement(self, htmltext):
        """Given an htmltext,
        check if the style element is available
        return True if yes"""
        myparser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(htmltext, parser=myparser)
        styleelements = tree.xpath('//style')
        if not styleelements:
            return False
        else:
            return True

    def getStyleElementRules(self, htmltext):
        """Given an htmltext,
        return the CSS rules contained in the content"""
        compiledstyle = ""
        stylesheet = cssutils.css.CSSStyleSheet()
        myparser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(htmltext, parser=myparser)
        styleelements = tree.xpath('//style')
        for styleelt in styleelements:
            if styleelt.text != None:
                compiledstyle = compiledstyle + styleelt.text
            else:
                logging.debug("STYLE ELEMENT %s on %s" % (styleelements.index(styleelt) + 1, len(styleelements)))
        if compiledstyle != None:
            cssutils.ser.prefs.indentClosingBrace = False
            cssutils.ser.prefs.keepComments = False
            cssutils.ser.prefs.lineSeparator = u''
            cssutils.ser.prefs.omitLastSemicolon = False
            try:
                stylesheet = cssutils.parseString(compiledstyle)
            except ValueError as e:
                logging.info("BOGUS STYLE RULE: %s" % (e.message))
        else:
            raise ValueError("STYLE ELEMENT: no CSS Rules")
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


class Survey:
    """Mother of survey modules"""

    def __init__(self):
        # TODO: Initializing the reporting output mode
        pass

    def compareCssProperties(self, vendorref, vendorcomp, propertyname, cssrule):
        """compares how CSS properties are used and computes a score
        vendorref  = +1
        vendorcomp = +2
        prefixless = +4

        Example:
        .sel {  -o-color: #fff;
              -moz-color: #fff;
                   color: #fff;}

        will return a score of 5
        with property = 'color', vendorref = 'o', vendorcomp = 'moz'
        """
        score = 0
        propertyvendorlist = []
        propertyvendorlist.append(propertyname)
        css = Css()
        if css.hasVendorProperty(vendorref, propertyname, cssrule):
            score += 1
            propertyvendorlist.append(vendorref)
        if css.hasVendorProperty(vendorcomp, propertyname, cssrule):
            score += 2
            propertyvendorlist.append(vendorcomp)
        if css.hasProperty(propertyname, cssrule):
            score += 4
            propertyvendorlist.append('prefixless')
        return score, propertyvendorlist

    def getVendorPrefixes(self, propertyname, cssrule):
        """It will return the list of vendor prefixes for this propertyname"""
        propertyvendorlist = []
        propertyvendorlist.append(propertyname)
        css = Css()
        for vendorref in VENDORPREFIX:
            if css.hasVendorProperty(vendorref, propertyname, cssrule):
                propertyvendorlist.append(vendorref)
        if css.hasProperty(propertyname, cssrule):
            propertyvendorlist.append('prefixless')
        return propertyvendorlist


def main():
    cssutils.log.setLevel(logging.FATAL)
    uc = UriCheck()
    req = HttpRequests()
    css = Css()
    survey = Survey()
    with open(SITELIST) as f:
        logging.info("START - %s with %s" % (datetime.today().isoformat(), UAREF))
        for uri in f:
            uri = uri.strip()
           # remove leading, trailing spaces
            if uri.startswith("#"):
                continue
            elif uri == '':
                continue
            logging.info("SITE: %s" % (uri))
            if uc.ishttpURI(uri):
                try:
                    htmltext, finaluri = req.getContent(uri, UAREF)
                    if css.hasStyleElement(htmltext):
                        styleeltrule = css.getStyleElementRules(htmltext)
                        if styleeltrule != "":
                            logging.info("STYLE ELEMENT at %s" % (finaluri))
                            logging.info("STYLE ELEMENT SIZE: %s at %s" % (len(styleeltrule.cssText), finaluri))
                            for cssrule in styleeltrule:
                                if cssrule.type == 1:
                                    for i, propertyname in enumerate(PROPERTYTOCHECK):
                                        score, propertyresultlist = survey.compareCssProperties('o', 'webkit', propertyname, cssrule.style)
                                        propertyfulllist = survey.getVendorPrefixes(propertyname, cssrule.style)
                                        # printing only if the propertyname is found and if there is more than prefixless
                                        if score > 0:
                                            print finaluri, propertyfulllist
                                            logging.info("SURVEY: %s %s" % (finaluri, propertyfulllist))

                    cssurislist = css.getCssUriList(htmltext, finaluri)
                    if len(cssurislist) == 0:
                        logging.info("NO CSS LINK REL at %s" % (finaluri))
                    else:
                        logging.info("CSS LINK REL: %s at %s" % (len(cssurislist), finaluri))
                    for cssuri in cssurislist:
                        cssruleslist = css.getCssRules(cssuri)
                        logging.info("LINK REL SIZE: %s at %s" % (len(cssruleslist.cssText), cssuri))
                        try:
                            cssruleslist = css.getCssRules(cssuri)
                        except ValueError as e:
                            logging.info("CSS Mime Type error: %s" % (e.message))
                        for cssrule in cssruleslist:
                            if cssrule.type == 1:
                                # This is a rule, we process
                                # Reminder cssrule.type == 0 -> comment
                                for i, propertyname in enumerate(PROPERTYTOCHECK):
                                    score, propertyresultlist = survey.compareCssProperties('o', 'webkit', propertyname, cssrule.style)
                                    propertyfulllist = survey.getVendorPrefixes(propertyname, cssrule.style)
                                    # printing only if the propertyname is found and if there is more than prefixless
                                    # if score > 0 and score != 4:
                                    if score > 0:
                                        # print finaluri, propertyresultlist
                                        print finaluri, propertyfulllist
                                        logging.info("SURVEY: %s %s" % (finaluri, propertyfulllist))
                        # logging.info(responseheaders)

                except requests.exceptions.ConnectionError as e:
                    # we are catching network connection error and record them.
                    logging.info("Connection error: %s" % (e.message))

if __name__ == '__main__':
    main()
