from http.server import BaseHTTPRequestHandler
import json
import time
from example_publisher.config import Config


from example_publisher.publisher import Publisher


class HTTPRequestHandler(BaseHTTPRequestHandler):
    publisher: Publisher
    config: Config

    def is_healthy(self):
        last_successful_update = HTTPRequestHandler.publisher.last_successful_update
        return (
            last_successful_update is not None
            and time.time() - last_successful_update
            < HTTPRequestHandler.config.health_check_threshold_secs
        )

    def do_GET(self):
        healthy = self.is_healthy()
        data = {
            "status": "ok" if healthy else "error",
            "last_successful_update": HTTPRequestHandler.publisher.last_successful_update,
        }

        self.send_response(200 if healthy else 503)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
