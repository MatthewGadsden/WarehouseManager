from tkinter import *
from cLibrary.widgets.controlPanel.DashWig import DashWig


class DashGrid(Frame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.configure(width=controller.wig_width, height=controller.wig_height)
        self.place(x=0, y=0)
        self.controller = controller

        self.dash_wigs = []
        self.wig_cols = controller.wigs_w
        self.wig_rows = controller.wigs_h

        self.wig_height = (controller.wig_height - (5 * (controller.wigs_h - 1))) / self.wig_rows
        self.wig_width = (controller.wig_width - (5 * (controller.wigs_w - 1))) / self.wig_cols

        y_val = 0
        for i in range(self.wig_rows):
            x_val = 0
            for j in range(self.wig_cols):
                cur_wig = DashWig(self, self.controller, width=self.wig_width, height=self.wig_height)
                cur_wig.place(x=x_val, y=y_val)
                self.dash_wigs.append(cur_wig)
                x_val += self.wig_width + 5
            y_val += self.wig_height + 5

    def __iter__(self):
        return ListIterator(len(self.dash_wigs), self.dash_wigs)

class ListIterator:
    def __init__(self, length, list):
        self.list = list
        self.length = length
        self.count = 0

    def __next__(self):
        if self.count >= self.length:
            raise StopIteration
        else:
            item = self.list[self.count]
            self.count += 1
            return item

    def __iter__(self):
        return self