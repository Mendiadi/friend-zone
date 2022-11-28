import threading
import time
import tkinter as tk


class BasicWin:
    def __init__(self,win:tk.Tk,geometry,app):
        self.win = win
        self.app = app
        self.win.geometry(geometry)


    def load(self):...

    def kill(self):...

    def mainloop(self):
        self.win.mainloop()

class ExploreWin(BasicWin):

    def __init__(self,win,geometry,app):
        super(ExploreWin, self).__init__(win,geometry,app)

        self.load()

    def update_win(self,my_canvas):
        self.win.update()
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))

    def kill(self):
        self.win.clipboard_clear()

    def load(self):
        main_frame = tk.Frame(self.win)
        main_frame.pack(fill=tk.BOTH, expand=1)
        # canvas
        my_canvas = tk.Canvas(main_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # scrollbar
        my_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: self.update_win(my_canvas))

        second_frame = tk.Frame(my_canvas)

        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        btn = tk.Button(second_frame, text="create",
                        command=lambda: self.onclick(my_canvas,second_frame, "my post", "im love eat bananas in the sea"))
        btn.pack()
        for i in range(15):
            self.create_post_label(second_frame,f"mypost{i}","im like you").pack()
        self.update_win(my_canvas)

    def create_post_label(self,root, h1, text):
        can = tk.Canvas(root,height=200,width=500,bg="red")
        label = tk.Label(can, text=h1, font="none 20 bold", height=0, width=len(h1) + 1)
        txt = tk.Label(can, text=text, font="none 12", height=0, width=len(text) + 1, bg="red")
        txt.place_configure(x=100, y=100)
        label.place_configure(x=10, y=10)
        can.pack_configure(padx=250,pady=50)
        return can


    def reload(self,):

        for post in self.app.posts:
            post.pack()

    def onclick(self,c,root, h1, text):

        label = self.create_post_label(root, h1, text)
        self.app.posts.append(label)
        self.update_win(c)
        self.reload()

class LoginWin(BasicWin):
    def __init__(self,win,geometry,app):
        super(LoginWin, self).__init__(win,geometry,app)
        self.login_btn = tk.Button(self.win,text="click",command=self.login)

    def login(self):
        self.kill()
        self.app.state = "explore"
    def kill(self):
        self.login_btn.destroy()
        self.win.clipboard_clear()

    def load(self):

        self.login_btn.pack()



class App:
    def __init__(self):
        self.state = "login"
        self.win = tk.Tk()
        self.root = LoginWin(self.win, "800x800", self)
        self.root.load()
        self.posts = []
        threading.Thread(target=self.state_gui,daemon=True).start()

    def state_gui(self):
        while True:
            time.sleep(0.2)
            print(self.state)
            if self.state == "explore" and type(self.root) != ExploreWin:
                self.root.kill()
                self.root = ExploreWin(self.win,"1000x1000",self)

def run_app():
    app = App()
    app.root.mainloop()


run_app()