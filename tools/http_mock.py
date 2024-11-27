from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib
import time
from urllib.parse import urlparse
import threading
import ssl
import gzip
import sys

class Handler(BaseHTTPRequestHandler):

    def do_PATCH(self):
        return self.do_GET()

    def do_PUT(self):
        return self.do_GET()

    def do_POST(self):
        return self.do_GET()

    def do_HEAD(self):
        self.send_response(501)
        print(self.headers)

    def do_GET(self):
        size = 1
        portions = 1
        o = urlparse(self.path)
        query = urllib.parse.parse_qs(o.query)

        if 'rcode' in query:
            rcode = int(query['rcode'][0])
        else:
            rcode = 200
        self.send_response(rcode)
        #self.send_response(429)
        if 'headers' in query:
            for i in range(int(query['headers'][0])):
                self.send_header(f'x-custom-header-{i}', 'test')
        if 'bsize' in query:
            size = int(query['bsize'][0])
        if 'bportions' in query:
            portions = int(query['bportions'][0])
        if 'wait' in query:
            time.sleep(int(query['wait'][0]))
        print(query)
        print(self.headers)
        #self.send_header('cache-control', 'no-cache')
        self.send_header('content-type', 'text/html')
        self.send_header('vary', 'Accept-Encoding')
        #self.send_header('cache-control', 'Max-Age=10000')
#        self.send_header('content-encoding', 'gzip')
        self.send_header('header_setsurkey','surrogatekeybug')
        self.send_header('X-Request-Path', self.path )
#       self.send_header('cache-control', 'private, no-cache, no-store, must-revalidate')
        self.end_headers()
        script=b'g'
        self.wfile.write(script)
#        self.wfile.write(gzip.compress(script))
        for i in range(portions):
            self.wfile.write(b'7'*size)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    port = sys.argv[1]
    server = ThreadingSimpleServer(('0.0.0.0', int(port)), Handler)
    #server = ThreadingSimpleServer(('0.0.0.0', 8888), Handler)
    #server.socket = ssl.wrap_socket(server.socket, keyfile='keyfile.key', certfile='certfile.crt', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs=None, do_handshake_on_connect=True)
    server.serve_forever()


if __name__ == '__main__':
    run()