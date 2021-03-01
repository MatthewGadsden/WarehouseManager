from cLibrary.widgets.controlPanel.DispWidgetFrame import *
from cLibrary.widgets.ToolTip import CreateToolTip
from cLibrary.structure.warehouse.Warehouse import Warehouse


class RAFP(DispWidgetFrame):

    def __init__(self, master, warehouse, controller, height=50, width=200, bg="snow", fg="lime green", *args, **kwargs):
        if not isinstance(warehouse, Warehouse):
            raise TypeError("warehouse must be of Type Warehouse")
        self.bg = bg
        self.fg = fg
        super().__init__(master, warehouse, controller, height=height, width=width, *args, **kwargs)

    def load_title(self):
        super(RAFP, self).load_title()
        self.title['text'] = "Aisle Reserve Slot Fill Display"
        self.title['bg'] = "MediumOrchid4"
        self.title['fg'] = "snow"

    def load_display(self):
        ta = 0
        max_slots = 0
        empty = []
        filled = []
        aisles = []
        for aisle in self.warehouse:
            reserves = aisle.get_reserve_slots()
            if len(reserves) > 0:
                e = 0
                for slot in reserves:
                    if not slot.items:
                        e += 1
                f = len(reserves) - e
                empty.append(e)
                filled.append(f)
                aisles.append(aisle)
                if e + f > max_slots:
                    max_slots = e + f
                ta += 1

        x_val = 0
        y_val = 20
        w = self.winfo_reqwidth() // ta
        h = self.winfo_reqheight() - 42
        for _ in range(len(empty)):
            e = empty[_]
            f = filled[_]
            t = e + f

            t_ratio = ((t / max_slots) * (h - 1)) // 1
            f_ratio = ((f / max_slots) * (h - 1)) // 1

            frame = Frame(self, bg=self.bg, relief="solid")
            frame.place(x=x_val + 1, y=y_val + h - t_ratio - 1, width=w - 2, height=t_ratio + 2)

            border = Label(frame, bg=self.bg, relief="solid")
            border.place(x=0, y=0, width=w - 2, height=t_ratio + 2)

            background = Label(frame, bg=self.bg, relief="flat")
            background.place(x=1, y=1, width=w - 4, height=t_ratio)

            filled_graphic = Label(frame, bg=self.fg, relief="flat")
            filled_graphic.place(x=1, y=(t_ratio - f_ratio) + 1, width=w - 4, height=f_ratio)

            text = Label(self, text=aisles[_].aisle, relief="groove")
            text.place(x=x_val, y=h + 20 + 2, width=w, height=20)

            CreateToolTip(frame, "{} / {}".format(f, t), c_off=(-15 + w))

            x_val += w