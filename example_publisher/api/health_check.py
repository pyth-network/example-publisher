from http.server import BaseHTTPRequestHandler
import json
import time
from example_publisher.config import Config


from example_publisher.publisher import Publisher


class HTTPRequestHandler(BaseHTTPRequestHandler):
    publisher: Publisher = None
    config: Config = None

    def __init__(self, *args, **kwargs):
        self.test_priod_secs: int = (
            HTTPRequestHandler.config.health_check_test_period_secs
        )
        self.last_successful_update: float = (
            HTTPRequestHandler.publisher.last_successful_update
        )
        super().__init__(*args, **kwargs)

    def is_healthy(self):
        return (
            self.last_successful_update is not None
            and time.time() - self.last_successful_update < self.test_priod_secs
        )

    def do_GET(self):
        healthy = self.is_healthy()
        data = {
            "status": "ok" if healthy else "error",
            "last_successful_update": self.last_successful_update,
        }

        self.send_response(200 if healthy else 503)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
