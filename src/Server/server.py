import BaseHTTPServer
import SocketServer
from urlparse import urlparse, parse_qs
from User import MyTestData


class Server(object):

    def __init__(self):

        PORT = 8000
        Handler = CostumeHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        httpd.serve_forever()


class CostumeHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_GET(self):
        #todo Change to switch
        params = ""
        if self.path.startswith("/Friends"):
            params = parse_qs(urlparse(self.path).query)
            #go to database and get all

            #go to db get
            self._set_headers()
            self.wfile.write(MyTestData().get())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


Server()
