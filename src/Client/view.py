import Tkinter as tk
import ttk
import os
from threading import Thread

from Constants import *


LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Times New Roman", 11)
pages = dict(StartPage='500x300',
             PageOne='300x300',
             MainUserPage='600x400')


class StreamerGUI(object):

    def __init__(self, root, controller):

        self.root = root
        # this container contains all the pages
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0, weight=1)  # make the cell in grid cover the entire window
        self.frames = {}  # these are pages we want to navigate to

        for F in (StartPage, PageOne, MainUserPage):  # for each page
            frame = F(container, self, controller)  # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew")  # grid it to container

        self.show_frame(StartPage, pages['StartPage'])  # let the first page be StartPage

    def show_frame(self, name, size):
        self.root.geometry(size)
        frame = self.frames[name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, pagecontroll, controller):

        tk.Frame.__init__(self, parent)  # construct frame
        self.controller = controller

        label = ttk.Label(self, text="Welcome to Streamer!", font=LARGE_FONT)
        label.pack(pady=10)
        info = tk.Frame(self)
        user = ttk.Label(info, text="Username:", font=SMALL_FONT)
        user.grid(row=0)
        self.userentry = ttk.Entry(info)
        self.userentry.grid(row=1)
        passw = ttk.Label(info, text="Password:", font=SMALL_FONT)
        passw.grid(row=2)
        self.passwentry = ttk.Entry(info, show='*')
        self.passwentry.grid(row=3)
        info.pack(pady=20)

        buttons = tk.Frame(self)
        self.sub = ttk.Button(buttons, text="Submit")
        # self.sub.bind("<Button>", self.validate)
        self.sub.grid(row=0, pady=5)
        self.new = ttk.Button(buttons, text="Create new account",
                              command=lambda: pagecontroll.show_frame(PageOne, pages['PageOne']))
        self.new.grid(row=1, pady=5)
        buttons.pack()

        #button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(ViewFriendInfo))
        #button2.pack()

    # def validate(self, event):
    #     self.controller.validate(self.userentry.get(), self.passwentry.get())
    #     self.userentry.delete(0, 'end')
    #     self.passwentry.delete(0, 'end')


class PageOne(tk.Frame):

    def __init__(self, parent, pagecontroll, controller):

        tk.Frame.__init__(self, parent)  # construct frame
        self.controller = controller

        label = ttk.Label(self, text='Page One', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Home', command=lambda: pagecontroll.show_frame(StartPage,
                                                                                                pages['StartPage']))
        button2 = ttk.Button(self, text='To view friends', command=lambda: pagecontroll.show_frame(MainUserPage,
                                                                                                pages['MainUserPage']))
        button1.pack()
        button2.pack()
        self.play = ttk.Button(self, text="Play")
        self.play.bind("<Button>", self.daemon)
        self.play.pack()

    def daemon(self, event):
        raz = self.controller.validate()[0]
        os.system(VLC_STREAM_URL + " http://" + raz.ip + ":18000/" + DEFAULT)


class MainUserPage(tk.Frame):

    def __init__(self, parent, pagecontroll, controller):

        tk.Frame.__init__(self, parent)  # construct frame

        self.controller = controller

        self.right_frame = tk.Frame(self)
        friends = self.controller.validate()
        for user in friends:
            l = ttk.Label(self.right_frame, text=user.username, font=SMALL_FONT)
            l.bind("<Button>", lambda event, data=user: self.test(event, data))
            l.pack(side="top")
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        self.left_frame = tk.Frame(self, bg="#888888", width=100, height=10)
        self.info = ttk.Label(self.left_frame, text="Some text", font=LARGE_FONT, background="#888888")
        self.info.pack(fill="none", expand=True)
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def test(self, event, user):
        file_list = self.controller.user_files(user.username)
        for child in self.left_frame.winfo_children():
            child.destroy()
        files = file_list.split(" ")
        files_frame = tk.Frame(self.left_frame, background="#888888")
        for element in files:
            l = ttk.Label(files_frame, text=element, font=SMALL_FONT, background="#888888")
            l.bind("<Button>", lambda e=event, u=user: self.daemon(e, u))
            l.pack()
        files_frame.pack(fill="none", expand=True)

    def daemon(self, event, user):
        Thread(target=self.playthread, args=[user.ip, event.widget['text']]).start()

    def playthread(self, ip, path):
        os.system(VLC_STREAM_URL + " http://" + ip + ":18000/" + path)