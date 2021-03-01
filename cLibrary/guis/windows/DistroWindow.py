from cLibrary.guis.windows.WidgetWindow import *
from cLibrary.widgets.ScrolledFrame import ScrolledFrame
from typing import List, Tuple, Set, Optional
from cLibrary.structure.item.Item import Item
from cLibrary.widgets.ImportBox import ImportBox
from cLibrary.widgets.WarehouseFrame import WarehouseFrame
from cLibrary.structure.warehouse.Area import Area
from cLibrary.guis.popups.SelectArea import SelectArea
from cLibrary.methods.distro import distro_setup
from cLibrary.methods.general import open_excel
from cLibrary.widgets.WinOutput import WinOutput
import tkinter.ttk as ttk


class Distro(WidgetWindow):

    def __init__(self, master, controller):
        self.upload_box = None  # type: Optional[UploadDistro]
        self.area_select = None     # type: Optional[AreaSelect]
        self.run_frame = None
        self.excel_entry = None
        self.excel_file = None  # type: Optional[str]
        super(Distro, self).__init__(master, controller)
        self.output = WinOutput(self, width=800, height=self.controller.wig_height - 80,
                                x=self.controller.wig_width - 800 - 20, y=70,
                                wrap=WORD, bg="snow", font="none 10", relief="groove")

    def load_title(self, text="Distro Program", bg="burlywood1", relief="groove"):
        super(Distro, self).load_title(text=text, bg=bg, relief=relief)

    def load_display(self):
        self.upload_box = UploadDistro(self)  # type: UploadDistro
        self.area_select = AreaSelect(self)  # type: AreaSelect
        self.run_frame = WarehouseFrame(self, )
        self.excel_entry = Entry(self.run_frame, relief="groove")

        self.upload_box.place(x=50, y=100, width=300, height=200)
        self.area_select.place(x=50, y=320, width=300, height=60)

        output_label = Label(self.run_frame, text="Output File Name: ", relief="groove", bg="light grey")
        run_button = Button(self.run_frame, text="Run Distro Setup", relief="groove", bg="pink", command=self.run_distro)
        open_file_button = Button(self.run_frame, text="Open File", relief="groove", bg="lime", command=self.open_file)

        self.run_frame.place(x=50, y=400, width=300, height=60)
        self.excel_entry.grid(row=0, column=1, columnspan=2, sticky=NSEW)
        self.run_frame.grid_columnconfigure(2, weight=1)
        self.run_frame.rowconfigure(0, weight=1)

        outfile_button = Button(self.run_frame, text="\uD83D\uDCC2", font="bold 14", relief="groove",
                                command=lambda: (
                                    self.excel_entry.delete(0, 'end'),
                                    self.excel_entry.insert(0, asksaveasfilename(filetypes=(('XML', '*.xlsx'),),
                                                                     defaultextension=".xlsx")),
                                    self.excel_entry.configure(fg="black")))
        outfile_button.grid(row=0, column=3, sticky=NSEW)

        output_label.grid(row=0, column=0, sticky=NSEW)
        run_button.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        open_file_button.grid(row=1, column=3, sticky=NSEW)

    def run_distro(self):
        try:
            if self.excel_entry.get() == "" or self.excel_entry.get() == "Must Select a File!":
                raise ValueError("")
            self.excel_file = distro_setup(self.upload_box.get(), self.area_select.get(), self.get_controller().warehouse, self.excel_entry.get())
        except ValueError as e:
            self.excel_entry.delete(0, "end")
            self.excel_entry.insert(0, "Must Select a File!")
            self.excel_entry.configure(fg="red")

    def open_file(self):
        open_excel(self.excel_file, self.output)


class UploadDistro(WarehouseFrame):

    def __init__(self, master, *args, **kw):
        super(UploadDistro, self).__init__(master, *args, **kw)
        self.data = None
        self.distro_data = DistroData(self)     # type: DistroData
        self.title = Label(self, text="Upload Distro Data", relief='groove', bg='deep sky blue', )
        self.imp_box = ImportBox(self, 'Distro File')
        self.info = Label(self, text="Format: [Item Code, Quantity]", relief='groove')
        self.upload_button = Button(self, text="Upload", relief='groove', bg='lime',
                                    command=lambda: self.imp_distro_file())

        self.title.grid(row=0, column=0, columnspan=8, sticky=NSEW)
        self.imp_box.grid(row=1, column=0, columnspan=8, sticky=NSEW)
        self.info.grid(row=2, column=0, columnspan=7, sticky=NSEW)
        self.upload_button.grid(row=2, column=7, columnspan=1, sticky=NSEW)
        self.distro_data.grid(row=3, column=0, columnspan=8, sticky=NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def imp_distro_file(self):
        data = []   # type: List[Tuple[Item, int]]
        warehouse = self.get_controller().warehouse
        with open(self.imp_box.get(), 'r') as f:
            for line in f:
                x = line.strip('\n').replace(' ', '').split(',')
                itm = warehouse.item_list[x[0]] # type: Item
                i = int(x[1])   # type: int
                data.append((itm, i))
        self.data = data
        self.distro_data.change_data(data)

    def get(self) -> List[Tuple[Item, int]]:
        return self.data


class DistroData(WarehouseFrame):
    """
    Display uploaded distro data in a scrolled frame
    """
    def __init__(self, master, *args, **kw):
        super(DistroData, self).__init__(master)
        self.data = None
        self.tview = ttk.Treeview(self)  # type: Treeview
        self.tview.pack(fill=BOTH, expand=True)
        self.tview['show'] = 'headings'

    def change_data(self, data: List[Tuple[Item, int]]):
        """
        update the distro data
        :param data: distro data to update to
        :return: None
        """
        self.tview.destroy()
        self.tview = ttk.Treeview(self, style="Custom.Treeview")
        self.tview.pack(fill=BOTH, expand=True)
        self.tview['columns'] = ('itm', 'qty')
        self.tview.heading('itm', text='Item Code')
        self.tview.heading('qty', text="Quantity")
        self.tview['show'] = 'headings'
        self.tview.column('itm', width=90)
        self.tview.column('qty', stretch=True)
        for item in data:
            self.tview.insert('', 'end', values=(item[0].item_id, str(item[1])))


class AreaSelect(WarehouseFrame):

    def __init__(self, master, *args, **kw):
        super(AreaSelect, self).__init__(master, *args, **kw)
        controller = self.get_controller()
        self.grid_columnconfigure(0, weight=1)
        self.title = Label(self, text="Select / Create Area", relief="groove")

        self.areas = controller.areas
        self.area_dict = {}
        for area in self.areas:
            self.area_dict[area.area_name] = area
        area_combo_options = [key.area_name for key in self.areas]

        self.area_combo = Combobox(self, values=area_combo_options, font="bold 10", state="readonly")
        self.area_combo.set(area_combo_options[0])

        self.create_area_button = Button(self, text="New Area", relief="groove", bg="orange",
                                         command=self.new_area, state="disabled")

        self.title.pack(fill=BOTH, expand=True)
        self.area_combo.pack(side=LEFT, fill=BOTH, expand=True)
        self.create_area_button.pack(side=LEFT, fill=BOTH, expand=True)

    def get(self) -> Area:
        """
        Get area selected in combo box
        :return: Area relating to selection
        """
        return self.area_dict[self.area_combo.get()]

    def new_area(self):
        """
        Create new area for distro's
        :return: None
        """
        pass
