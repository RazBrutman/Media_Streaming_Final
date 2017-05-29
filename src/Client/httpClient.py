import httplib
import sys

class HttpClient(object):

    def __init__(self, httpServer):
        conn = httplib.HTTPConnection(httpServer)

    def getFriendInfo(self):
        return


while 1:
    cmd = raw_input('input command (ex. GET index.html): ')
    cmd = cmd.split()

    if cmd[0] == 'exit': #tipe exit to end it
        break

    #request command to server
    conn.request(cmd[0], cmd[1])

    #get response from server
    rsp = conn.getresponse()

    #print server response and data
    print(rsp.status, rsp.reason)
    data_received = rsp.read()
    print(data_received)
  
conn.close()