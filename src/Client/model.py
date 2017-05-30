# -*- coding: utf-8 -*-
import httplib
from threading import Thread
import pickle
from Queue import Queue
import errno


class Client(object):

    def send_msg(self, url):
        return HttpClient('127.0.0.1', 8000).assignToThread(url)


class HttpClient(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def assignToThread(self, url):
        q = Queue()
        Thread(target=self.Request, args=[url, q]).start()
        return q.get()

    def Request(self, url, q):
        conn = httplib.HTTPConnection(self.ip, self.port)
        conn.request("GET", url)
        rsp = conn.getresponse()
        #print server response and data
        data = rsp.read()
        if url.startswith("/Friends"):
            data = pickle.loads(data)
        q.put(data)
        conn.close()