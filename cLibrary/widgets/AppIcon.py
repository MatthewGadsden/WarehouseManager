from tkinter import *
from cLibrary.widgets.ToolTip import CreateToolTip
from PIL import ImageTk, Image


class AppIcon(Frame):

    def __init__(self, master, window, **kwargs):
        """
        Icon for opening a task bar app in MGSS
        :param master: master window
        :param img: icon image
        :param window: window that icon opens
        :param kwargs: style arguments
        """
        super(AppIcon, self).__init__(master)

        # initialize keyword argument values
        bg = kwargs['bg'] if kwargs.get('bg') is not None else 'dark grey'
        name = kwargs['name'] if kwargs.get('name') is not None else 'testing'
        width = kwargs['width'] if kwargs.get('width') is not None else 25
        height = kwargs['height'] if kwargs.get('height') is not None else 25
        self.img = kwargs['img'] if kwargs.get('img') is not None else None

        # check value types
        if not isinstance(width, int): raise TypeError("width must be of type Integer")
        if not isinstance(height, int): raise TypeError("height must be of type Integer")
        if not isinstance(name, str): raise TypeError("name must be of type String")
        if not isinstance(bg, str): raise TypeError("bg must be of type String")

        if self.img is not None:
            self.img = Image.open(self.img).resize((width-5, width-5), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)

        osa = Button(self, image=self.img, anchor="n", bg=bg, bd=1, command=lambda: self.open_window(window))
        self.configure(width=width, height=height)
        osa.configure(width=width-5, height=height-5)
        osa.place(x=0, y=0)
        CreateToolTip(osa, name, c_off=width-15)

    def open_window(self, window):
        self.master.root_menu.entryconfig("File", state="disabled")
        self.master.root_menu.entryconfig("Edit", state="disabled")
        self.master.root_menu.entryconfig("View", state="disabled")
        self.master.root_menu.entryconfig("Stock", state="disabled")
        self.master.wait_window(window(self.master.controller.container,
                                       self.master.controller))
        try:
            self.master.root_menu.entryconfig("Edit", state="normal")
            self.master.root_menu.entryconfig("File", state="normal")
            self.master.root_menu.entryconfig("View", state="normal")
            self.master.root_menu.entryconfig("Stock", state="normal")
        except TclError:
            pass