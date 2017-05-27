# -*- coding: utf-8 -*-
from model import Client
from view import StreamerGUI
import Tkinter as tk
import tkMessageBox
#import database


class Controller(object):
    def __init__(self, ip, port):
        self.model = Client(ip, port)
        if not self.model.connected:
            tkMessageBox.showerror("Server not found!",
                                   """We've encountered a problem trying to connect to the server.
                                   Please try again later.""")
        else:
            self.root = tk.Tk()
            self.view = StreamerGUI(self.root, self)
            self.run()

    def run(self):
        root = self.root

        #root.geometry("100x100")
        #root.resizable(width=False, height=False)
        root.iconbitmap(r'favicon.ico')
        root.title("Streamer")
        root.deiconify()
        root.mainloop()

    def validate(self, un, ps):
        self.model.send_msg([un, ps], type="account")




