from cLibrary.guis.popups.StandardPopup import *
from cLibrary.widgets.Output import Output


class ErrorWindow(StandardPopUp):

    def __init__(self, master, error_msg, error_code='ZZZZ', cust_sugg=None, *args, **kwargs):
        super(ErrorWindow, self).__init__(master, width=400, height=170, title='ERROR : '+error_code.upper(),
                                          icon="resources/img/error.ico", *args, **kwargs)

        img = PIL.Image.open("resources/img/error.ico").resize((40, 40), PIL.Image.ANTIALIAS)
        self.n_img = PIL.ImageTk.PhotoImage(img)
        osa = Label(self, image=self.n_img, anchor="n", bd=1)
        osa.place(x=20, y=20)

        self.suggest_action(error_code, cust_sugg)
        self.expanded = False

        code = Label(self, text="Error Code : " + error_code, font="bold 15")
        code.place(x=70, y=30)

        self.smb = Button(self, text="show more", command=self.show_more)
        self.smb.place(x=30, y=130)

        self.output = Output(self, relief="groove", wrap=WORD, )
        self.output.r_insert(error_msg)

        ok = Button(self, text="OK", bg="white", relief="groove", command=self.on_close)
        ok.place(x=400 - 110, y=130, width=90, height=30)

    def show_more(self):
        expand_val = 70
        if not self.expanded:
            self.geometry('{}x{}'.format(self.winfo_width(), self.winfo_height()+expand_val))
            self.output.place(x=10, y=175, width=380, height=50)
            self.smb['text'] = "show less"
            self.update()
        else:
            self.geometry('{}x{}'.format(self.winfo_width(), self.winfo_height()-expand_val))
            self.output.place_forget()
            self.smb['text'] = "show more"
            self.update()
        self.expanded = not self.expanded

    def suggest_action(self, code, cust_sugg):
        def suggestion(msg):
            output = Output(self, relief="flat", wrap=WORD, bg=self['bg'])
            output.place(x=10, y=70, width=380, height=50)
            output.r_insert(msg)

        code_id = code[0]

        if cust_sugg is not None:
            suggestion(cust_sugg)
        elif code_id == 'U':
            suggestion('User Input Error Detected: Make sure to check you have entered the correct values into fields')
        elif code_id == "I":
            suggestion('Import Error Detected: It seems something failed to import properly, check what you\'re '
                       'trying to import is correct')
        else:
            suggestion('Unknown Error: Please restart the program. If the problem persists see Admin')
