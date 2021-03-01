from tkinter import *


class Output(Text):

    def __init__(self, master, *args, **kwargs):
        super(Output, self).__init__(master, *args, **kwargs)
        self.configure(state="disabled")

    def r_insert(self, text):
        self.configure(state="normal")
        self.delete(0.0, END)
        self.insert(END, text)
        self.configure(state="disabled")
        self.update()

    def i_insert(self, text):
        self.configure(state="normal")
        self.insert(END, text)
        self.configure(state="disabled")
        self.update()