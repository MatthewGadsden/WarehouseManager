from tkinter import *
from cLibrary.widgets.controlPanel.HexColour import HexColour


class DSP(Frame):

    def __init__(self, master, pickslot, width=100, height=20):
        super().__init__(master)
        self.avehitsday = 0
        id = 0
        best_hits = pickslot.warehouse.get_best_hits()

        if not pickslot.allocations:
            pass
        else:
            self.avehitsday = pickslot.get_item_avehitsday()
            id = pickslot.allocations[0].item.item_id

        OldRange = (best_hits - 0)
        NewRange = (255 - 0)
        NewValue = (((self.avehitsday - 0) * NewRange) / OldRange) // 1

        self.color = HexColour(255, 255 - int(NewValue), 0)

        label = Label(self, text=id, bg=str(self.color))
        label.place(x=0,y=0, width=width, height=height)
        self.configure(width=width, height=height)