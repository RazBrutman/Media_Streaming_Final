import Tkinter as tk
import ttk
import os

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
        self.new = ttk.Button(buttons, text="Create new account", command=lambda: pagecontroll.show_frame(PageOne, pages['PageOne']))
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
        self.play.bind("<Button>", self.Daemon)
        self.play.pack()

    def Daemon(self, event):
        raz = self.controller.validate()[0]
        os.system(VLC_STREAM_URL + " http://" + raz.ip + ":18000/" + DEFAULT)


class MainUserPage(tk.Frame):

    def __init__(self, parent, pagecontroll, controller):

        tk.Frame.__init__(self, parent)  # construct frame
        self.controller = controller
        right_frame = tk.Frame(self)
        friends = self.controller.validate()
        for user in friends:
            ttk.Label(right_frame, text=user.username, font=SMALL_FONT).pack()
        right_frame.pack(side="right")
        left_frame = tk.Frame(self)
        ttk.Label(left_frame, text="Some text", font=LARGE_FONT).pack()
        left_frame.pack(side="left")