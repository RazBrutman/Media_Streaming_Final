import BaseHTTPServer
import SocketServer
from urlparse import urlparse, parse_qs
from database import database


class Server(object):

    def __init__(self):

        PORT = 8000
        Handler = CostumeHandler
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        print "started"
        httpd.serve_forever()


class CostumeHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_GET(self):
        #TODO: Change to switch
        params = ""

        self._set_headers()

        if self.path.startswith("/User"):
            params = parse_qs(urlparse(self.path).query)
            db = database()
            self.wfile.write(db.get_user(params['name'][0], params['ip'][0]))

        elif self.path.startswith("/Friends"):
            params = parse_qs(urlparse(self.path).query)
            db = database()
            friends = db.get_friends(params['name'][0])
            self.wfile.write(friends)
            db.close_db()

        elif self.path.startswith("/Files"):
            params = parse_qs(urlparse(self.path).query)
            db = database()
            files = db.get_files(params['name'][0])
            self.wfile.write(files)
            db.close_db()

        else:
            self.wfile.write("<html><body><h1>Hi!</h1></body></html>")

Server()
