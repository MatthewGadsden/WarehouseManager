from tkinter import *
from cLibrary.widgets.Output import Output


class WinOutput(Output):

    def __init__(self, master, width, height, x, y, *args, **kwargs):
        super(WinOutput, self).__init__(master, *args, **kwargs)
        self.title = Label(self.master, text="Output")
        self.title.place(x=x, y=y, width=width, height=30)
        self.place(x=x, y=y+30, width=width, height=height-30)
