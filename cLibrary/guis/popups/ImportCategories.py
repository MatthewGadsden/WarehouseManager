from cLibrary.guis.popups.StandardPopup import *
from cLibrary.guis.popups.Notification import Notification
from cLibrary.widgets.InfoHover import InfoHover


class ImportCategories(StandardPopUp):

    def load_display(self):
        l1 = Label(self, text="Category File :")
        l1.place(x=40, y=30)

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

        item_file = StringVar()
        item_entry = Entry(self, textvariable=item_file, state='readonly')
        item_entry.place(x=40, y=50, width=390, height=20)

        def ok_press():
            if item_entry.get() == "" or item_entry.get() == "No File Selected":
                entry_set(item_entry, "No File Selected")
                item_entry.configure(fg="red")
                return

            else:
                self.import_item_cat(item_entry.get())

        item_button = Button(self, text="\uD83D\uDCC2", relief="groove", command=lambda: (entry_set(item_entry, askopenfilename()), item_entry.configure(fg="black")))
        item_button.place(x=430, y=50, width=20, height=20)

        info_hover = InfoHover(self, "Select item category data")
        info_hover.place(x=450, y=50, width=20, height=20)

        l2 = Label(self, text="File Format : ")
        l2.place(x=40, y=80)

        excel_eg = Frame(self,)
        excel_eg.place(x=115, y=80)

        excel_eg.grid_columnconfigure(0, minsize=50)
        excel_eg.grid_columnconfigure(1, minsize=50)

        col_1_title = Label(excel_eg, text="item id", bg="white", relief="groove")
        col_1_title.grid(column=0, row=0, sticky="nsew")

        col_2_title = Label(excel_eg, text="category", bg="white", relief="groove")
        col_2_title.grid(column=1, row=0, sticky="nsew")

        col_1_row_1 = Label(excel_eg, text="527540", bg="white", relief="groove")
        col_1_row_1.grid(column=0, row=1, sticky="nsew")

        col_1_row_2 = Label(excel_eg, text="...", bg="white", relief="groove")
        col_1_row_2.grid(column=0, row=2, sticky="nsew")

        col_2_row_1 = Label(excel_eg, text="ashdene", bg="white", relief="groove")
        col_2_row_1.grid(column=1, row=1, sticky="nsew")

        col_2_row_2 = Label(excel_eg, text="...", bg="white", relief="groove")
        col_2_row_2.grid(column=1, row=2, sticky="nsew")

        ok_button = Button(self, text="upload", bg="lime", fg="grey20", relief="groove", command=ok_press)
        ok_button.place(x=400, y=70, height=20, width="50")

    def import_item_cat(self, file):
        if not isinstance(self.controller, Controller):
            raise TypeError("Controller must be a controller")
        with open(file, "r", encoding='utf-8-sig') as cat_file:
            data = []
            for line in cat_file:
                data.append(line.strip("\n").split(","))

        added_count = 0
        total_count = 0
        error_count = 0

        cats = {}
        error_items = []

        for x in data:
            item_string = x[0].lstrip()
            item = self.controller.warehouse.item_list[item_string]
            total_count += 1
            if item is not None:
                added_count += 1
                self.controller.categories.add_item(item, x[1].lower())
                cats[x[1].lower()] = (1 if cats.get(x[1].lower()) is None else cats.get(x[1].lower())+1)
            else:
                error_items.append(item_string)
                error_count += 1
        msg = "Successfully assigned items to categories:\n"

        for key in cats:
            msg += "\t{} items successfully assigned to {}\n".format(cats[key], key)

        for error in error_items:
            msg += 'error with item: ' + error + '\n'

        msg += '\n{} out of {} items added\n'.format(added_count, total_count)
        msg += 'Errors = {}'.format(error_count)
        self.wait_window(Notification(self, msg, width=500, height=180))
        self.on_close()
