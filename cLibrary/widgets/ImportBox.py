from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as fdlog


class ImportBox(Frame):

    def __init__(self, master, title, *args, **kw):
        super(ImportBox, self).__init__(master, *args, **kw)
        self.item_label = Label(self, text=title + ": ", relief="groove", fg="gray40", anchor=W, padx=15)
        self.item_label.pack(side=TOP, fill=BOTH, expand=True)
        self.item_file = StringVar()
        self.item_entry = Entry(self, textvariable=self.item_file, state="readonly")
        self.item_entry.pack(side=LEFT, fill=BOTH, expand=True)
        self.item_button = Button(self, text="\uD83D\uDCC2", relief="groove",
                                     command=lambda: (
                                         self.entry_set(self.item_entry, fdlog.askopenfilename()),
                                         self.item_entry.configure(fg="black")
                                         )
                                     )
        self.item_button.pack(side=LEFT, fill=BOTH, expand=True)

    def get(self):
        return self.item_entry.get()

    @staticmethod
    def entry_set(entry: Entry, text: str):
        """
        Set entry box text
        :param entry: entry box
        :param text: text to set
        :return: None
        """
        if text != '':
            entry['state'] = 'normal'
            entry.delete(0, 'end')
            entry.insert(END, text)
            entry['state'] = 'readonly'
