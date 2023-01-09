

import http.server
from socketserver import ThreadingMixIn
import threading
import urllib.request
import signal


EXIT_EVENT = threading.Event()
PU_BASE_URL = "https://example.com"

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Send a 'GET' request to a remote server over HTTPS
            print("dasdasdasda")
            url = "{base_url}{path}"\
                .format(base_url=PU_BASE_URL, path=self.path)

            response = urllib.request.urlopen(url)

            # Read the response data
            data = response.read()

            self.send_response(response.status)
            
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Write the response data
            self.wfile.write(data)
        except Exception:
            self.send_response(404)
            
            self.send_header("Content-Type", "application/json")
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
    pass

class StoppableHTTPsProxyServer():
    def __init__(self):
        self.server = None

    def start_server(self):
        self.server = ThreadedHTTPServer(('localhost', 8000), Handler)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass


def signal_handler(signal, frame):
    proxy_server.server.shutdown
    EXIT_EVENT.set()
    sys.exit(1)

proxy_server = StoppableHTTPsProxyServer()
signal.signal(signal.SIGINT, signal_handler)
daemon = threading.Thread(
    name='mp_proxy_server', target=proxy_server.start_server)
daemon.start()
daemon.join()


