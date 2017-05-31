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
        db = database()

        self._set_headers()

        if self.path.startswith("/User"):
            params = parse_qs(urlparse(self.path).query)
            self.wfile.write(db.get_user(params['name'][0], params['ip'][0]))


        elif self.path.startswith("/Friends"):
            params = parse_qs(urlparse(self.path).query)
            friends = db.get_friends(params['name'][0])
            self.wfile.write(friends)

        elif self.path.startswith("/Files"):
            params = parse_qs(urlparse(self.path).query)
            files = db.get_files(params['name'][0])
            self.wfile.write(files)

        elif self.path.startswith("/Path"):
            params = parse_qs(urlparse(self.path).query)
            db.add_file(params['p'][0], params['name'][0])

        else:
            self.wfile.write("<html><body><h1>Hi!</h1></body></html>")
        db.close_db()

Server()
