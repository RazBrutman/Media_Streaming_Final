import Tkinter as tk
import ttk
import os


LARGE_FONT = ("Verdana", 12)  # font's family is Verdana, font's size is 12
SMALL_FONT = ("Times New Roman", 11)
pages = dict(StartPage='500x300',
             PageOne='300x300')


class StreamerGUI(object):

    def __init__(self, root, controller):

        self.root = root
        # this container contains all the pages
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0, weight=1)  # make the cell in grid cover the entire window
        self.frames = {}  # these are pages we want to navigate to

        for F in (StartPage, PageOne):  # for each page
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
        tk.Frame.__init__(self, parent)

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
        self.sub.bind("<Button>", self.validate)
        self.sub.grid(row=0, pady=5)
        self.new = ttk.Button(buttons, text="Create new account", command=lambda: pagecontroll.show_frame(PageOne, pages['PageOne']))
        self.new.grid(row=1, pady=5)
        buttons.pack()

        #button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(ViewFriendInfo))
        #button2.pack()

    def validate(self, event):
        self.controller.validate(self.userentry.get(), self.passwentry.get())
        self.userentry.delete(0, 'end')
        self.passwentry.delete(0, 'end')


class PageOne(tk.Frame):
    def __init__(self, parent, pagecontroll, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page One', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Home', command=lambda: pagecontroll.show_frame(StartPage, pages['StartPage']))
                                                                # likewise StartPage
        button1.pack()
        self.play = ttk.Button(self, text="Play")
        self.play.bind("<Button>", self.Daemon)
        self.play.pack()

    def Daemon(self, event):
        os.system("\"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe\" http://127.0.0.1:18000")