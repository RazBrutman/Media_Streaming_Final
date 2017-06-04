import Tkinter as tk
from Tkinter import *
import tkFileDialog
import ttk
from ttk import *


STREAMER_FONT = ("Chaparral Pro", 26)
LARGE_FONT = ("Calibri", 22)
SMALL_FONT = ("Calibri", 12)

BACKGROUND1 = "#F38181"
FOREGROUND1 = "#EAFFD0"

BACKGROUND2 = "#FCE38A"
FOREGROUND2 = BACKGROUND1

BACKGROUND3 = "#EAFFD0"
FOREGROUND3 = BACKGROUND1

BUTTON_BG = "#95E1D3"
BUTTON_FG = "#2e544d"

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
        entry = frame.userentry.get()
        if entry:
            import re
            if not re.match("^[a-zA-Z0-9_]*$", entry) or len(entry) > 10:
                frame.invalid.pack()
            else:
                self.username = self.controller.user_exists(entry)
                self.start_main_page(frame)
                frame.invalid.pack_forget()
        frame.userentry.delete(0, 'end')

    def start_main_page(self, frame):
        page_2 = MainUserPage(self.container, self, self.controller, frame.userentry.get())
        self.frames[MainUserPage] = page_2
        page_2.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainUserPage, pages['MainUserPage'])


class StartPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller):

        tk.Frame.__init__(self, parent, background=BACKGROUND1)  # constructs frame

        self.controller = controller
        self.pagecontrol = pagecontrol

        label = ttk.Label(self, text="Welcome to Streamer", background=BACKGROUND1, foreground=FOREGROUND1,
                          font=STREAMER_FONT)
        label.pack(pady=(30, 10))
        info = tk.Frame(self, background=BACKGROUND1)
        user = ttk.Label(info, text="Username", background=BACKGROUND1, font=SMALL_FONT, foreground=FOREGROUND1)
        user.grid(row=0, sticky="w")
        self.userentry = ttk.Entry(info, font=SMALL_FONT)
        self.userentry.grid(row=1)
        self.invalid = ttk.Label(self, text="Invalid Username!", background=BACKGROUND1, foreground="red")
        self.sub = tk.Button(info, text="Submit", background=BUTTON_BG, foreground=BUTTON_FG,
                             relief=tk.FLAT, width=10,
                             command=lambda: self.pagecontrol.validate_username(self))
        self.sub.grid(row=4, pady=30)
        info.pack(pady=10)


class MainUserPage(tk.Frame):

    def __init__(self, parent, pagecontrol, controller, username):

        tk.Frame.__init__(self, parent)  # constructs frame

        self.username = username

        self.controller = controller
        self.pagecontrol = pagecontrol

        top = tk.Frame(self, width=650, height=40, background="orange")
        top.grid_propagate(0)
        choices = []
        all_users = self.controller.get_all(username)
        for user in all_users:
            choices.append(user.username)
        self.tkvar = StringVar(top)
        self.tkvar.set(choices[0])
        popupMenu = OptionMenu(top, self.tkvar, choices[0], *choices)
        popupMenu.config(width=8)
        Label(top, text="add friend:", font=SMALL_FONT, background="orange").grid(row=0, column=0)
        popupMenu.grid(row=0, column=1, pady=10, padx=15)
        f_button = tk.Button(top, text="Select", background=BUTTON_BG, foreground=BUTTON_FG, relief=FLAT,
                             command=lambda: self.edit_friend(self.tkvar.get(), False))
        f_button.grid(row=0, column=2)
        top.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.right = tk.Frame(self, width=200, height=360)

        self.top_right = VerticalScrolledFrame(self.right)
        self.top_right.interior.config(width=200, height=260, background="blue")
        friends = self.update_friends()
        self.top_right.grid(row=0, column=0, sticky="ew")

        self.bottom_right = tk.Frame(self.right, width=200, height=100, background="yellow")
        self.bottom_right.pack_propagate(0)
        home = tk.Button(self.bottom_right, text='Back to Home', background=BUTTON_BG, foreground=BUTTON_FG,
                            relief=FLAT, width=14,
                            command=lambda: pagecontrol.show_frame(StartPage, pages['StartPage']))
        home.pack(pady=15)
        add = tk.Button(self.bottom_right, text="Add shared media", background=BUTTON_BG, foreground=BUTTON_FG,
                        relief=FLAT, width=14,
                        command=self.add_file)
        add.pack()
        self.bottom_right.grid(row=1, column=0, sticky="ew")

        self.right.grid(row=1, column=1, sticky="nsew")

        self.left = tk.Frame(self, width=450, height=360, background="green")
        self.left.pack_propagate(0)
        self.info = ttk.Label(self.left, text="No friends yet :(", font=LARGE_FONT, background=BACKGROUND2,
                              foreground=FOREGROUND2)
        if friends:
            self.info['text'] = "Click on name to view files..."
        self.info.pack(fill="none", expand=True, anchor="nw", pady=30, padx=30)
        self.left.grid(row=1, column=0)

        self.remove_menu = tk.Menu(self, tearoff=0)
        self.remove_menu.add_command(label="Remove friend", command=self.remove_friend)

    def popup(self, event):
        global selected
        self.remove_menu.post(event.x_root, event.y_root)
        selected = event.widget

    def remove_friend(self):
        self.edit_friend(selected["text"], True)

    def edit_friend(self, other_name, to_remove):
        self.controller.edit_relationship(self.pagecontrol.username, other_name, to_remove)
        self.update_friends()

    def update_friends(self):
        for child in self.top_right.interior.winfo_children():
            child.destroy()
        friends = self.controller.validate(self.username)
        for user in friends:
            l = ttk.Label(self.top_right.interior, text=user.username, font=SMALL_FONT, background="blue",
                          foreground=FOREGROUND1)
            l.bind("<Button-1>", lambda event, data=user: self.test(event, data))
            l.bind("<Button-3>", self.popup)
            l.pack(side="top", pady=10)
        return friends

    def add_file(self):
        file_path = tkFileDialog.askopenfilename(initialdir="/",
                                                 title="Select file",
                                                 filetypes=(("jpeg files", "*.mp3;*.mp4"), ("all files", "*.*")))
        if file_path:
            self.controller.add_path(file_path, self.pagecontrol.username)

    def test(self, event, user):
        file_list = self.controller.user_files(user.username)
        for child in self.left.winfo_children():
                child.destroy()
        files = file_list.split(" ")
        files_frame = tk.Frame(self.left, background=BACKGROUND2)
        ttk.Label(self.left, text='Shared files', font=LARGE_FONT, background=BACKGROUND2,
                  foreground=FOREGROUND2).pack(anchor="nw", pady=30, padx=30)
        if files[0] != "":
            for element in files:
                shortened = []
                if element.split("/")[0] == element:
                    shortened = element.split("\\")[-1]
                else:
                    shortened = element.split("/")[-1]
                l = (ttk.Label(files_frame, text=shortened, font=SMALL_FONT, background=BACKGROUND2,
                               foreground=FOREGROUND2), element)
                l[0].bind("<Button>", lambda e=event, u=user, p=l[1]: self.controller.daemon(e, u, p))
                l[0].pack(anchor="w")
        else:
            ttk.Label(files_frame, text="No files", font=SMALL_FONT, background=BACKGROUND2,
                      foreground=FOREGROUND2).pack(anchor="w")
        files_frame.pack(fill="none", expand=True, anchor="nw", padx=30, pady=30)


class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0, background=BACKGROUND1, yscrollcommand=vscrollbar.set)
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
