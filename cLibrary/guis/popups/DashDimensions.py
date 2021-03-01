from cLibrary.guis.popups.StandardPopup import *
from cLibrary.guis.popups.ErrorWindow import ErrorWindow


class DashDimensions(StandardPopUp):

    def __init__(self, master, controller, *args, **kwargs):
        """
        Initialise from super
        :param master: master window
        :param controller: program controller
        """
        super(DashDimensions, self).__init__(master, controller, width=230, height=85, *args, **kwargs)

    def load_display(self):
        """
        Load display
        :return: None
        """
        rows_label = Label(self, text="Rows:", relief="flat", fg="gray40", anchor=W)
        rows_label.place(width=100, height=20, x=(self.winfo_reqwidth()//2)-105, y=(self.winfo_reqheight()//2)-35)
        self.rows_var = StringVar()
        rows_entry = Entry(self, relief="groove", textvariable=self.rows_var)
        rows_entry.place(width=100, height=20, x=(self.winfo_reqwidth() // 2) + 5, y=(self.winfo_reqheight() // 2) - 35)

        cols_label = Label(self, text="Columns:", relief="flat", fg="gray40", anchor=W)
        cols_label.place(width=100, height=20, x=(self.winfo_reqwidth()//2)-105, y=(self.winfo_reqheight()//2)-10)
        self.cols_var = StringVar()
        cols_entry = Entry(self, relief="groove", textvariable=self.cols_var)
        cols_entry.place(width=100, height=20, x=(self.winfo_reqwidth()//2)+5, y=(self.winfo_reqheight()//2)-10)

        with open("resources/data/config.txt", "r") as file:
            line = file.readline().strip("\n").split(",")
            self.rows_var.set(line[0])
            self.cols_var.set(line[1])

        ok_button = Button(self, text="OK", relief="groove", pady=13, bg="SteelBlue1",
                           command=lambda :(self.ok(),))
        ok_button.place(x=self.winfo_reqwidth()-65, y=self.winfo_reqheight()-25, width=55, height=20)

        cancel_button = Button(self, text="Cancel", relief="groove", pady=30, bg="grey", command=lambda :(self.on_close(),))
        cancel_button.place(x=self.winfo_reqwidth()-125, y=self.winfo_reqheight()-25, width=55, height=20)

    def ok(self):
        """
        Save dash dimensions
        :return: None
        """
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            self.on_close()
            self.controller.wigs_w = cols
            self.controller.wigs_h = rows
            self.master.update_dash()
        except Exception as e:
            ErrorWindow(self,e,'U001',)