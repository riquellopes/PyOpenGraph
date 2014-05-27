#conding: utf-8
import unitest
from nose.tools import *
 
class MockUrlLib(object):
	
	def __init__(self, _file, _type='html', code=200, msg='OK', headers={'content-type': 'text/plain; charset=utf-8'}):
		self.file_test = ("%s.%s" % (_file, _type))
		self.code = code
		self.msg = msg
		self.headers = headers
		
	def read(self):
		handle = open(self.file_test)
		html = "".join( handle )
		return html


class PyOpenGraph(unitest.TestCase):
	pass