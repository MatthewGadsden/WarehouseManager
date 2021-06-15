from tkinter.ttk import Combobox
from cLibrary.methods.general import *
import PIL.ImageTk, PIL.Image, copy, shutil
from tkinter.filedialog import *
from cLibrary.guis.Controller import Controller
from typing import Union, Optional, Set, List
from tkinter import *


class StandardPopUp(Toplevel):

    def __init__(self, master, controller: Controller = None, width=230, height=220, title=None, cen_win=None, icon=None, *args, **kwargs):
        """
        Build standard Popup
        :param master: Master window
        :param controller: Data controller (used to access data)
        :param width: Width of popup
        :param height: Height of popup
        :param title: Title of popup
        :param cen_win: window to center on
        :param icon: Popup window icon
        :param args: Extra arguments
        :param kwargs: Keyword arguments
        """
        super(StandardPopUp, self).__init__(master, *args, **kwargs)
        self.load_config(width, height, cen_win, title, icon)
        self.config_loaded = False
        self.controller = controller    # type: Controller
        self.load_display()

    def load_config(self, width, height, master, title, icon):
        """
        Loading configuration for popup
        :param width: width of popup
        :param height: height of popup
        :param master: master of popup
        :param title: title for popup
        :param icon: icon for popup
        :return: None
        """
        self.configure(width=width, height=height)
        self.resizable(False, False)
        center_to_win(self, self.master) if not master else center_to_win(self, master)
        self.iconbitmap(icon) if not master else 'pass'
        self.title(title) if not master else 'pass'
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.config_loaded = True

    def load_display(self):
        """
        Load display of popup
        :return: None
        """
        pass

    def on_close(self):
        """
        Closing popup protocols
        :return: None
        """
        self.master.grab_set()
        self.destroy()