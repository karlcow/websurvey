import unittest
from survey import core


class UriCheckTests(unittest.TestCase):
    """Tests for parseUriFile"""

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


def main():
    unittest.main()


if __name__ == '__main__':
    main()
