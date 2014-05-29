#!/usr/bin/env python
#coding: utf-8

#Copyright (c) 2010 Gerson Minichiello
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import re
import rdfadict
import urllib2
from bs4 import BeautifulSoup

OPENGRAPH_NAMESPACES = [
  "http://opengraphprotocol.org/schema",
  "http://opengraphprotocol.org/schema/",
  "http://ogp.me/ns#",
]

class PyOpenGraph(object):
	
	def __init__(self, url=None, xml=None, prefix=True):
		if prefix:
			parser = rdfadict.RdfaParser()
			if not xml:
				result = parser.parse_url(url)
			else:
				result = parser.parse_string(xml, url)
		else:
			result = self._parse_web(url)
		data = result[url]
		self.metadata = self.get_properties(data)
	
	def get_properties(self, data):
		content = {}
		for k, v in data.iteritems():
			for ns in OPENGRAPH_NAMESPACES:
				if k.startswith(ns) and len(v)>0:
					content[k.replace(ns, '')] = v[0]
		return content
	
	def _parse_web(self, url):
		soup = BeautifulSoup( urllib2.urlopen(url).read() )
		content = {} 
		for og in soup.findAll('meta', {'property':re.compile('og:')}):
			content["{0}/{1}".format(OPENGRAPH_NAMESPACES[0], og['property'].split(':')[1])] = [ og['content'] ]
		return {url:content}