# -*- coding: utf-8 -*-
from model import Client
from view import StreamerGUI
import Tkinter as tk
import tkMessageBox
import socket


class Controller(object):
    def __init__(self):
        self.model = Client()
        self.root = tk.Tk()
        self.view = StreamerGUI(self.root, self)
        self.run()

    def run(self):
        root = self.root
        #root.geometry("100x100")
        #root.resizable(width=False, height=False)
        root.iconbitmap(r"..\..\resources\favicon.ico")
        root.title("Streamer")
        root.deiconify()
        root.mainloop()

    def user_exists(self, name):
        return self.model.send_msg("/User?name=" + name + "&ip=" + socket.gethostbyname_ex(socket.gethostname())[2][1])

    def validate(self, name):
        return self.model.send_msg("/Friends?name=" + name)

    def user_files(self, name):
        return self.model.send_msg("/Files?name=" + name)

    def add_path(self, path, name):
        self.model.send_msg("/Path?p=" + path + "&name=" + name)
        tkMessageBox.askokcancel("Success!", "You have successfuly added a file to your shared files")