import tkinter as tk

class BasicWin:
    def __init__(self, win: tk.Tk, geometry, app):
        self.win = win
        self.app = app
        self.win.geometry(geometry)
        self.win.resizable(False, False)

    def load(self): ...

    def kill(self):
        for w in self.win.winfo_children():
            w.destroy()

    def update(self):
        self.win.update()