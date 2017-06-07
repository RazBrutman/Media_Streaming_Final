import httplib
from threading import Thread
import pickle
from Queue import Queue
import sys
sys.path.insert(0, '../Commons')
import User
from Config import *



class Client(object):

    def send_msg(self, url):
        return HttpClient(SERVER_IP, SERVER_PORT).assignToThread(url)


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
        try:
            conn.request("GET", url)
            rsp = conn.getresponse()
            #print server response and data
            data = rsp.read()
            if url.startswith("/Friends") or url.startswith("/All"):
                data = pickle.loads(data)
            q.put(data)
            conn.close()
        except Exception as ex:
            print ex
            q.put("Server error")