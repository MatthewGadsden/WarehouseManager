from tkinter import *
from cLibrary.widgets.ToolTip import CreateToolTip
from cLibrary.widgets.controlPanel.HexColour import HexColour


class BAD(Frame):

    def __init__(self, master, warehouse, controller, height=50, width=200, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.warehouse = warehouse
        self.width = width
        self.height = height
        self.h = height
        self.y_val = 0
        self.x_val = 0
        self.configure(width=width, height=height)

        self.title = Label(self, text="Best Aisles PickSlot Display", bg="CadetBlue1", relief="groove")
        self.title.place(x=0, y=0, width=self.width, height=20)
        self.h -= 40
        self.y_val += 20

        hits = []
        best = 0
        for aisle in self.warehouse:
            hit = aisle.get_average_hits()
            if hit > 0:
                hits.append((aisle.aisle, hit))
            if hit > best:
                best = hit

        self.w = (self.width/len(hits))//1

        for hit in hits:
            filled_ratio = (hit[1] / best * self.h) // 1
            OldRange = (best - 0)
            NewRange = (255 - 0)
            NewValue = (((hit[1] - 0) * NewRange) / OldRange) // 1

            self.color = HexColour(255, 255 - int(NewValue), 0)

            tempLabel = Label(self, bg=str(self.color), relief="groove")
            tempLabel.place(x=self.x_val, y=self.y_val+self.h-filled_ratio, width=self.w, height=filled_ratio)

            CreateToolTip(tempLabel, "avg hits / day: {}".format(round(hit[1], 3)), c_off=(-15 + self.w))

            text = Label(self, text=hit[0], relief="groove")
            text.place(x=self.x_val, y=self.h + 20, width=self.w, height=20)
            self.x_val += self.w