
#
# given a file with hashes for comments and
#   an HTTP URI by line, read it into a list object
# check that the URI has no leading space
#   if yes log an error URI_LEADING_SPACE in error log file
# check that the URI has no trailing space
#   if yes log an error URI_TRAILING_SPACEin error log file
# check that the URI start by "http" or "https",
#   if no log an error URI_NOT_HTTP in error log file
# code to move
# import sys
# def parseUriFile(file="urlist.data"):
#     """Read the list of URIs from a file"""
#     try:
#         f = open(file, 'r')
#         print f
#     except IOError, (errno, strerror):
#         print "I/O error({0}): {1}".format(errno, strerror)
#     except:
#         print "Unexpected error:", sys.exc_info()[0]
#         raise


* href="/css/screen.css"     media="screen,projection,tv"
	@import '/css/core/reset.css';
		[rules]
	@import '/css/core/typography.css';
		[rules]
	@import '/css/core/grid.css';
		[rules]
	@import '/css/core/forms.css';
		[rules]
	@import '/css/pages/common.css';
		[rules]
* href="/css/handheld.css"   media="handheld"
	[rules]
* href="/css/print.css"      media="print"
	@import url(/css/tv.css);
	+ [rules]
* href="/css/pages/home.css" media="screen,projection,tv"
	[rules]