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

        self.__current_pos = [self.__init_position]
        self.__direction = 'down'
        self.__score = 0
        self.__prev_grid = None
        self.__is_game = True
        self.speed = 200
        self.string_var = tk.StringVar()

        self.get_root().title("Snake Game")
        self.add_keyboard_events()
        self.init_position()
        self.start()
        self.create_buttons()
        self.draw()
        self.mainloop()

    def init_position(self):
        init_cell_number = self.get_cell_number_from_coordinates(self.__init_position[0], self.__init_position[1])
        self.set_cell(init_cell_number, Snake())
        self.plant_rand_apple()

    def add_keyboard_events(self):
        self.get_root().bind('<Key>', self.clickHandler)

    def plant_rand_apple(self):
        empty_cells = self.get_same_value_cell_numbers(EmptyCell())
        random_cell_number = random.choice(empty_cells)
        self.set_cell(random_cell_number, Apple())

    def create_buttons(self):
        # Bouton de fermeture
        self.__b_quit = tk.Button(self.get_root(), text='Close', command=self.quit)
        self.__b_quit.pack(side=tk.BOTTOM)

        btn_frame = tk.Frame(self.get_root())
        btn_frame.pack(side=tk.BOTTOM)
        start_button = tk.Button(btn_frame, text="Démarrer", command=self.start)
        start_button.pack(side=tk.LEFT)
        stop_button = tk.Button(btn_frame, text="Arrêter", command=self.stop)
        stop_button.pack(side=tk.LEFT)
        slow_speed_button = tk.Button(btn_frame, text="vitesse lente", command=lambda: self.set_speed(200))
        slow_speed_button.pack(side=tk.LEFT)
        med_speed_button = tk.Button(btn_frame, text="vitesse moyenne", command=lambda: self.set_speed(100))
        med_speed_button.pack(side=tk.LEFT)
        high_speed_button = tk.Button(btn_frame, text="vitesse rapide", command=lambda: self.set_speed(50))
        high_speed_button.pack(side=tk.LEFT)

        self.string_var.set(f"Score: {self.get_score()}")
        tk.Label(btn_frame, textvariable=self.string_var).pack(side=tk.LEFT)

    def set_speed(self, speed):
        self.speed = speed

    def start(self):
        self.__is_game = True
        self.update_canvas()

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

    # TODO  simplifie THIS function
    def move_forward(self):
        current_positions = self.get_current_pos()
        head_x, head_y = current_positions[0]  # Get the current head position

        # Determine the new head position based on the direction
        if self.get_direction() == 'up':
            new_head = (head_x - 1, head_y)
        elif self.get_direction() == 'down':
            new_head = (head_x + 1, head_y)
        elif self.get_direction() == 'left':
            new_head = (head_x, head_y - 1)
        elif self.get_direction() == 'right':
            new_head = (head_x, head_y + 1)

        new_head = (new_head[0] % self.get_columns_count(), new_head[1] % self.get_lines_count())

        # Update the snake's positions
        updated_positions = [new_head]  # Start with the new head position

        # Update the positions for the rest of the snake's body
        for i in range(1, len(current_positions)):
            updated_positions.append(current_positions[i-1])  # Append the previous position

        self.set_current_pos(updated_positions)

    def clickHandler(self, event):
        if (event.keysym == "Left"):
            self.turn_left()
        elif (event.keysym == "Right"):
            self.turn_right()

    def check_death(self, current_positions):
        next_head_position = current_positions[0]
        direction = self.get_direction()
        l, c = self.get_lines_count(), self.get_columns_count()
        # here i predict the next head position based on the current direction
        # then i check if the next head position is a snake's position

        next_head_cell_number = self.get_cell_number_from_coordinates(
            (next_head_position[0]-2) % l, next_head_position[1])
        if (direction == 'up' and self.get_cell(next_head_cell_number) == Snake()):
            self.stop()

        next_head_cell_number = self.get_cell_number_from_coordinates(
            (next_head_position[0]+2) % l, next_head_position[1])
        if (direction == 'down' and self.get_cell(next_head_cell_number) == Snake()):
            self.stop()

        next_head_cell_number = self.get_cell_number_from_coordinates(
            next_head_position[0], (next_head_position[1]-2) % c)
        if (direction == 'left' and self.get_cell(next_head_cell_number) == Snake()):
            self.stop()

        next_head_cell_number = self.get_cell_number_from_coordinates(
            next_head_position[0], (next_head_position[1]+2) % c)
        if (direction == 'right' and self.get_cell(next_head_cell_number) == Snake()):
            self.stop()

    def remove_snake_from_grid(self, current_positions):
        for (x, y) in current_positions:
            cell_number = self.get_cell_number_from_coordinates(x, y)
            if (self.get_cell(cell_number) == Snake()):
                cell_number = self.get_cell_number_from_coordinates(x, y)
                self.set_cell(cell_number, EmptyCell())

    def draw_new_snake_positions(self):
        new_positions = self.get_current_pos()
        for (new_x, new_y) in new_positions:
            new_cell_number = self.get_cell_number_from_coordinates(new_x, new_y)
            self.set_cell(new_cell_number, Snake())

    def eat_apple_and_grow_snake(self):
        head_position = self.get_current_pos()[0]
        head_cell_number = self.get_cell_number_from_coordinates(head_position[0], head_position[1])
        direction = self.get_direction()

        if (self.get_cell(head_cell_number) == Apple()):
            self.update_score(1)
            self.string_var.set(f"Score: {self.get_score()}")

            self.plant_rand_apple()
            if (direction == 'up'):
                self.set_current_pos([(head_position[0]+1, head_position[1])] + self.get_current_pos())
            elif (direction == 'down'):
                self.set_current_pos([(head_position[0]-1, head_position[1])] + self.get_current_pos())
            elif (direction == 'left'):
                self.set_current_pos([(head_position[0], head_position[1]-1)] + self.get_current_pos())
            elif (direction == 'right'):
                self.set_current_pos([(head_position[0], head_position[1]+1)] + self.get_current_pos())

    def step(self):
        self.set_prev_grid(self.copy_grid())

        current_positions = self.get_current_pos()

        self.check_death(current_positions)

        # remove old snake's positions from the grid
        self.remove_snake_from_grid(current_positions)

        self.move_forward()

        # appending the head position that ate an apple to the snake body's positions
        self.eat_apple_and_grow_snake()

        # draw the snake's new positions
        self.draw_new_snake_positions()

    def update_canvas(self):
        if (self.__is_game):
            self.step()

        for cell_number in range(self.get_cells_count()):
            i, j = self.get_coordinates_from_cell_number(cell_number)
            if (self.get_cell(cell_number) == Apple()):
                self.itemconfigure(f'c_{cell_number}', fill='red')

            if (self.get_cell(cell_number) != self.get_prev_grid()[i][j]):
                cell_type = self.get_cell(cell_number)
                color = 'green' if (cell_type == Snake()) else 'white'

                self.itemconfigure(f't_{cell_number}', text=cell_type)
                self.itemconfigure(f'c_{cell_number}', fill=color)

        self.after(self.speed, self.update_canvas)


if __name__ == '__main__':
    root = tk.Tk()
    LINES_COUNT = 30
    COLUMNS_COUNT = 30
    cell_size = 20
    gutter_size = 0
    margin_size = 10
    show_content = True
    show_grid_lines = True
    background_color = 'white'
    foreground_color = 'black'
    gridlines_color = 'black'

    app = SnakeGame(root, "Snake", LINES_COUNT, COLUMNS_COUNT, background_color, foreground_color, gridlines_color,
                    cell_size, gutter_size, margin_size, show_content, show_grid_lines, width=80, height=50)
