from cLibrary.widgets.controlPanel.DispWidgetFrame import *


class WFP(DispWidgetFrame):
    """
    This is a graphic display of how full the warehouse is
    The green bar shown is how many full slots there are
    The grey bar behind is how many total slots there are
    """
    def __init__(self, master, warehouse, controller, height=50, width=200, bg="snow", fg="lime green", *args, **kwargs):
        self.bg = bg
        self.fg = fg
        super().__init__(master, warehouse, controller, height=height, width=width, *args, **kwargs)

    def load_title(self):
        super(WFP, self).load_title()
        self.title['text'] = "PickSlot Warehouse Fill Display"

    def load_display(self):
        h = self.winfo_reqheight() - 60
        empty = self.warehouse.get_empty_pick_slots_count()
        filled = self.warehouse.get_filled_pick_slots_count()
        total = empty + filled
        title_str = "Filled Slots / Total Slots\n" + str(filled) + " / " + str(total)
        label = Label(self, text=title_str, bg="white", fg="black", relief="groove")
        label.place(y=h + 20, width=self.winfo_reqwidth(), height=40)

        filled_ratio = (filled / total * self.winfo_reqwidth()) // 1
        background = Label(self, bg=self.bg, relief="groove")
        background.place(width=self.winfo_reqwidth(), height=h, y=20)
        filled_graphic = Label(self, bg=self.fg)
        filled_graphic.place(x=2, y=2 + 20, width=filled_ratio, height=h - 5)