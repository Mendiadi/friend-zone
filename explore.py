import enum
import hashlib
import os
import threading

import tkinter as tk

def load_assets():

    img = tk.PhotoImage (file="assets/bg_login.png")
    return img

class AppStates(enum.Enum):
    LOGIN = "login"
    EXPLORE = "explore"


class ComponentCreator:
    @staticmethod
    def create_text_label(root,text,color="white",fg_color="black"):
        label = tk.Label(root,text=text,
                         font="none 10 bold",
                         bg=color,
                         fg=fg_color,

                         )
        return label

    @staticmethod
    def create_post_label(root, h1, text):
        can = tk.Canvas(root, height=200, width=500, bg="red")
        label = tk.Label(can, text=h1, font="none 20 bold", height=0, width=len(h1) + 1)
        txt = tk.Label(can, text=text, font="none 12", height=0, width=len(text) + 1, bg="red")
        txt.place_configure(x=100, y=100)
        label.place_configure(x=10, y=10)
        can.pack_configure(padx=250, pady=50)
        return can

    @staticmethod
    def create_entry(root,text_var):
        return tk.Entry(root,textvariable=text_var,font="none 20",bg="light blue",border=1)

    @staticmethod
    def create_button(root,text,func,state,size):
        return tk.Button(root, text=text, command=func, state=state,
                         highlightbackground="blue",height=size[0],width=size[1],bg="deepskyblue")

class BasicWin:
    def __init__(self, win: tk.Tk, geometry, app):
        self.win = win
        self.app = app
        self.win.geometry(geometry)

    def load(self): ...

    def kill(self): ...

    def mainloop(self):
        self.win.mainloop()


class ExploreWin(BasicWin):

    def __init__(self, win, geometry, app):
        super(ExploreWin, self).__init__(win, geometry, app)
        self.second_frame = None

        self.load()

    def update_win(self, my_canvas):
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
                        command=lambda: self.onclick(my_canvas, second_frame, "my post",
                                                     "im love eat bananas in the sea"))
        btn.pack()
        ComponentCreator.create_text_label(second_frame, "Your Feed").pack()



    def reload(self, ):
        for post in self.app.posts:
            post.pack()

    def onclick(self, c, root, h1, text):
        label = ComponentCreator.create_post_label(root, h1, text)
        self.app.posts.append(label)
        self.update_win(c)
        self.reload()


class LoginWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(LoginWin, self).__init__(win, geometry, app)
        img = load_assets()
        self.win.resizable(False,False)
        self.bg = tk.Label(self.win, image=img)
        self.bg.image = img
        self.login_btn = ComponentCreator.create_button(self.win, "Login",
                        self.login_btn_onclick,"normal",(5,60))
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.email_field = ComponentCreator.create_entry(self.win,self.email_var)
        self.password_field = ComponentCreator.create_entry(self.win,self.password_var)
        self.validate_job = None
        self.email_text = ComponentCreator.create_text_label(self.win,"Your Email:",color="light blue")
        self.pass_text = ComponentCreator.create_text_label(self.win,"Your Password:",color="light blue")

    def login_btn_onclick(self):


        response = self.app.login(self.email_var.get(), self.password_var.get())
        if response == 1:
            self.win.after_cancel(self.validate_job)
            self.kill()
            self.app.state = AppStates.EXPLORE
            self.app.update_content()

        else:
            # show error
            self.password_field.delete(0, tk.END)

    def kill(self):
        self.email_text.destroy()
        self.pass_text.destroy()
        self.login_btn.destroy()
        self.email_field.destroy()
        self.password_field.destroy()
        self.win.clipboard_clear()

    def validate_input(self):
        if len(self.email_var.get()) < 3:
            self.login_btn.config(state="disabled")
        else:
            self.login_btn.config(state="active")
        self.validate_job = self.win.after(1, self.validate_input)

    def load(self):
        self.bg.place(y=0, x=0)
        pad_y = 10
        self.email_text.place(y=480,x=330)
        self.email_field.place(y=450,x=330)
        self.pass_text.place(y=580,x=330)
        self.password_field.place(y=545,x=330)
        self.login_btn.place(y=680,x=290)


        self.validate_input()



class App:
    def __init__(self):
        self.state = AppStates.LOGIN
        self.win = tk.Tk()

        self.root = LoginWin(self.win, "1000x1000", self)
        self.root.load()
        self.posts = []

    def login(self, email, password):
        hash = hashlib.md5(password.encode())
        # requests login
        # response 200 -> return ok
        # response bad return not ok
        print(email, hash.hexdigest())
        return 1

    def update_content(self):
        threading.Thread(target=self.state_gui, daemon=True).start()

    def state_gui(self):
        print(self.state)
        if self.state == AppStates.EXPLORE and type(self.root) != ExploreWin:
            self.root.kill()
            self.root = ExploreWin(self.win, "1000x1000", self)


def run_app():


    app = App()
    app.root.mainloop()


run_app()
