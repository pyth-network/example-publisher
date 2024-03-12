from http.server import BaseHTTPRequestHandler
import json

from example_publisher.publisher import Publisher

class HTTPRequestHandler(BaseHTTPRequestHandler):
    publisher: Publisher = None

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            'status': 'ok',
            'last_successful_update': HTTPRequestHandler.publisher.last_successful_update
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))