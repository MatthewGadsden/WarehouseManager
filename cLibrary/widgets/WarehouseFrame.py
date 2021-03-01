from tkinter import *
import tkinter.ttk as ttk
from cLibrary.guis.Controller import Controller


class WarehouseFrame(Frame):

    def __init__(self, master, *args, **kw):
        super(WarehouseFrame, self).__init__(master, *args, **kw)

    def get_controller(self) -> Controller:
        return self.master.get_controller()
