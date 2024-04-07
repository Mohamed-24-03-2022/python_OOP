from S07_TP14_01 import *
from S08_TP15 import PlanetTk
import tkinter as tk
import math


class SnakeGame(PlanetTk):

    # COLORS = {"empty": "white", "snake": "green", "apple": "red"}

    def __init__(self, root, name, lattitude_cells_count, longitude_cells_count, background_color='white', foreground_color='black', gridlines_color='maroon',  cell_size=5, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw):
        super().__init__(root, name, lattitude_cells_count, longitude_cells_count, {Snake, Apple, EmptyCell}, EmptyCell(), background_color,
                         foreground_color, gridlines_color,  cell_size, gutter_size, margin_size, show_content, show_grid_lines, **kw)

        self.__init_position = (lattitude_cells_count // 2, longitude_cells_count // 2)  # Start in the middle

        self.__current_pos = self.__init_position
        self.__direction = 'down'
        self.__score = 0
        self.__prev_grid = None
        self.__is_game = True

        self.init_position()
        self.get_root().bind('<Key>', self.clickHandler)
        self.update_canvas()
        # self.create_buttons()
        self.draw()
        self.mainloop()

    def init_position(self):
        init_cell_number = self.get_cell_number_from_coordinates(self.__init_position[0], self.__init_position[1])
        self.set_cell(init_cell_number, Snake())
        self.plant_rand_apple()

    def plant_rand_apple(self):
        empty_cells = self.get_same_value_cell_numbers(EmptyCell())
        random_cell_number = random.choice(empty_cells)
        self.set_cell(random_cell_number, Apple())

    def start(self):
        self.__is_game = True
        # self.update_canvas()

    def stop(self):
        self.__is_game = False

    def get_current_pos(self):
        return self.__current_pos

    def set_current_pos(self, new_pos):
        self.__current_pos = new_pos

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def get_score(self):
        return self.__score

    def update_score(self, value):
        self.__score += value

    def copy_grid(self):
        copied_grid = [[cell for cell in row] for row in self.get_grid()]
        return copied_grid

    def set_prev_grid(self, grid):
        self.__prev_grid = [[cell for cell in row] for row in grid]

    def get_prev_grid(self):
        return self.__prev_grid

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

    def clickHandler(self, event):
        if (event.keysym == "Left"):
            self.turn_left()
        elif (event.keysym == "Right"):
            self.turn_right()

    def step(self):
        self.set_prev_grid(self.copy_grid())

        # Removing the old cell before moving forward
        x, y = self.get_current_pos()
        current_cell_number = self.get_cell_number_from_coordinates(x, y)
        self.set_cell(current_cell_number, EmptyCell())

        # Moving forward
        self.move_forward()

        # Adding the new cell after moving forward
        new_x, new_y = self.get_current_pos()
        new_cell_number = self.get_cell_number_from_coordinates(new_x, new_y)

        if self.get_cell(new_cell_number) == Apple():
            self.update_score(1)
            self.plant_rand_apple()
            self.set_cell(current_cell_number, Snake())  # Keep the previous tail

            # Check if score meets a threshold to increase snake length
            if self.get_score() % 2 == 0:  # Adjust the threshold as needed
                # Add a new segment to the snake's body
                snake_body = self.get_grid_positions(Snake)
                tail_position = snake_body[-1] if snake_body else self.__current_pos
                new_tail_position = (tail_position[0] + 1, tail_position[1])  # Example: Extend tail to the right
                tail_cell_number = self.get_cell_number_from_coordinates(*new_tail_position)
                self.set_cell(tail_cell_number, Snake())

        elif self.get_cell(new_cell_number) == Snake():
            self.stop()  # Game over

        self.set_cell(new_cell_number, Snake())

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
    LINES_COUNT = 25
    COLUMNS_COUNT = 25
    cell_size = 10
    gutter_size = 0
    margin_size = 10
    show_content = True
    show_grid_lines = True
    background_color = 'white'
    foreground_color = 'black'
    gridlines_color = 'black'

    app = SnakeGame(root, "Snake", LINES_COUNT, COLUMNS_COUNT, background_color, foreground_color, gridlines_color,
                    cell_size, gutter_size, margin_size, show_content, show_grid_lines, width=80, height=50)
