#!/usr/bin/python

from lxml import html
import requests

INIT_FIELDS = [ 'endpoint_url', \
				'resource_url', \
				'xpath' ]

'''
Encapsulates an endpoint to RESTful api service
'''
class Endpoint(object):

	def __init__(self, params):
		for field in INIT_FIELDS:
			if field not in params:
				raise EndpointException('\'%s\' is a required field.' % field)
		self._params = params
		self._params['endpoint_url'] = self.valid_url(self._params['endpoint_url'])

	def do_get(self):
		return self.scrape(self._params['resource_url'], \
								self._params['xpath'])

	def scrape(self, resource_url, xpath):
		page = requests.get(resource_url)
		tree = html.fromstring(page.text)
		return tree.xpath(xpath)

	def url(self):
		return self._params['endpoint_url']

	def valid_url(self, endpoint_url):
		if not endpoint_url.startswith('/'):
			endpoint_url = '/' + endpoint_url
		if not endpoint_url.endswith('/'):
			endpoint_url += '/'
		return endpoint_url
	

class EndpointException(Exception):
	pass











