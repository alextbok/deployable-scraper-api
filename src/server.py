#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse
from endpoint import Endpoint
from config import Parser

CONFIG_PATH = '../config/config.yaml'

class Server(object):

	def __init__(self):
		parser = Parser(CONFIG_PATH)
		self._host = parser.server()['host']
		self._port = parser.server()['port']
		self._endpoints = {}
		for ep in parser.endpoints():
			self._endpoints[ ep['endpoint_url'] ] = Endpoint(ep)

	def add_endpoint(self, params):
		self._endpoints.append( Endpoint(params) )
		self._urls.append( params['endpoint_url'] )

	def run(self):
		def handler(*args):
			Handler(self._endpoints, *args)
		server = ThreadedHTTPServer((self._host, self._port), handler)
		server.serve_forever()		

class Handler(BaseHTTPRequestHandler):

	def __init__(self, endpoints, *args):
		self._endpoints = endpoints
		BaseHTTPRequestHandler.__init__(self, *args)

	def do_GET(self):
		
		parsed_path = urlparse.urlparse(self.path)
		real_path = parsed_path.path if parsed_path.path.endswith('/') \
										else parsed_path.path + '/'
		if real_path in self._endpoints:
			print self._endpoints[real_path].do_get()

		message_parts = [
				'CLIENT VALUES:',
				'client_address=%s (%s)' % (self.client_address,
											self.address_string()),
				'command=%s' % self.command,
				'path=%s' % self.path,
				'real path=%s' % parsed_path.path,
				'query=%s' % parsed_path.query,
				'request_version=%s' % self.request_version,
				'',
				'SERVER VALUES:',
				'server_version=%s' % self.server_version,
				'sys_version=%s' % self.sys_version,
				'protocol_version=%s' % self.protocol_version,
				'',
				'HEADERS RECEIVED:',
				]

		for name, value in sorted(self.headers.items()):
			message_parts.append('%s=%s' % (name, value.rstrip()))
		message_parts.append('')
		message = '\r\n'.join(message_parts)

		message += '\n ' + threading.currentThread().getName()
		
		self.send_response(200)
		self.end_headers()

		self.wfile.write(message)
		self.wfile.write('\n')
		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""This class handles requests in a separate thread."""

if __name__ == '__main__':
	print 'Starting server, use <Ctrl-C> to terminate'
	s = Server()
	s.run()







