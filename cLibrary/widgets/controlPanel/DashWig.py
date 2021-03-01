from tkinter import *
from tkinter.ttk import Combobox
from cLibrary.widgets.ToolTip import CreateToolTip
from cLibrary.widgets.controlPanel.BAD import BAD
from cLibrary.widgets.controlPanel.AFP import AFP
from cLibrary.widgets.controlPanel.BAIL import BAIL
from cLibrary.widgets.controlPanel.BIL import BIL
from cLibrary.widgets.controlPanel.STS import STS
from cLibrary.widgets.controlPanel.DSP import DSP
from cLibrary.widgets.controlPanel.WFP import WFP
from cLibrary.widgets.controlPanel.WRFP import WRFP
from cLibrary.widgets.controlPanel.TimeGradient import TimeGradient
from cLibrary.widgets.controlPanel.RAFP import RAFP


class DashWig(Frame):
    widget_dict = {"PickSlot Fill Percentage": AFP, "Warehouse Fill Percentage": WFP, "Best Items List": BIL,
                   "Time Gradient": TimeGradient, "Best Aisle Display": BAD, "Best Aisle Items List": BAIL,
                   "Reserve Fill Percentage": RAFP, "Warehouse Reserves Fill": WRFP, "Slots To Swap": STS}
    widget_dict_2 = {"AFP": AFP, "WFP": WFP, "BIL": BIL, "TimeGradient": TimeGradient, "BAD": BAD, "BAIL": BAIL,
                     "RAFP": RAFP, "WRFP": WRFP, "STS": STS,}

    widgets = ["PickSlot Fill Percentage", "Warehouse Fill Percentage",
               "Best Aisle Display", "Best Items List", "Best Aisle Items List",
               "Reserve Fill Percentage", "Warehouse Reserves Fill", "Slots To Swap"]

    def __init__(self, master, controller, width=100, height=100, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.current_widget_type = None
        self.current_type = None
        self.close_button = None
        self.fullscreen = False
        self.disp_widgets = []
        self.def_val = self.set_menu_val(self.widgets[0])
        self.bw = 2
        self.configure(width=width, height=height, bg="light grey", borderwidth=self.bw)
        self.og_w = width
        self.og_h = height
        self.width = width
        self.height = height
        self.og_x = None
        self.og_y = None
        self.clean()
        self.update()

    def choose_widget(self):
        while len(self.disp_widgets) > 0:
            temp = self.disp_widgets.pop()
            temp.destroy()
        self.comb = Combobox(self, textvariable=self.def_val, value=self.widgets, state="readonly")
        self.comb.place(width=(self.width/2.2)//1, height=30, x=(self.width//2)-((self.width/4.4)//1)-self.bw, y=self.height//2 - 45)
        ok_but = Button(self, text="OK", bg="lawn green", command=lambda:self.disp_wid(self.widget_dict[self.comb.get()]))
        ok_but.place(width=(self.width/2.2)//1, height=30, x=(self.width//2)-((self.width/4.4)//1)-self.bw, y=self.height//2-15)
        cancel_but = Button(self, text="Cancel", bg="grey90",
                        command=lambda: self.clean())
        cancel_but.place(width=(self.width / 2.2) // 1, height=30,
                     x=(self.width // 2) - ((self.width / 4.4) // 1) - self.bw, y=self.height // 2+15)

        self.disp_widgets.append(self.comb)
        self.disp_widgets.append(ok_but)
        self.disp_widgets.append(cancel_but)

    def set_menu_val(self, x):
        val = StringVar(self)
        val.set(x)  # default value
        return val

    def disp_wid(self, type=None):
        if type is not None:
            self.current_widget_type = type.__name__
            self.current_type = type
        while len(self.disp_widgets) > 0:
            temp = self.disp_widgets.pop()
            temp.destroy()
        widget = self.current_type(self, warehouse=self.controller.warehouse, controller=self.controller, width=self.width-4, height=self.height-4)
        widget.place(x=0, y=0)
        self.close_button = Button(self, text="X", bg="coral1", command=self.clean, relief="groove")
        self.close_button.place(width=20, height=20, x=self.width-24, y=0)

        CreateToolTip(self.close_button, "Close", c_off=10)

        widget.title.bind('<Double-Button-1>', lambda e: self.full_screen())
        if not self.fullscreen:
            widget.title.unbind_all("<Escape>")
        else:
            widget.title.bind_all("<Escape>", self.full_screen)
        self.disp_widgets.append(widget)
        self.disp_widgets.append(self.close_button)

    def full_screen(self, event=None):
        self.fullscreen = not self.fullscreen
        if not self.fullscreen:
            self.width = self.og_w
            self.height = self.og_h
            self.configure(height=self.height, width=self.width)
            self.disp_wid()
            self.place(x=self.og_x, y=self.og_y)
        else:
            self.width = self.controller.container.winfo_width()
            self.height = self.controller.container.winfo_height()
            self.configure(height=self.height, width=self.width)
            self.lift()
            self.disp_wid()
            self.og_x = self.winfo_x()
            self.og_y = self.winfo_y()
            self.place(x=0, y=0)

    def clean(self):
        if self.fullscreen:
            self.full_screen()
        else:
            self.current_widget_type = None
            for widget in self.winfo_children():
                widget.destroy()
            self.default_display()

    def default_display(self):
        add_button = Button(self, text="+", anchor="center", bg="orange", fg="white", font="bold",
                            command=lambda: self.choose_widget())
        add_button.place(width=30, height=30, x=self.width // 2 - 15 - self.bw, y=self.height // 2 - 15 - self.bw)

        CreateToolTip(add_button, "Add New Widget", c_off=20)

        self.disp_widgets.append(add_button)
        self.update()

    def load_widget(self, type):
        self.disp_wid(self.widget_dict_2[type])