from cLibrary.guis.windows.WidgetWindow import *
from tkinter.filedialog import *
from cLibrary.methods.relay import relay
from cLibrary.methods.general import open_excel, xlsx_ft
from cLibrary.guis.popups.ErrorWindow import ErrorWindow
from cLibrary.widgets.WinOutput import WinOutput


class Relay(WidgetWindow):

    def __init__(self, master, controller):
        super(Relay, self).__init__(master, controller)
        self.output = WinOutput(self, width=870, height=self.controller.wig_height - 80,
                                x=self.controller.wig_width - 870 - 20, y=70,
                                wrap=WORD, bg="snow", font="none 10", relief="groove")

        self.excel = None

    def load_title(self, text="Relay Warehouse", bg="burlywood1", relief="groove"):
        super(Relay, self).load_title(text=text, bg=bg, relief=relief)

    def relay(self, area_dict, cat_dict, area_comb, cat_comb, excess_comb, outfile):
        """
        Relay selected Category into the specified Areas within the Warehouse
        :param area_dict: dictionary for CustomArea's
        :param cat_dict: dictionary for Categories
        :param area_comb: Area combobox
        :param cat_comb: Category combobox
        :param excess_comb: Excess Area combobox
        :param outfile: file location to output relay file to
        :return: None
        """
        try:
            if outfile == '':
                raise ValueError("1")
            elif area_comb.get() == excess_comb.get():
                raise ValueError("2")
            else:
                outfile = xlsx_ft(outfile)
                self.output.r_insert("Creating Allocations...")
                self.excel = relay(cat_dict[cat_comb.get()], area_dict[area_comb.get()],
                                   area_dict[excess_comb.get()], self.controller, outfile)
                self.output.r_insert("Allocations created and sent to {}".format(outfile))
        except ValueError as e:
            auto_resp = "User error, no additional info needed"
            e = str(e)
            if e == "1":
                ErrorWindow(self, auto_resp, "U003",
                            "Please enter an output file name to send the data to.")
            elif e == "2":
                ErrorWindow(self, auto_resp, 'U002',
                            "Area option and excess area option cannot have the same area selected.")
            else:
                ErrorWindow(self, e, "U004",
                            "Unknown user error detected, please contact admin if issue cannot be resolved")

    def open_excel(self):
        open_excel(self.excel, self.output)

    @staticmethod
    def entry_set(entry, text):
        """
        Set entry box text
        :param entry: entry box
        :param text: text to set
        :return: None
        """
        if text != '':
            entry.delete(0, 'end')
            entry.insert(END, text)

    def load_display(self):
        w = 250

        cat_title = Label(self, text="Category", font="bold 15")
        cat_title.place(x=30, y=70, width=w, height=40)

        cats = self.controller.categories
        cat_dict = {}
        for cat in cats:
            cat_dict[cat] = cats[cat]
        cat_combo_options = [key for key in cats]

        cat_combo = Combobox(self, values=cat_combo_options, font="bold 10", state="readonly")
        cat_combo.place(x=30, y=110, width=w, height=30)
        cat_combo.set(cat_combo_options[0])

        area_title = Label(self, text="Area", font="bold 15")
        area_title.place(x=30, y=150, width=w, height=40)

        areas = self.controller.areas
        area_dict = {}
        for area in areas:
            area_dict[area.area_name] = area
        area_combo_options = [key.area_name for key in areas]

        area_combo = Combobox(self, values=area_combo_options, font="bold 10", state="readonly")
        area_combo.place(x=30, y=190, width=w, height=30)
        area_combo.set(area_combo_options[0])

        area_title2 = Label(self, text="Excess Area", font="bold 15")
        area_title2.place(x=30, y=230, width=w, height=40)

        area_combo_options2 = [key.area_name for key in areas]

        area_combo2 = Combobox(self, values=area_combo_options2, font="bold 10", state="readonly")
        area_combo2.place(x=30, y=270, width=w, height=30)
        area_combo2.set(area_combo_options2[0])

        outfile_label = Label(self, text="Output File Name", font="bold 15")
        outfile_label.place(x=30, y=310, width=w-40, height=40)

        outfile_entry = Entry(self, )
        outfile_entry.place(x=30, y=350, width=w, height=30)

        outfile_button = Button(self, text="\uD83D\uDCC2", font="bold 14", relief="groove",
                                command=lambda: (
                                    self.entry_set(outfile_entry,
                                    asksaveasfilename(filetypes=(('XML', '*.xlsx'),), defaultextension=".xlsx")),
                                    outfile_entry.configure(fg="black")))

        outfile_button.place(x=30+w-40, y=310, width=40, height=40)

        relay_button = Button(self, text="Relay",
                              bg="limegreen",
                              font="bold 12",
                              relief="groove",
                              command=lambda: self.relay(area_dict, cat_dict, area_combo, cat_combo, area_combo2, outfile_entry.get()))
        relay_button.place(x=30, y=390, width=w-60, height=30)

        open_button = Button(self, text="Open", bg="lawn green", relief="groove", command=lambda: self.open_excel())
        open_button.place(x=30+w-60, y=390, width=60, height=30)
