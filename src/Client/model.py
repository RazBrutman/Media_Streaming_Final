# -*- coding: utf-8 -*-
import httplib
import pickle


class Client(object):

    def send_msg(self, *args):
        return HttpClient('127.0.0.1', 8000).getFriendInfo()


class HttpClient(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def getFriendInfo(self):
        conn = httplib.HTTPConnection(self.ip, self.port)
        conn.request("GET", "/Friends?name=raz")
        rsp = conn.getresponse()
        #print server response and data
        print(rsp.status, rsp.reason)
        data_received = rsp.read()
        friend_list = pickle.loads(data_received)
        conn.close()
        return friend_list

