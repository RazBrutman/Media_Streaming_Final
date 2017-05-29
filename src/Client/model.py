# -*- coding: utf-8 -*-
import socket
import select
import msvcrt
import os
import httplib
import sys
from threading import Thread


class Client(object):

    def send_msg(self, *args):
        HttpClient('127.0.0.1', 8000).assignToThread(*args)


class HttpClient(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def assignToThread(self, *args):
        Thread(target=self.getFriendInfo).start()

    def getFriendInfo(self):
        conn = httplib.HTTPConnection(self.ip, self.port)
        conn.request("GET", "\\")
        rsp = conn.getresponse()
        #print server response and data
        print(rsp.status, rsp.reason)
        data_received = rsp.read()
        print(data_received)
        conn.close()
        return

