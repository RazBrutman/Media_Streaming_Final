# -*- coding: utf-8 -*-
import socket
from threading import Thread


class MediaServer(object):

    def __init__(self, PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', PORT))
        self.sock.listen(5)

        while True:
            connection, client = self.sock.accept()
            Thread(target=self.HandleClient, args=(connection, client)).start()

    def HandleClient(self, connection, client):
        print "new connection\nIP:", client[0], "\nPort:", client[1]
        connection.send("""HTTP/1.1 200 OK
        Content-Type: audio/mp3\r\n\r\n""")
        f = open("D:\PycharmProjects\\fun_and_games\\green_day_holiday_lyrics.mp3", "rb")
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

MediaServer(54321)