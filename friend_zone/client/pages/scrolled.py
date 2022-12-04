from .base import BasicWin


import tkinter as tk

class ScrolledWin(BasicWin):
    def __init__(self, win, geometry, app):
        self.my_canvas = None
        self.second_frame = None
        self.my_scrollbar = None
        super(ScrolledWin, self).__init__(win, geometry, app)

    def update_win(self):
        super().update()
        try:
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        except tk.TclError as e:
            print(e)

    def load(self):
        self.main_frame = tk.Frame(self.win)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        # canvas
        self.my_canvas = tk.Canvas(self.main_frame)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # scrollbar
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.update_win())

        self.second_frame = tk.Frame(self.my_canvas)

        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw")