from cLibrary.guis.MainWindow import MGSlotSystem


if __name__ == '__main__':
    win = MGSlotSystem("resources/source/item.csv", "resources/source/slot.csv", "resources/source/itmslot.csv", "resources/source/hits.csv")
    win.mainloop()
