import Tkinter as tk
from Tkinter import *
import tkFileDialog
import ttk
from ttk import *


STREAMER_FONT = ("Chaparral Pro", 26)
LARGE_FONT = ("Calibri", 22)
SMALL_FONT = ("Chaparral Pro", 14)
SMALLER_FONT = ("Calibri", 12)
BG_COLOR = "#888888"

pages = dict(StartPage='400x300',
             MainUserPage='650x400')


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
        username = self.controller.user_exists(frame.userentry.get())
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
        page_2 = MainUserPage(self.container, self, self.controller, frame.userentry.get())
        self.frames[MainUserPage] = page_2
        page_2.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainUserPage, pages['MainUserPage'])


class StartPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller):

        tk.Frame.__init__(self, parent)  # constructs frame

        self.controller = controller
        self.pagecontrol = pagecontrol

        label = ttk.Label(self, text="Welcome to Streamer", font=STREAMER_FONT)
        label.pack(pady=(30, 10))
        info = tk.Frame(self)
        user = ttk.Label(info, text="Username", font=SMALL_FONT)
        user.grid(row=0, sticky="w")
        self.userentry = ttk.Entry(info, font=SMALLER_FONT)
        self.userentry.grid(row=1)
        self.invalid = ttk.Label(self, text="Invalid Username!", foreground="red")
        self.sub = ttk.Button(info, text="Submit",
                              command=lambda: self.pagecontrol.validate_username(self))
        self.sub.grid(row=2, pady=10)
        info.pack(pady=10)


class MainUserPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller, username):

        tk.Frame.__init__(self, parent)  # constructs frame

        self.username = username

        self.controller = controller
        self.pagecontrol = pagecontrol

        top_frame = tk.Frame(self)

        choices = []
        all_users = self.controller.get_all(username)
        for user in all_users:
            choices.append(user.username)
        self.tkvar = StringVar(top_frame)
        self.tkvar.set(choices[0])
        popupMenu = OptionMenu(top_frame, self.tkvar, choices[0], *choices)
        Label(top_frame, text="add friend:").pack(side="left")
        popupMenu.pack(side="left")
        f_button = ttk.Button(top_frame, text="Select", command=self.add_friend)
        f_button.pack(side="left")
        top_frame.pack(anchor="nw")

        self.right_frame = tk.Frame(self)

        self.top_right_frame = VerticalScrolledFrame(self.right_frame)

        friends = self.controller.validate(username)
        for user in friends:
            l = ttk.Label(self.top_right_frame.interior, text=user.username, font=SMALL_FONT)
            l.bind("<Button>", lambda event, data=user: self.test(event, data))
            l.pack(side="top", pady=10)

        self.bottom_right_frame = tk.Frame(self.right_frame)
        button1 = ttk.Button(self.bottom_right_frame, text='Back to Home',
                             command=lambda: pagecontrol.show_frame(StartPage, pages['StartPage']))
        button1.pack(side="bottom", pady=10)

        add = ttk.Button(self.bottom_right_frame, text="Add shared media", command=self.add_file)
        add.pack(side="bottom", padx=20, pady=20)

        self.top_right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_right_frame.pack(side=tk.BOTTOM)

        self.right_frame.pack(side=tk.RIGHT)

        self.left_frame = tk.Frame(self, bg="#888888")

        self.info = ttk.Label(self.left_frame, text="No friends yet :(", font=LARGE_FONT, background=BG_COLOR)
        if friends:
            self.info['text'] = "Click on name to view files..."
        self.info.pack(fill="none", expand=True, anchor="nw", pady=30, padx=30)

        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def add_friend(self):
        self.controller.befriend(self.pagecontrol.username, self.tkvar.get())
        self.update_friends()

    def update_friends(self):
        friends = self.controller.validate(self.username)
        for user in friends:
            add = True
            for child in self.top_right_frame.interior.winfo_children():
                if child['text'] == user.username:
                    add = False
            if add:
                l = ttk.Label(self.top_right_frame.interior, text=user.username, font=SMALL_FONT)
                l.bind("<Button>", lambda event, data=user: self.test(event, data))
                l.pack(side="top", pady=10)

    def add_file(self):
        file_path = tkFileDialog.askopenfilename(initialdir="/",
                                                 title="Select file",
                                                 filetypes=(("jpeg files", "*.mp3;*.mp4"), ("all files", "*.*")))
        if file_path:
            self.controller.add_path(file_path, self.pagecontrol.username)

    def test(self, event, user):
        file_list = self.controller.user_files(user.username)
        for child in self.left_frame.winfo_children():
                child.destroy()
        files = file_list.split(" ")
        files_frame = tk.Frame(self.left_frame, background=BG_COLOR)
        ttk.Label(self.left_frame, text='Shared files', font=LARGE_FONT, background=BG_COLOR)\
            .pack(anchor="nw", pady=30, padx=30)
        if files[0] != "":
            for element in files:
                shortened = []
                if element.split("/")[0] == element:
                    shortened = element.split("\\")[-1]
                else:
                    shortened = element.split("/")[-1]
                l = (ttk.Label(files_frame, text=shortened, font=SMALL_FONT, background=BG_COLOR), element)
                l[0].bind("<Button>", lambda e=event, u=user, p=l[1]: self.controller.daemon(e, u, p))
                l[0].pack(anchor="w")
        else:
            ttk.Label(files_frame, text="No files", font=SMALL_FONT, background=BG_COLOR).pack(anchor="w")
        files_frame.pack(fill="none", expand=True, anchor="nw", padx=30, pady=30)


class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)