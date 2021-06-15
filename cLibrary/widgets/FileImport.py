import tkinter as tk
import tkinter.filedialog as fdlog


class FileImport(tk.Frame):

    def __init__(self, master, **kw):
        super(FileImport, self).__init__(master)
        title = kw.get('title', 'Output')
        filetypes = kw.get('filetypes', (("all files","*.*"), ))
        t_fg = kw.get('t_fg', 'black')
        t_font = kw.get('t_font', 'bold 10')
        b_fg = kw.get('b_bg', t_fg)
        b_font = kw.get('b_font', t_font)
        self.item_label = tk.Label(self, text=title + ": ", relief="groove", fg=t_fg, font=t_font, anchor=tk.W, padx=15)
        self.item_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.item_file = tk.StringVar()
        self.item_entry = tk.Entry(self, textvariable=self.item_file, state="readonly")
        self.item_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.item_button = tk.Button(self, text="\uD83D\uDCC2", font=b_font, fg=b_fg, relief="groove",
                                  command=lambda: (
                                      self.entry_set(self.item_entry, fdlog.askopenfilename(filetypes=filetypes)),
                                      self.item_entry.configure(fg="black")
                                  )
                            )
        self.item_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get(self):
        return self.item_entry.get()

    @staticmethod
    def entry_set(entry: tk.Entry, text: str):
        """
        Set entry box text
        :param entry: entry box
        :param text: text to set
        :return: None
        """
        if text != '':
            entry['state'] = 'normal'
            entry.delete(0, 'end')
            entry.insert(tk.END, text)
            entry['state'] = 'readonly'