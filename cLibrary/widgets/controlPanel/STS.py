from cLibrary.widgets.controlPanel.DispWidgetFrame import *
from cLibrary.methods.AreaMethods import dayxhits_sort_1_4
from cLibrary.widgets.ToolTip import CreateToolTip


class STS(DispWidgetFrame):

    def load_title(self):
        super().load_title()
        self.title['text'] = "Slots To Swap"
        self.title['bg'] = "orange"

    def load_display(self):
        ta = 0
        max_slots = 0
        empty = []
        aisles = []
        for area in self.controller.areas.values():
            e = len(dayxhits_sort_1_4(area))
            if e > 0:
                empty.append(e)
                aisles.append(area)
                ta += 1
            if e > max_slots:
                max_slots = e

        x_val = 0
        y_val = 20

        if ta == 0:
            return

        w = self.winfo_reqwidth() // ta
        h = self.winfo_reqheight() - 42
        for _ in range(len(empty)):
            e = empty[_]

            t_ratio = ((e / max_slots) * (h - 1)) // 1

            border = Label(self, relief="solid")
            border.place(x=x_val + 1, y=y_val + h - t_ratio - 1, width=w - 2, height=t_ratio + 2)

            background = Label(self, relief="flat", bg="light blue")
            background.place(x=x_val + 2, y=y_val + h - t_ratio, width=w - 4, height=t_ratio)

            CreateToolTip(background, "{}".format(e), c_off=(-15 + w))

            text = Label(self, text=aisles[_].area_name, relief="groove")
            text.place(x=x_val, y=h + 20 + 2, width=w, height=20)

            x_val += w