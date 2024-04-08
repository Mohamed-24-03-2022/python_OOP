import tkinter as tk
from S07_TP14_01 import Turmite, Human
from conway import Conway
from langtonAnt import LangtonAnt
from snake import SnakeGame


class LangtonAntWindow():
    def __init__(self, **kw):
        self.__master = tk.Tk()
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
        self.__game = LangtonAnt(self.__master, "Turmite", LINES_COUNT, COLUMNS_COUNT, background_color, foreground_color, gridlines_color,
                                 cell_size, gutter_size, margin_size, show_content, show_grid_lines, width=80, height=50)


class ConwayWindow():
    def __init__(self, **kw):
        self.__master = tk.Tk()
        LINES_COUNT = 30
        COLUMNS_COUNT = 60
        CELL_SIZE = 20
        GUTTER_SIZE = 0
        MARGIN_SIZE = 10
        self.__game = Conway(self.__master, "Terre",  LINES_COUNT, COLUMNS_COUNT,
                             initial_population={Human}, cell_size=CELL_SIZE, gutter_size=GUTTER_SIZE,
                             margin_size=MARGIN_SIZE, width=80, height=50)


class SnakeGameWindow():
    def __init__(self, **kw):
        self.__master = tk.Tk()
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
        self.__game = SnakeGame(self.__master, "Snake", LINES_COUNT, COLUMNS_COUNT, background_color, foreground_color, gridlines_color,
                                cell_size, gutter_size, margin_size, show_content, show_grid_lines, width=80, height=50)


class MyApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("OOP PROJECT")
        tk.Button(self, text='Conway game', command=self.openConway).pack(side=tk.LEFT)
        tk.Button(self, text='LangtonAnt game', command=self.openLangtonAnt).pack(side=tk.LEFT)
        tk.Button(self, text='Snake game', command=self.openSnakeGame).pack(side=tk.LEFT)
        fr = tk.Frame(self)
        fr.pack(side=tk.BOTTOM)
        tk.Button(fr, text='Quit', command=self.quit).pack(side=tk.LEFT)

    def openConway(self):
        self.destroy()
        ConwayWindow()

    def openLangtonAnt(self):
        self.destroy()
        LangtonAntWindow()

    def openSnakeGame(self):
        self.destroy()
        SnakeGameWindow()


if __name__ == '__main__':
    MyApp().mainloop()
