import unittest
from survey import core


class UriCheckTests(unittest.TestCase):
    """Tests for Uris"""

    def testHttpURI(self):
        gooduri = core.UriCheck()
        httpuristart = 'http://www.opera.com/'
        self.assertTrue(gooduri.ishttpURI(httpuristart))

    def testHttpsURI(self):
        gooduri = core.UriCheck()
        httpuristart = 'https://www.opera.com/'
        self.assertTrue(gooduri.ishttpURI(httpuristart))

    def testUpperCaseHttpURI(self):
        gooduri = core.UriCheck()
        httpuristart = 'HTTP://www.opera.com/'
        self.assertTrue(gooduri.ishttpURI(httpuristart))

    def testHttpURIWrong(self):
        gooduri = core.UriCheck()
        httpurifalse = 'mailto:foo@example.org'
        self.assertFalse(gooduri.ishttpURI(httpurifalse))

    def testLeadingSpaceHttpURI(self):
        gooduri = core.UriCheck()
        httpuristart = '  http://www.opera.com/'
        self.assertTrue(gooduri.ishttpURI(httpuristart))

    def testTrailingSpaceHttpURI(self):
        gooduri = core.UriCheck()
        httpuristart = 'http://www.opera.com/   '
        self.assertTrue(gooduri.ishttpURI(httpuristart))


class HttpRequestsTests(unittest.TestCase):
    """Tests for HTTP"""

    def setUp(self):
        "Starting a Web server"
        pass

    def testGetRequestStatusOK(self):
        "Check if everything is ok"
        pass

    def testGetRequestStatus4xx(self):
        "Check if we advertise the right message when 4xx"
        pass

    def testGetRequestLocation(self):
        "Check if we grab the right location when there is a redirection"
        pass


class CssTests(unittest.TestCase):
    """Tests for CSS requests"""

    def setUp(self):
        self.css = core.Css()
        self.req = core.HttpRequests()

    def testCssList(self):
        "For a given Web site, check if we get the right list of linked stylesheets"
        WebSiteUri = 'http://www.opera.com/'
        expected = [
        'http://www.opera.com/css/handheld.css',
        'http://www.opera.com/css/screen.css',
        'http://www.opera.com/css/print.css',
        'http://www.opera.com/css/pages/home.css']
        content = self.req.getContent(WebSiteUri)
        actual = self.css.getCssUriList(content, WebSiteUri)
        # we need to compare ordered list.
        actual.sort()
        expected.sort()
        self.assertListEqual(expected, actual)

    def testRulesList(self):
        "for a given CSS do we list the right list of rules"
        pass

    def testHasStyleElement(self):
        "for a given URI, is there a style element? return True if there is."
        content = "<!doctype><html><head><title>foo</title><style>.foo {color: #fff;}</style></head><body>foo</body></html>"
        self.assertTrue(self.css.hasStyleElement(content))

    def testStyleElementRules(self):
        "When there is a style element, do we gest the expected rules?"
        # we might need to normalize to cope for spaces in the test.
        content = "<!doctype><html><head><title>foo</title><style>.foo {color: #fff;}</style></head><body>foo</body></html>"
        expected = ".foo {color: #fff;}"
        actual = self.css.getStyleElementRules(content)
        self.assertEqual(expected, actual)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
