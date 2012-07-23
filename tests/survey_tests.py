import unittest
from survey import core
import cssutils


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
        self.req = core.HttpRequests()

    def tearDown(self):
        self.req = None

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

    def tearDown(self):
        self.css = None
        self.req = None

    def testUriCssList(self):
        "For a given html page, check if we get the right list of linked stylesheets"
        WebSiteUri = "http://example.org/"
        content_input = """<!doctype html>
            <html>
            <head>
                <title>Test</title>
                <link rel="stylesheet" href="/css/style1.css">
                <link rel="stylesheet" href="http://example.org/css/style2.css">
            </head>
            <body>
            </body>
            </html>"""
        expected = ['http://example.org/css/style1.css', 'http://example.org/css/style2.css']
        actual = self.css.getCssUriList(content_input, WebSiteUri)
        # we need to compare ordered list.
        actual.sort()
        expected.sort()
        self.assertListEqual(expected, actual)

    def testUriCssHttp(self):
        "For a given set of HTTP headers, is there an HTTP Link header for CSS"
        WebSiteUri = "http://example.org/"
        http_input = {'content-length': '1162', 'date': 'Thu, 19 Jul 2012 19:16:43 GMT', 'content-type': 'text/html; charset=utf-8', 'server': 'Apache/2.2.21', 'link': 'http://example.org/css/style.css;rel=stylesheet'}
        expected = ['http://example.org/css/style.css']
        actual = self.css.getCssHttpUriList(http_input, WebSiteUri)
        actual.sort()
        expected.sort()
        self.assertListEqual(expected, actual)

    def testRulesList(self):
        "for a given CSS do we list the right list of rules"
        pass

    def testHasStyleElement(self):
        "for a given URI, there a style element. return True."
        content = "<!doctype><html><head><title>foo</title><style>.foo {color: #fff;}</style></head><body>foo</body></html>"
        self.assertTrue(self.css.hasStyleElement(content))

    def testNoStyleElement(self):
        "for a given URI, there is no style element. return False"
        content = "<!doctype><html><head><title>foo</title></head><body>foo</body></html>"
        self.assertFalse(self.css.hasStyleElement(content))

    def testStyleElementRules(self):
        "When there is a style element, do we get the expected rules?"
        # we might need to normalize to cope for spaces in the test.
        content = """<!doctype><html><head><title>foo</title>
            <style>.foo {/*comment*/
            color: #fff;}</style>
            <!-- foo -->
            <style>  .bar {margin: 10px;}</style>
            </head><body>foo</body></html>"""
        expected = u'.foo {color: #fff;}.bar {margin: 10px;}'
        actual = self.css.getStyleElementRules(content).cssText
        self.assertEqual(expected, actual)


class SurveyTests(unittest.TestCase):
    """Tests for survey Stats"""

    def setUp(self):
        self.survey = core.Survey()
        self.css = core.Css()

    def tearDown(self):
        self.survey = None


def main():
    unittest.main()


if __name__ == '__main__':
    main()
