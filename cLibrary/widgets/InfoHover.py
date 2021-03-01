from tkinter import *
from cLibrary.widgets.ToolTip import CreateToolTip


class InfoHover(Frame):
    def __init__(self, root, text, *args, **kwargs):
        super(InfoHover, self).__init__(root, *args, **kwargs)
        label = Label(self, text="     \u2139\uFE0F", bg="dodgerblue4", font="none 8", pady=0, borderwidth=0, fg="white")
        label.place(x=0, y=0, width=10, height=10)
        CreateToolTip(label, text)