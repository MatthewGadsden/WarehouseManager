from tkinter import *
import time


class Clock(Frame):
    def __init__(self, master, width=50, height=20):
        self.show_colon = True
        super().__init__(master)
        self.label = Label(self, text=time.strftime("%H:%M"), bg="snow", relief="groove")
        self.label.place(x=0, y=0, width=width, height=height)
        self.configure(width=width, height=height)
        self.up_clock()

    def up_clock(self):
        if self.show_colon:
            self.label.configure(text=time.strftime("%H:%M"))
            self.after(600, self.up_clock)
            self.show_colon = False
        else:
            self.label.configure(text=time.strftime("%H %M"))
            self.after(600, self.up_clock)
            self.show_colon = True