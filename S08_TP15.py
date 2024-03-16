import tkinter as tk
from S06_TP11 import PlanetAlpha
from S07_TP14_01 import *


class PlanetTk(PlanetAlpha, tk.Canvas):

    def __init__(self, root, name, lattitude_cells_count, longitude_cells_count, authorized_classes, background_color='white', foreground_color='dark blue', gridlines_color='maroon',  cell_size=40, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw):

        PlanetAlpha.__init__(self, name, lattitude_cells_count,
                             longitude_cells_count, Ground())

        l = lattitude_cells_count
        c = longitude_cells_count
        kw['width'] = c*cell_size + (c-1) * gutter_size + margin_size * 2
        kw['height'] = l*cell_size + (l-1) * gutter_size + margin_size * 2
        tk.Canvas.__init__(self, width=kw['width'], height=kw['height'])

        self.__cell_size = cell_size
        self.__gutter_size = gutter_size
        self.__margin_size = margin_size
        self.__root = root
        self.__show_content = show_content
        self.__show_grid_lines = show_grid_lines
        self.__authorized_classes = {Ground} | authorized_classes
        self.__background_color = background_color
        self.__foreground_color = foreground_color
        self.__gridlines_color = gridlines_color

    def get_root(self):
        return self.__root

    def get_authorized_classes(self):
        return self.__authorized_classes

    def get_background_color(self):
        return self.__background_color

    def get_foreground_color(self):
        return self.__foreground_color

    def born(self, cell_number, element):
        line, col = self.get_coordinates_from_cell_number(cell_number)
        grid = self.get_grid()
        for type in self.__authorized_classes:
            if (isinstance(element, type) or type().__repr__() == element):
                if (grid[line][col] == self.get_ground()):
                    self.set_cell(cell_number, element)

    def die(self, cell_number):
        cell = self.get_cell(cell_number)
        if (cell != self.get_ground()):
            self.set_cell(cell_number, self.get_ground())

    def born_randomly(self, element):
        random_free_place = self.get_random_free_place()
        self.born(random_free_place, element)

    def populate(self, class_names_count):
        for element_type, element_count in class_names_count.items():
            instance = element_type()
            for _ in range(element_count):
                self.born_randomly(instance)

    def move_element(self, cell_number, new_cell_number):

        element = self.get_cell(cell_number)
        element_in_new_cell_number = self.get_cell(new_cell_number)

        # Move the element only if the new cell is free
        if (element_in_new_cell_number == self.get_ground() and element != self.get_ground()):
            self.die(cell_number)
            self.born(new_cell_number, element)

    def get_classes_cell_numbers(self, class_name):
        cell_numbers = {class_name: []}
        for cell_number in self.get_same_value_cell_numbers(class_name):
            cell_numbers['class_name'].append(cell_number)
        return cell_numbers

    def draw(self):
        for i in range(self.get_lines_count()):
            y0 = self.__margin_size + i * \
                (self.__cell_size + self.__gutter_size)
            y1 = self.__margin_size + self.__cell_size + \
                i * (self.__cell_size + self.__gutter_size)

            for j in range(self.get_columns_count()):
                x0 = self.__margin_size + j * \
                    (self.__cell_size + self.__gutter_size)
                x1 = self.__margin_size + self.__cell_size + \
                    j * (self.__cell_size + self.__gutter_size)

                x_center = (x0 + x1) / 2
                y_center = (y0 + y1) / 2

                cell_number = self.get_cell_number_from_coordinates(i, j)
                cell_content = self.get_cell(cell_number)

                if (self.__show_grid_lines):
                    self.create_rectangle(x0, y0, x1, y1, tags=(f'c_{cell_number}'))

                self.create_text(x_center, y_center, text=cell_content, tags=(f't_{cell_number}'))
                self.lift(f't_{cell_number}')
                self.itemconfigure(f't_{cell_number}', fill="dark blue")

                if (cell_content != self.get_ground()):
                    self.itemconfigure(f'c_{cell_number}', fill="yellow")

        self.pack()

    def __repr__(self):
        return PlanetAlpha.__repr__(self)

    def __str__(self):
        return PlanetAlpha.__str__(self)


# TODO  use tags to change text/color
# self.itemcget(f't_{cell_number}', "text")
if __name__ == '__main__':
    root = tk.Tk()
    LINES_COUNT = 20
    COLUMNS_COUNT = 30
    CELL_SIZE = 40
    GUTTER_SIZE = 0
    MARGIN_SIZE = 10
    elements_types = {Lion, Cow, Water, Herb, Dragon}

    app = PlanetTk(root, "Terre", LINES_COUNT, COLUMNS_COUNT, elements_types, 'white',
                   'dark blue', 'maroon', CELL_SIZE, GUTTER_SIZE, MARGIN_SIZE, True, True, width=80, height=50)

    INHABITANTS_TEST = {Lion: 70, Cow: 30}
    RESOURCES_TEST = {Water: 100, Herb: 1000}

    app.populate(INHABITANTS_TEST)
    app.populate(RESOURCES_TEST)

    nw_neighborhood = app.get_cell_neighborhood_numbers(0,
                                                        PlanetAlpha.WIND_ROSE)

    app.die(0)
    app.die(0)
    app.die(0)

    for cell in nw_neighborhood:
        app.die(cell)

    app.move_element(2, 0)
    app.move_element(3, 1)

    app.draw()
    print(app)
    app.mainloop()
