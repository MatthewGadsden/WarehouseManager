from tkinter.ttk import *
from tkinter import *
from tkinter.filedialog import *


class WidgetWindow(Frame):

    def __init__(self, master, controller):
        """
        Overarching class for a standard widget window template
        :param master: master window / frame
        :param controller: program controller
        """
        super(WidgetWindow, self).__init__(master)
        self.controller = controller
        self.warehouse = controller.warehouse
        self.configure(width=controller.wig_width, height=controller.wig_height, bg="dark grey")
        self.title = Label(self)
        self.load_title()
        self.load_display()
        self.load_close_button()

        self.place(x=0, y=0)
        self.grab_set()

    def load_title(self, text="Generic Dash Widget", bg="burlywood1", relief="groove"):
        """
        loading widget title
        :return: None
        """
        self.title['text'] = text
        self.title['bg'] = bg
        self.title['relief'] = relief
        self.title.place(x=0, y=0, width=self.controller.wig_width-30, height=30)

    def get_controller(self):
        return self.controller

    def load_display(self):
        """
        load widget display
        :return: None
        """
        wip_text = Label(self, text="Work In Progress\n(Not Ready Yet)", font="bold 20", relief="groove")
        wip_text.place(x=self.winfo_reqwidth()/2-200, y=self.winfo_reqheight()/2 - 75, width=400, height=150)
        pass

    def load_close_button(self):
        """
        load close button for widget
        :return: None
        """
        self.close_but = Button(self, command=self.on_close)
        self.close_but['text'] = "X"
        self.close_but['bg'] = "coral1"
        self.close_but['relief'] = "groove"
        self.close_but.place(x=self.controller.wig_width - 30, y=0, width=30, height=30)

    def on_close(self):
        """
        close widget protocol
        :return:
        """
        self.destroy()