from cLibrary.guis.popups.StandardPopup import *
from cLibrary.widgets.Output import Output


class Notification(StandardPopUp):

    def __init__(self, master, msg, *args, **kwargs):
        self.msg = msg
        super(Notification, self).__init__(master, *args, **kwargs)

    def load_display(self):
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()

        output = Output(self,)
        output.place(x=10, y=10, width=w-20, height=h-50)

        ok_button = Button(self, text="okay", bg="lime", fg="grey35", relief="groove", command=lambda: self.on_close())
        ok_button.place(x=w-70, y=h-30, width=60, height=20)

        output.r_insert(self.msg)