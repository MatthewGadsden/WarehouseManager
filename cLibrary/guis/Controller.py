# from cLibrary.guis.Windows import
from tkinter import *
from tkinter.font import *
from cLibrary.methods.general import *
from cLibrary.structure.datatypes.Category import CatList, Category
from cLibrary.structure.warehouse.CustomArea import CustomArea
import tkinter.ttk as ttk


class Controller:

    def __init__(self, master, warehouse):
        """
        initialize the controller
        :param master: master window
        :param warehouse: warehouse framework the system is running on
        """
        self.warehouse = warehouse
        self.areas = {}  # type: dict
        self.categories = CatList()
        self.master = master

        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title_font2 = Font(family='Calibri', size=11)
        self.title_fontmainTMenu = Font(family='Helvetica', size=15)
        self.title_fontDevices = Font(family='Didot', size=13)
        self.title_fontT = Font(family='Cambria', size=16)
        self.wig_width = master.winfo_reqwidth()-10
        self.wig_height = master.winfo_reqheight()-50
        self.bay_range = 0
        self.gap = 0
        self.hp = 0

        self.load_con_settings()
        self.load_categories()
        self.load_areas()

        self._create_styles()

        with open("resources/data/config.txt", "r") as file:
            line = file.readline().strip("\n").split(",")
            self.wigs_w = int(line[0])
            self.wigs_h = int(line[1])

            co_ords = file.readline().strip("\n").split(",")
            x = co_ords[0]
            y = co_ords[1]
            wid = self.master.winfo_reqwidth()
            hei = self.master.winfo_reqheight()

            screen_w = self.master.winfo_screenwidth()
            screen_h = self.master.winfo_screenheight()
            if 0 > int(x) or int(x)+10 > screen_w or 0 > int(y) or int(y) > screen_h:
                center_to_screen(self.master, adj=20)
            else:
                self.master.geometry("%dx%d+%d+%d" % (wid, hei, int(x), int(y)))
        self.container = Frame(master, bg="coral1")
        self.container.place(x=5, y=25, height=self.wig_height, width=self.wig_width)
        self.frames = {}

    def on_close(self):
        self.save_categories()
        self.save_areas()

    def load_con_settings(self):
        """
        load con settings from settings file
        :return: None
        """
        with open("resources/data/con-set.txt") as file:  # opening con settings file
            x = file.readline().strip("\n").split(",")
            self.bay_range = int(x[0])
            self.gap = int(x[1])
            self.hp = int(x[2])

            reserves = self.warehouse.get_reserve_slots()
            for spot in reserves:
                spot.get_attrs(room=self.gap, hp=self.hp)

    def save_categories(self):
        """
        Save categories to data save (application data)
        :return: None
        """
        save_data = []
        for category in self.categories.values():
            temp_cat_data = [category.name]
            for item in category.values():
                temp_cat_data.append(item.item_id)
            save_data.append(temp_cat_data)

        with open('resources/data/categories.csv', 'w') as file:
            for row in save_data:
                first_value = True
                for value in row:
                    if first_value:
                        first_value = not first_value
                        file.write(value)
                    else:
                        file.write(',' + str(value))
                file.write('\n')

    def load_categories(self):
        """
        Load categories from data save (application data)
        :return: None
        """
        with open('resources/data/categories.csv', 'r', encoding='utf-8-sig') as file:
            data = []
            for line in file:
                data.append(line.strip('\n').split(','))

            for row in data:
                first_value = True
                current_cat = None
                for value in row:
                    if first_value:
                        first_value = not first_value
                        current_cat = value
                        self.categories.add_category(value)
                    else:
                        self.categories.add_item(self.warehouse.item_list[value], current_cat) if self.warehouse.item_list[value] is not None else "pass"

    def load_areas(self):
        """
        Load warehouse areas into system
        :return:
        """
        from cLibrary.structure.warehouse.CustomArea import CustomArea
        with open("resources/data/areas.wf", "r") as file:
            areas = {}
            for line in file:
                line = line.strip("\n").split(",")
                i = 1
                while i < len(line):
                    save_line = line[i]
                    spot = self.warehouse.find_area(line[i])
                    if spot is None:
                        raise ValueError("Save File Error:\n\nSpot ID {} was found in save file, contact help is further "
                                         "assistance is needed".format(save_line))
                    line[i] = spot
                    i += 1
                areas[line[0]] = (CustomArea(line[1:], line[0], self.warehouse))
        self.areas = areas

    def save_areas(self):
        """
        Save current warehouse areas in warehouse system (application data)
        :return: None
        """
        with open("resources/data/areas.wf", "w") as file:
            for area in self.areas:
                a = self.areas[area]
                file.write(a.area_name)
                for spot in a:
                    file.write("," + spot.spot_id)
                file.write("\n")

    @staticmethod
    def _create_styles():
        style = ttk.Style()
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview",
                        background="white", foreground="black", relief="sunken")
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])
        style.map("Custom.Treeview.Row",
                  relief=[('active', 'groove')])

    def get_area(self, area_name: str) -> CustomArea:
        return self.areas[area_name]

    def get_category(self, cat_name: str) -> Category:
        return self.categories['cat_name']
