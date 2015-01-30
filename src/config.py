#!/usr/bin/python

import yaml

'''
Parser for project-specific yaml config file
'''
class Parser(object):

	def __init__(self, fp):
		try:
			self._cfg = yaml.load( open(fp, 'r') )
		except yaml.scanner.ScannerError:
			raise Exception('Corrupt configuration file.')

	def server(self):
		'''
		Return the server configuration
		'''
		if 'server' not in self._cfg:
			raise Exception('Corrupt configuration file. No server config.')
		if 'host' not in self._cfg['server']:
			raise Exception('Corrupt configuration file. No host defined.')
		if 'port' not in self._cfg['server']:
			raise Exception('Corrupt configuration file. No port number defined.')
		return self._cfg['server']

	def endpoints(self):
		'''
		Return the endpoint configurations
		'''
		if 'endpoints' not in self._cfg:
			raise Exception('Corrupt configuration file. No endpoints defined.')		
		for ep in self._cfg['endpoints']:
			self.check_endpoint(ep)
		return self._cfg['endpoints']

	def check_endpoint(self, ep):
		'''
		Checks for valid endpoint configuration
		'''
		if 'resource_url' not in ep or 'xpath' not in ep or 'resource_url' not in ep:
			raise Exception('Corrupt configuration file. Endpoint ill-defined.')
