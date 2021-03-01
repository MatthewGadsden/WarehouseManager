from cLibrary.widgets.controlPanel.DispWidgetFrame import *
from cLibrary.widgets.controlPanel.SlotRow import SlotRow


class BIL(DispWidgetFrame):

    def __init__(self, master, warehouse, controller, height=50, width=200, bg="snow", fg="lime green", *args,
                 **kwargs):
        self.bg = bg
        self.fg = fg
        super().__init__(master, warehouse, controller, height=height, width=width, *args, **kwargs)

    def load_display(self):
        self.item_num = 20
        self.items = []

        self.hier_canvas = Canvas(self, width=self.winfo_reqwidth() - 5, height=self.winfo_reqheight() - 25)
        self.hier_frame = Frame(self.hier_canvas)

        self.scrollbar = Scrollbar(self.hier_canvas, orient="vertical", command=self.hier_canvas.yview)
        self.hier_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.hier_canvas.place(x=0, y=22)
        self.scrollbar.place(x=self.winfo_reqwidth() - 20, y=0, width=20, height=self.winfo_reqheight() - 22)

        self.canvas_frame = self.hier_canvas.create_window((0, 0), window=self.hier_frame, anchor="nw")

        self.hier_canvas.bind("<MouseWheel>", self.mouse_scroll)
        self.hier_frame.bind("<MouseWheel>", self.mouse_scroll)
        self.bind("<Configure>", self.on_frame_configure)

        update_button = Button(self, text="\uD83D\uDD04", bg="light green", font="bold 18",
                               command=lambda: self.update(), relief="groove")
        update_button.place(x=self.winfo_reqwidth() - 40, y=0, width=20, height=20)

        self.num_input = Entry(self, font="bold 10", relief="groove", bd=2, bg="white")
        self.num_input.place(x=self.winfo_reqwidth() - 40 - 40, y=0, width=40, height=20)
        self.num_input.insert(0, self.item_num)

        sel_num_label = Label(self, text="Num of Slots: ", bg="grey", relief="groove", fg="white")
        sel_num_label.place(x=self.winfo_reqwidth() - 40 - 40 - 100, y=0, width=100, height=20)

        self.update()

    def load_title(self):
        super(BIL, self).load_title()
        self.title['text'] = "Best Items List"
        self.title['bg'] = "light grey"
        self.title.place(y=0, x=0, width=self.winfo_reqwidth() - 40 - 40 - 100, height=20)

    def mouse_scroll(self, event):
        if event.delta:
            self.hier_canvas.yview_scroll(int(-1 * (event.delta / 100)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.hier_canvas.yview_scroll(move, "units")

    def on_frame_configure(self, event=None):
        self.hier_canvas.configure(scrollregion=self.hier_canvas.bbox(ALL))

    def update(self):
        super().update()
        while len(self.items) > 0:
            item = self.items.pop()
            item.destroy()

        self.item_num = int(self.num_input.get())

        slots = self.warehouse.get_best_avehitsday(self.item_num)
        row_val = 1
        y_val = 20
        for slot in slots:
            row = SlotRow(self.hier_frame, row_val, slot, width=self.hier_canvas.winfo_width() - 20, height=20)
            row.place(x=0, y=y_val)
            row.bind("<MouseWheel>", self.mouse_scroll)
            self.items.append(row)
            y_val += 20
            row_val += 1

        self.hier_frame.configure(width=self.hier_canvas.winfo_width(), height=y_val)

        for i in self.items:
            i.bind("<MouseWheel>", self.mouse_scroll)

        self.hier_frame.update()
        nw = row.numLabel.winfo_width()
        sw = row.tempLabel.winfo_width()
        iw = row.itemLabel.winfo_width()
        hw = row.hitsLabel.winfo_width()
        dhw = row.dayshitsLabel.winfo_width()
        aw = row.avgLabel.winfo_width()
        self.hier_canvas.update()
        self.hier_canvas.configure(scrollregion=self.hier_canvas.bbox(ALL))
        num_label = Label(self, text="#", bg="azure3", relief="groove")
        num_label.place(y=22, x=0, width=nw, height=20)
        slot_label = Label(self, text="Slot ID", bg="azure3", relief="groove")
        slot_label.place(y=22, x=nw, width=sw, height=20)
        item_label = Label(self, text="Item ID", bg="azure3", relief="groove")
        item_label.place(y=22, x=nw + sw, width=iw, height=20)
        hits_label = Label(self, text="Hits", bg="azure3", relief="groove")
        hits_label.place(y=22, x=nw + sw + iw, width=hw, height=20)
        day_hits_label = Label(self, text="Days Hit", bg="azure3", relief="groove")
        day_hits_label.place(y=22, x=nw + sw + iw + hw, width=dhw, height=20)
        avg_label = Label(self, text="Avg Hits / Day", bg="azure3", relief="groove")
        avg_label.place(y=22, x=nw + sw + iw + hw + dhw, width=aw, height=20)
        self.items.append(num_label)
        self.items.append(slot_label)
        self.items.append(item_label)
        self.items.append(hits_label)
        self.items.append(day_hits_label)
        self.items.append(avg_label)