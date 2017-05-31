# -*- coding: utf-8 -*-
import socket
from threading import Thread

import sys
sys.path.insert(0, '../Commons')
from Config import *


class MediaServer(object):

    def __init__(self, PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', PORT))
        print "Started"
        self.sock.listen(5)

        while True:
            connection, client = self.sock.accept()
            Thread(target=self.HandleClient, args=(connection, client)).start()

    def HandleClient(self, connection, client):
        data = connection.recv(2048)
        path = data.split(" ")[1][1:]
        print "new connection\nIP:", client[0], "\nPort:", client[1]
        connection.send("""HTTP/1.1 200 OK
        Content-Type: application/octet-stream\r\nCache-Control: no-cache\r\n\r\n""")
        f = open(path, "rb")
        l = f.read(4096)
        while l:
            try:
                connection.send(l)
                l = f.read(4096)
            except socket.error:
                break
        f.close()
        connection.close()
        print "connection closed"

MediaServer(STREAMER_PORT)