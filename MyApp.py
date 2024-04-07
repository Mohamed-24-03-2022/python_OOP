import tkinter as tk
from S07_TP14_01 import Turmite, Human
from conway import Conway
from langtonAnt import LangtonAnt
# from S08_TP16_3_snake import SnakeGame


class LangtonAntWindow(tk.Toplevel):

    def __init__(self, master, **kw):
        tk.Toplevel.__init__(self, master, **kw)
        self.__master = master
        self.__game = LangtonAnt(self, 120, 200, turmite_type=Turmite, LangtonAnt_count=8, cell_size=5)
        self.__game.pack()
        tk.Button(self, text="Quit", command=self.destroy).pack()


class ConwayWindow():

    def __init__(self, root):
        self.__master = tk.Tk()
        self.__game = Conway(self.__master, "Terre", 40, 60, {
                             Human}, 25, 0, 10, width=80, height=50, show_gridlines=False)
        # self.__game.pack()
        # tk.Button(self, text="Quit", command=self.destroy).pack()


class MyApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Some Planets")
        tk.Button(self, text='Conway game', command=self.openConway).pack(side=tk.LEFT)
        tk.Button(self, text='LangtonAnt game', command=lambda: LangtonAntWindow(self)).pack(side=tk.LEFT)
        # tk.Button(self, text='Snake game', command=lambda: SnakeGameWindow(self)).pack(side=tk.LEFT)
        tk.Button(self, text='Quit', command=self.quit).pack(side=tk.RIGHT)

    def openConway(self):
        self.quit()
        ConwayWindow(self)


if __name__ == '__main__':
    MyApp().mainloop()
