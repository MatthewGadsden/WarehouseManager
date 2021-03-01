from tkinter import *
from tkinter.ttk import Combobox


class DispWidgetFrame(Frame):

    def __init__(self, master, warehouse, controller, height=50, width=200, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.warehouse = warehouse
        self.controller = controller
        self.configure(width=width, height=height)

        self.title = Label(self)
        self.load_title()

        self.load_display()

    def load_title(self):
        self.title['text'] = "Generic Dash Widget"
        self.title['bg'] = "CadetBlue1"
        self.title['relief'] = "groove"
        self.title.place(x=0, y=0, width=self.winfo_reqwidth(), height=20)

    def load_display(self):
        pass