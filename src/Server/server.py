import BaseHTTPServer
import SocketServer
from urlparse import urlparse, parse_qs
from database import database

import sys
sys.path.insert(0, '../Commons')
from Config import *

class Server(object):

    def __init__(self):
        Handler = CostumeHandler
        httpd = SocketServer.TCPServer(("", SERVER_PORT), Handler)
        print "Started"
        httpd.serve_forever()


class CostumeHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_GET(self):
        params = ""
        db = database()

        self._set_headers()

        if self.path.startswith("/All"):
            params = parse_qs(urlparse(self.path).query)
            friends = db.get_friends(params['name'][0], "All")
            self.wfile.write(friends)

        elif self.path.startswith("/Edit"):
            params = parse_qs(urlparse(self.path).query)
            db.edit_relationship(params['name1'][0], params['name2'][0], params['to_remove'][0])

        elif self.path.startswith("/User"):
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
            self.wfile.write("1")

        else:
            self.wfile.write("<html><body><h1>Saar The King</h1></body></html>")
        db.close_db()

# Get local Server IP address
import subprocess
cmd = subprocess.Popen('ipconfig', shell=True, stdout=subprocess.PIPE).stdout
l = ""
for line in cmd:
    if line.__contains__("IPv4 Address"):
        l = line
print "FOR CONFIG FILE: USE " + l.split(":")[-1][1:]

# Start Server
Server()
