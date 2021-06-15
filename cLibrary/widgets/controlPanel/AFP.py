from cLibrary.widgets.controlPanel.DispWidgetFrame import *
from cLibrary.structure.warehouse.Warehouse import Warehouse
from cLibrary.structure.warehouse.Aisle import Aisle
from cLibrary.widgets.ToolTip import CreateToolTip
from typing import List, Set, Union, Optional


class AFP(DispWidgetFrame):

    def __init__(self, master, warehouse, controller, height=50, width=200, bg="snow", fg="lime green", *args, **kwargs):
        if not isinstance(warehouse, Warehouse):
            raise TypeError("warehouse must be of Type Warehouse")
        self.bg = bg
        self.fg = fg
        super().__init__(master, warehouse, controller, height=height, width=width, *args, **kwargs)

    def load_title(self):
        super(AFP, self).load_title()
        self.title['text'] = "Aisle PickSlot Fill Display"

    def load_display(self):
        max_slots = 0
        aisle_empty_filled = []  # type: List[Set[Aisle, int, int]]
        for aisle in self.warehouse:
            e = aisle.get_empty_pick_slots_count()
            f = aisle.get_filled_pick_slots_count()
            if e+f > 0:
                aisle_empty_filled.append((aisle, e, f))
            if e + f > max_slots:
                max_slots = e + f
        aisle_empty_filled.sort(key=lambda x:x[0].spot_id)
        ta = len(aisle_empty_filled)
        x_val = 0
        y_val = 20
        w = self.winfo_reqwidth() // ta
        h = self.winfo_reqheight() - 42
        for aisle, empty_n, filled_n in aisle_empty_filled:
            t = empty_n + filled_n

            t_ratio = ((t / max_slots) * (h - 1)) // 1
            f_ratio = ((filled_n / max_slots) * (h - 1)) // 1

            frame = Frame(self, bg=self.bg, relief="solid")
            frame.place(x=x_val + 1, y=y_val + h - t_ratio - 1, width=w - 2, height=t_ratio + 2)

            border = Label(frame, bg=self.bg, relief="solid")
            border.place(x=0, y=0, width=w - 2, height=t_ratio + 2)

            background = Label(frame, bg=self.bg, relief="flat")
            background.place(x=1, y=1, width=w - 4, height=t_ratio)

            filled_graphic = Label(frame, bg=self.fg, relief="flat")
            filled_graphic.place(x=1, y=(t_ratio - f_ratio) + 1, width=w - 4, height=f_ratio)

            text = Label(self, text=aisle.aisle, relief="groove")
            text.place(x=x_val, y=h + 20 + 2, width=w, height=20)

            CreateToolTip(frame, "{} / {}".format(filled_n, t), c_off=(-15+w))

            x_val += w
