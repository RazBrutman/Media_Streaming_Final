import Tkinter as tk
import tkFileDialog
import ttk
from PIL import ImageTk, Image


LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Times New Roman", 11)


pages = dict(StartPage='400x300',
             MainUserPage='600x400')


class StreamerGUI(object):

    def __init__(self, root, controller):
        """
        Main class that switches between windows. Creates each page, then puts them inside a list.
        """

        self.root = root
        self.controller = controller

        self.username = ""

        self.container = tk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        self.container.grid_columnconfigure(0, weight=1)  # make the cell in grid cover the entire window
        self.frames = {}  # these are pages we want to navigate to

        page_1 = StartPage(self.container, self, controller)
        self.frames[StartPage] = page_1
        page_1.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage, pages['StartPage'])  # let the first page be StartPage

    def show_frame(self, name, size):
        self.root.geometry(size)
        frame = self.frames[name]
        frame.tkraise()

    def validate_username(self, frame):
        username = frame.userentry.get()
        if username:
            import re
            if not re.match("^[a-zA-Z0-9_]*$", username):
                frame.invalid.pack()
            else:
                self.username = username
                self.start_main_page(frame)
                frame.userentry.delete(0, 'end')
                frame.invalid.pack_forget()

    def start_main_page(self, frame):
        # friends = self.controller.validate(username)
        # if friends:
        page_2 = MainUserPage(self.container, self, self.controller, frame.userentry.get())
        self.frames[MainUserPage] = page_2
        page_2.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainUserPage, pages['MainUserPage'])


class StartPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller):

        tk.Frame.__init__(self, parent)  # constructs frame

        self.controller = controller
        self.pagecontrol = pagecontrol

        label = ttk.Label(self, text="Welcome to Streamer!", font=LARGE_FONT)
        label.pack(pady=(30, 10))
        info = tk.Frame(self)
        user = ttk.Label(info, text="Username:", font=SMALL_FONT)
        user.grid(row=0)
        self.userentry = ttk.Entry(info)
        self.userentry.grid(row=1)
        self.invalid = ttk.Label(self, text="Invalid Username!", font=SMALL_FONT, foreground="red")
        self.sub = ttk.Button(info, text="Submit",
                              command=lambda: self.pagecontrol.validate_username(self))
        self.sub.grid(row=2, pady=10)
        info.pack(pady=10)
        # self.new = ttk.Button(buttons, text="Create new account",
        #                       command=lambda: pagecontroll.show_frame(PageOne, pages['PageOne']))
        # self.new.grid(row=1, pady=5)


class MainUserPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller, username):

        tk.Frame.__init__(self, parent)  # constructs frame

        self.controller = controller
        self.pagecontrol = pagecontrol

        self.right_frame = tk.Frame(self)
        friends = self.controller.validate(username)
        for user in friends:
            l = ttk.Label(self.right_frame, text=user.username, font=SMALL_FONT)
            l.bind("<Button>", lambda event, data=user: self.test(event, data))
            l.pack(side="top", pady=10)

        button1 = ttk.Button(self.right_frame, text='Back to Home',
                             command=lambda: pagecontrol.show_frame(StartPage, pages['StartPage']))
        button1.pack(side="bottom", pady=10)

        img = ImageTk.PhotoImage(Image.open("add_btn.png").resize((40, 40), Image.ANTIALIAS))
        add = ttk.Label(self.right_frame, text="I add", image=img)
        add.image = img
        add.pack(side="bottom", padx=20, pady=20)
        add.bind("<Button>", self.add_file)

        self.right_frame.pack(side=tk.RIGHT, padx=20, fill=tk.Y)

        self.left_frame = tk.Frame(self, bg="#888888")
        self.text_subframe = tk.Frame(self.left_frame)
        self.info = ttk.Label(self.text_subframe, text="No friends yet :(", font=LARGE_FONT, background="#888888")
        if friends:
            self.info['text'] = "Click on name to view files..."
        self.info.pack(fill="none", expand=True)
        self.text_subframe.pack()

        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def add_file(self, event):
        file_path = tkFileDialog.askopenfilename()
        print self.controller.add_path(file_path, self.pagecontrol.username)

    def test(self, event, user):
        file_list = self.controller.user_files(user.username)
        for child in self.left_frame.winfo_children():
                child.destroy()
        files = file_list.split(" ")
        files_frame = tk.Frame(self.left_frame, background="#888888")
        for element in files:
            l = ttk.Label(files_frame, text=element, font=SMALL_FONT, background="#888888")
            l.bind("<Button>", lambda e=event, u=user: self.controller.daemon(e, u))
            l.pack()
        files_frame.pack(fill="none", expand=True)