#coding: utf-8
import unittest
from mock import patch
from nose.tools import *
from PyOpenGraph import PyOpenGraph as o

class MockResponse(object):
	
	def __init__(self, _file, _type='html', code=200, msg='OK', headers={'content-type': 'text/plain; charset=utf-8'}):
		self.file_test = ("%s.%s" % (_file, _type))
		self._type = _type
		self.code = code
		self.msg = msg
		self.headers = headers
		
	def parse_url(self, *arg):
		handle = open(self.file_test)
		html = "".join( handle )
		if self._type == 'json':
			import json
			return json.loads(html)
		return html
	
	def parse_string(self, *arg):
		pass


class PyOpenGraph(unittest.TestCase):
	
	@patch('PyOpenGraph.PyOpenGraph.rdfadict.RdfaParser')
	def test_for_zappos_web_site_the_lib_should_be_load_og_metas(self, p):
		"""
			For the zappos web site, the lib should be load og metas.
		"""
		p.return_value = MockResponse('contents/zappos', _type='json', headers={'content-type': 'text/javascript;  charset=utf-8'})
		og = o.PyOpenGraph('http://www.zappos.com/timberland-pro-titan-safety-toe-oxford')
		assert_equals(og.metadata['title'], u'Timberland PRO TiTAN® Safety Toe Oxford')
		assert_equals(og.metadata['url'], 'http://www.zappos.com/timberland-pro-titan-safety-toe-oxford')
		assert_equals(og.metadata['type'], 'product')
		assert_equals(og.metadata['site_name'], 'Zappos.com')
	
	@patch('PyOpenGraph.PyOpenGraph.rdfadict.RdfaParser')
	def test_for_booking_web_site_the_lib_should_be_load_og_metas(self, p):
		"""
			For the booking web site, the lib should be load og metas.
		"""
		p.return_value = MockResponse('contents/booking', _type='json', headers={'content-type': 'text/javascript;  charset=utf-8'})
		og = o.PyOpenGraph('http://www.booking.com/hotel/br/best-western-sol-ipanema.pt-br.html')
		assert_equals(og.metadata['title'], 'Best Western Plus Sol Ipanema Hotel, Rio de Janeiro, BR')
		assert_equals(og.metadata['url'], 'http://www.booking.com/hotel/br/best-western-sol-ipanema.pt-br.html')
		assert_equals(og.metadata['type'], 'booking_com:hotel')
		assert_equals(og.metadata['site_name'], 'Booking.com')
	
	@patch('PyOpenGraph.PyOpenGraph.rdfadict.RdfaParser')
	def test_case_player_does_n_use_prefix_og_at_head_the_lib_should_be_process_with_beaut_soap(self, p):
		"""
			Case player does'n use prefix og at head, the lib should be process with beautiful soup.
		"""
		og = o.PyOpenGraph('http://www.hotelurbano.com/pacote/rio-de-janeiro-angra-dos-reis-melia-angra/48795')
		assert_equals(og.metadata['title'], 'Angra dos Reis, Meliá Angra, 7x de R$ 60,00')
		assert_equals(og.metadata['type'], 'website')
		assert_equals(og.metadata['site_name'], 'hotelurbano.com')
		assert_equals(og.metadata['url'], 'http://www.hotelurbano.com/pacote/rio-de-janeiro-angra-dos-reis-melia-angra/48795?cmp=895')