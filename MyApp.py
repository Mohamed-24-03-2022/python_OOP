import tkinter as tk
from S07_TP14_01 import Turmite, Human
from Conway import Conway
from Turmites import Turmites
# from S08_TP16_3_snake import SnakeGame


class TurmitesWindow(tk.Toplevel):

    def __init__(self, master, **kw):
        tk.Toplevel.__init__(self, master, **kw)
        self.__master = master
        self.__game = Turmites(self, 120, 200, turmite_type=Turmite, turmites_count=8, cell_size=5)
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
        tk.Button(self, text='Turmites game', command=lambda: TurmitesWindow(self)).pack(side=tk.LEFT)
        # tk.Button(self, text='Snake game', command=lambda: SnakeGameWindow(self)).pack(side=tk.LEFT)
        tk.Button(self, text='Quit', command=self.quit).pack(side=tk.RIGHT)

    def openConway(self):
        self.quit()
        ConwayWindow(self)


if __name__ == '__main__':
    MyApp().mainloop()
