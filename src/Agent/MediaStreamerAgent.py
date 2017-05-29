# -*- coding: utf-8 -*-
import socket
from threading import Thread


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

    # 'GET /D:\\Music\\green_day_holiday.mp3 HTTP/1.1
    # Host: 10.0.0.8:18000
    # User-Agent: VLC/2.2.6 LibVLC/2.2.6
    # Range: bytes=0-
    # Connection: close
    # Icy-MetaData: 1'
        path = data.split(" ")[1][1:]
        print "new connection\nIP:", client[0], "\nPort:", client[1]
        connection.send("""HTTP/1.1 200 OK
        Content-Type: audio/mp3\r\n\r\n""")
        f = open(path, "rb")
        l = f.read(1024)
        while l:
            try:
                connection.send(l)
                l = f.read(1024)
            except socket.error:
                break
        f.close()
        connection.close()
        print "connection closed"

MediaServer(18000)