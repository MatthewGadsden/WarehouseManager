from cLibrary.methods.general import *
import PIL.ImageTk, PIL.Image, copy, shutil
from tkinter.filedialog import *
from cLibrary.guis.popups.ErrorWindow import ErrorWindow
from cLibrary.widgets.InfoHover import InfoHover


class ChooseNewWarehouse(Toplevel):

    def __init__(self, master):
        """
        Initialise New Warehouse Popup window
        :param master: master window
        """
        super(ChooseNewWarehouse, self).__init__(master)
        self.transient(master)
        title = Label(self, text="Create New Warehouse", font="bold 22", fg="grey26")
        title.place(x=55, y=5, width=340, height=60)

        def entry_set(entry, text):
            """
            Set entry box text
            :param entry: entry box
            :param text: text to set
            :return: None
            """
            if text!='':
                entry['state'] = 'normal'
                entry.delete(0, 'end')
                entry.insert(END, text)
                entry['state'] = 'readonly'

        def file_line(title, x, y, msg):
            """
            Create file entry and buttons widget
            :param title: file title
            :param x: x pos
            :param y: y pos
            :param msg: msg on hover
            :return:
            """
            item_label = Label(self, text=title + ": ", relief="flat", fg="gray40", anchor=W)
            item_label.place(x=x, y=y, height=20, width=60)
            item_file = StringVar()
            item_entry = Entry(self, textvariable=item_file, state="readonly")
            item_entry.place(x=x + 60, y=y, height=20, width=300)
            item_button = Button(self, text="\uD83D\uDCC2", relief="groove",
                                 command=lambda: (entry_set(item_entry, askopenfilename()), item_entry.configure(fg="black")))
            item_button.place(x=x + 360, y=y, height=20, width=20)
            info_hover = InfoHover(self, msg)
            info_hover.place(x=x + 360 + 20, y=y, height=20, width=20)
            return item_entry

        titles = [("item file", "file containing item data"), ("slot file", "file containing slot data"), ("stock file", "file containing info on current stock"), ("hits file", "file for hits history")]
        x = 20
        y = 60
        self.entries = []
        for name in titles:
            self.entries.append(file_line(name[0], x, y, name[1]))
            y += 30

        def create_new_warehouse():
            """
            Use files from entries to create new warehouse and push it into the system
            :return: None
            """
            for entry in self.entries:
                if entry.get() == "" or entry.get() == "No File Selected":
                    entry_set(entry, "No File Selected")
                    entry.configure(fg="red")
                    return

            try:
                self.master.change_warehouse(self.entries[0].get(), self.entries[1].get(), self.entries[2].get(), self.entries[3].get())
                shutil.copy(self.entries[0].get(), "resources/source/item.csv")
                shutil.copy(self.entries[1].get(), "resources/source/slot.csv")
                shutil.copy(self.entries[2].get(), "resources/source/itmslot.csv")
                shutil.copy(self.entries[3].get(), "resources/source/hits.csv")
                self.destroy()
            except Exception as e:
                ErrorWindow(self, e, 'I001')

        create_button = Button(self, text="Create", relief="groove", pady=13, bg="SteelBlue1",
                               command=create_new_warehouse)
        create_button.place(x=450-105, y=220-40, width=55, height=20)

        self.configure(width=450, height=220)
        center_to_win(self, master)
        self.grab_set()