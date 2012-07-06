import unittest
from survey import core


class UriCheckTests(unittest.TestCase):
    """Tests for parseUriFile"""

    def testHttpURI(self):
        gooduri = core.UriCheck()
        httpuristart = 'http://www.opera.com/'
        self.assertTrue(gooduri.ishttpURI(httpuristart))



def main():
    unittest.main()


if __name__ == '__main__':
    main()
