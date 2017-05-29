# -*- coding: utf-8 -*-
from model import Client
from view import StreamerGUI
import Tkinter as tk
import tkMessageBox
#import database


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

    def validate(self, un, pw):
        self.model.send_msg(un, pw)




