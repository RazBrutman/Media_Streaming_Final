# -*- coding: utf-8 -*-
import httplib
from threading import Thread
import pickle
from Queue import Queue


class Client(object):
    def send_msg(self, *args):
        return HttpClient('127.0.0.1', 8000).assignToThread(*args)


class HttpClient(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def assignToThread(self, *args):
        q = Queue()
        Thread(target=self.getFriendInfo, args=[q]).start()
        return q.get()

    def getFriendInfo(self, q):
        conn = httplib.HTTPConnection(self.ip, self.port)
        conn.request("GET", "/Friends?name=Raz")
        rsp = conn.getresponse()
        #print server response and data
        print(rsp.status, rsp.reason)
        data_received = rsp.read()
        friend_list = pickle.loads(data_received)
        conn.close()
        q.put(friend_list)




