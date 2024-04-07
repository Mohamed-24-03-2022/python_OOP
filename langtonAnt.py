from S07_TP14_01 import *
from S08_TP15 import PlanetTk
import tkinter as tk


class LangtonAnt(PlanetTk):

    # COLORS = {"empty": "white", "turmite": "black"}

    def __init__(self, root, name, lattitude_cells_count, longitude_cells_count, background_color='white', foreground_color='black', gridlines_color='maroon',  cell_size=5, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw):
        super().__init__(root, name, lattitude_cells_count, longitude_cells_count, {Turmite, EmptyCell}, EmptyCell(), background_color,
                         foreground_color, gridlines_color,  cell_size, gutter_size, margin_size, show_content, show_grid_lines, **kw)

        self.__init_position = (lattitude_cells_count // 2, longitude_cells_count // 2)  # Start in the middle
        self.__current_pos = self.__init_position
        self.__direction = 'up'
        self.__prev_grid = None
        self.__is_game = False

        self.init_position()
        self.create_buttons()
        self.draw()
        self.mainloop()

    def init_position(self):
        init_cell_number = self.get_cell_number_from_coordinates(self.__init_position[0], self.__init_position[1])
        self.set_cell(init_cell_number, Turmite())

    def start(self):
        self.__is_game = True
        self.update_canvas()

    def stop(self):
        self.__is_game = False

    def reset(self):
        self.stop()
        for i in range(self.get_cells_count()):
            if (self.get_cell(i) != EmptyCell()):
                self.set_cell(i, EmptyCell())
                self.itemconfigure(f't_{i}', text=EmptyCell())
                # self.itemconfigure(f'c_{i}', fill='white')
        self.set_direction('up')
        self.set_current_pos(self.__init_position)
        init_cell_number = self.get_cell_number_from_coordinates(self.__init_position[0], self.__init_position[1])
        self.set_cell(init_cell_number, Turmite())
        self.itemconfigure(f't_{init_cell_number}', text=Turmite())
        # self.itemconfigure(f'c_{init_cell_number}', fill=LangtonAnt.COLORS["turmite"])

    def get_current_pos(self):
        return self.__current_pos

    def set_current_pos(self, new_pos):
        self.__current_pos = new_pos

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def copy_grid(self):
        copied_grid = [[cell for cell in row] for row in self.get_grid()]
        return copied_grid

    def set_prev_grid(self, grid):
        self.__prev_grid = [[cell for cell in row] for row in grid]

    def get_prev_grid(self):
        return self.__prev_grid

    def create_buttons(self):
        # Bouton de fermeture
        self.__b_quit = tk.Button(self.get_root(), text='Close', command=self.quit)
        self.__b_quit.pack(side=tk.BOTTOM)
        # Bouton de démarrage
        btn_frame = tk.Frame(self.get_root())
        btn_frame.pack(side=tk.BOTTOM)
        start_button = tk.Button(btn_frame, text="Démarrer", command=self.start)
        start_button.pack(side=tk.LEFT)
        # Bouton d'arrêt
        stop_button = tk.Button(btn_frame, text="Arrêter", command=self.stop)
        stop_button.pack(side=tk.LEFT)
        # # Bouton de réinitialisation
        reset_button = tk.Button(btn_frame, text="Réinitialiser", command=self.reset)
        reset_button.pack(side=tk.LEFT)

    def turn_right(self):
        if self.get_direction() == 'up':
            self.set_direction('right')
        elif self.get_direction() == 'right':
            self.set_direction('down')
        elif self.get_direction() == 'down':
            self.set_direction('left')
        elif self.get_direction() == 'left':
            self.set_direction('up')

    def turn_left(self):
        if self.get_direction() == 'up':
            self.set_direction('left')
        elif self.get_direction() == 'left':
            self.set_direction('down')
        elif self.get_direction() == 'down':
            self.set_direction('right')
        elif self.get_direction() == 'right':
            self.set_direction('up')

    def move_forward(self):
        x, y = self.get_current_pos()
        if self.get_direction() == 'up':
            self.set_current_pos((x-1, y))
        elif self.get_direction() == 'down':
            self.set_current_pos((x+1, y))
        elif self.get_direction() == 'left':
            self.set_current_pos((x, y-1))
        elif self.get_direction() == 'right':
            self.set_current_pos((x, y+1))

        self.set_current_pos((self.get_current_pos()[0] % self.get_columns_count(),
                             self.get_current_pos()[1] % self.get_lines_count()))

    def step(self):
        # when on a colored cell => turn 90deg left & move forward into a new cell & remove old cell's color
        # when on a white cell => turn 90deg right & move forward into a new cell & color old cell
        self.set_prev_grid(self.copy_grid())
        x, y = self.get_current_pos()
        current_cell_number = self.get_cell_number_from_coordinates(x, y)

        if (self.get_cell(current_cell_number) == Turmite()):
            self.turn_left()
            self.move_forward()
            self.set_cell(current_cell_number, EmptyCell())
        elif (self.get_cell(current_cell_number) == EmptyCell()):
            self.turn_right()
            self.move_forward()
            self.set_cell(current_cell_number, Turmite())

    def update_canvas(self):

        if (self.__is_game):
            self.step()
            for cell_number in range(self.get_cells_count()):
                i, j = self.get_coordinates_from_cell_number(cell_number)
                if (self.get_cell(cell_number) != self.get_prev_grid()[i][j]):
                    cell_type = self.get_cell(cell_number)
                    # color = LangtonAnt.COLORS["turmite"] if cell_type == Turmite() else LangtonAnt.COLORS["empty"]
                    self.itemconfigure(f't_{cell_number}', text=cell_type)
                    # self.itemconfigure(f'c_{cell_number}', fill=color)

        self.after(100, self.update_canvas)


if __name__ == '__main__':
    root = tk.Tk()
    LINES_COUNT = 80
    COLUMNS_COUNT = 80
    cell_size = 8
    gutter_size = 0
    margin_size = 10
    show_content = True
    show_grid_lines = True
    background_color = 'white'
    foreground_color = 'black'
    gridlines_color = 'black'

    app = LangtonAnt(root, "Turmite", LINES_COUNT, COLUMNS_COUNT, background_color, foreground_color, gridlines_color,
                     cell_size, gutter_size, margin_size, show_content, show_grid_lines, width=80, height=50)
