from tkinter import *


class SlotRow(Frame):

    def __init__(self, master, index, slot, width, height, *args, **kwargs):
        super(SlotRow, self).__init__(master, *args, **kwargs)
        self.configure(width=width, height=height)
        self.parts = []
        self.numLabel = Label(self, text=str(index) + ". ", bg="white", relief="groove")
        self.numLabel.place(x=0, y=0, width=(4 / 37) * width, height=height)
        self.tempLabel = Label(self, text=slot.spot_id, bg="white", relief="groove")
        self.tempLabel.place(x=(4 / 37) * width, y=0, width=(5 / 37) * width, height=height)
        self.itemLabel = Label(self, text=slot.allocations[0].item.item_id, bg="white", relief="groove")
        self.itemLabel.place(x=(9 / 37) * width, y=0, width=(7 / 37) * width, height=height)
        self.hitsLabel = Label(self, text=slot.allocations[0].item.hits, bg="white", relief="groove")
        self.hitsLabel.place(x=(16 / 37) * width, y=0, width=(5 / 37) * width, height=height)
        self.dayshitsLabel = Label(self, text=slot.allocations[0].item.dayshit, bg="white", relief="groove")
        self.dayshitsLabel.place(x=(21 / 37) * width, y=0, width=(6 / 37) * width, height=height)
        self.avgLabel = Label(self, text=slot.allocations[0].item.avehitsday, bg="white", relief="groove")
        self.avgLabel.place(x=(27 / 37) * width, y=0, width=(10 / 37) * width, height=height)
        self.parts += [self.numLabel, self.tempLabel, self.itemLabel, self.hitsLabel, self.dayshitsLabel, self.avgLabel]

    def bind(self, sequence=None, func=None, add=None):
        super().bind(sequence, func, add)
        for i in self.parts:
            i.bind(sequence, func, add)