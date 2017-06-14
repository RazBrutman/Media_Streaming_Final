# -*- coding: utf-8 -*-
from model import Client
from view import StreamerGUI
import Tkinter as tk
import tkMessageBox
from threading import Thread
import os
import socket
import subprocess

import sys
sys.path.insert(0, '../Commons')
from Config import *


class Controller(object):
    def __init__(self):
        self.model = Client()
        # if self.model.send_msg("/") == "Server error":
        #     tkMessageBox.showerror("Server error", "App server is not connected! Please try again")
        #     return
        self.root = tk.Tk()
        self.view = StreamerGUI(self.root, self)
        self.run()

    def run(self):
        root = self.root
        root.resizable(width=False, height=False)
        root.iconbitmap(r"favicon.ico")
        root.title("Streamer")
        root.deiconify()
        root.mainloop()

    def get_all(self, name):
        return self.model.send_msg("/All?name=" + name)

    def edit_relationship(self, name1, name2, to_remove):
        return self.model.send_msg("/Edit?name1=" + name1 + "&name2=" + name2 + "&to_remove=" + str(to_remove))

    def user_exists(self, name):
        # Get local Server IP address
        import socket
        return self.model.send_msg("/User?name=" + name + "&ip=" + socket.gethostbyname(socket.gethostname()))

    def validate(self, name):
        return self.model.send_msg("/Friends?name=" + name)

    def user_files(self, name):
        return self.model.send_msg("/Files?name=" + name)

    def add_path(self, path, name):
        return self.model.send_msg("/Path?p=" + path + "&name=" + name)

    def daemon(self, event, user, path):
        Thread(target=self.playthread, args=[user.ip, path]).start()

    def playthread(self, ip, path):
        command = '"' + VLC_STREAM_URL + '" "http://' + ip + ':' + str(STREAMER_PORT) + "/" + path + '"'
        subprocess.call(command, shell=True)
