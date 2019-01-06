from http.server import BaseHTTPRequestHandler, HTTPServer
import libamp
import argparse
from urllib.parse import urlparse, parse_qsl
from functools import partial

class Server(BaseHTTPRequestHandler):

  def __init__(self, pin, *args, **kwargs):
        self.pin = pin
        super().__init__(*args, **kwargs)

  def do_GET(self):

    qs = dict(parse_qsl(urlparse(self.path).query))
    command = qs["cmd"]
    repeat = 1
    if "repeat" in qs:
      repeat = qs["repeat"]

    try:
      libamp.execute(self.pin, command, repeat)
      self.send_response(200)
      self.end_headers()
      self.wfile.write(bytes("OK", "utf-8"))
    except Exception as err:
      self.send_response(500)
      self.end_headers()
      self.wfile.write(bytes("Error: {0}".format(err), "utf-8"))
        
def run(port, pin):
    server_address = ("", port)
    handler = partial(Server, pin)
    httpd = HTTPServer(server_address, handler)
    
    print("Starting Cambridge Audio amplifier web control on port %d..." % port)
    httpd.serve_forever()


parser = argparse.ArgumentParser(description="Web server for Cambridge Audio amplifiers control")
parser.add_argument("--pin", nargs="?", default=4, type=int)
parser.add_argument("--port", nargs="?", default=9696, type=int)
args = parser.parse_args()

run(port=args.port, pin=args.pin)
        


