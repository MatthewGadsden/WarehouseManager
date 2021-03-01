from tkinter import *
from cLibrary.widgets.controlPanel.HexColour import HexColour


class TimeGradient(Frame):
    def __init__(self, master, warehouse, **kwargs):
        super().__init__(master)
        self.width = width = kwargs['width'] if kwargs.get('width') is not None else 200
        self.height = height = kwargs['height'] if kwargs.get('height') is not None else 100
        self.color = HexColour(255, 0, 0)
        self.label = Label(self, text="Testing Gradients", bg=str(self.color), relief="groove")
        self.label.place(x=0, y=0, width=width, height=height)
        self.reverse = False
        self.update_clock()
        self.configure(width=width, height=height)

    def update_clock(self):
        if self.reverse:
            if self.color.get_red() == 255 and self.color.get_green() < 255:
                self.color._green += 1
            elif self.color.get_red() > 0 and self.color.get_green() == 255:
                self.color._red -= 1
            else:
                self.reverse = not self.reverse
        else:
            if self.color.get_red() < 255 and self.color.get_green() == 255:
                self.color._red += 1
            elif self.color.get_red() == 255 and self.color.get_green() > 0:
                self.color._green -= 1
            else:
                self.reverse = not self.reverse
        self.label.configure(bg=str(self.color))
        self.after(5, self.update_clock)