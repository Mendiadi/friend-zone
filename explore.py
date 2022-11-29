import enum
import threading
import time
import tkinter as tk

import requests

import api_fecth


def load_assets():
    img = tk.PhotoImage(file="assets/bg_login.png")
    return img


class AppStates(enum.Enum):
    HOME = 0
    LOGIN = 1
    EXPLORE = 2
    REGISTER = 3
    PROFILE = 4


class ComponentCreator:
    @staticmethod
    def create_text_label(root, text, color="white", fg_color="black"):
        label = tk.Label(root, text=text,
                         font="none 10 bold",
                         bg=color,
                         fg=fg_color,

                         )
        return label

    @staticmethod
    def create_user_label(root, email, func):
        # can = tk.Canvas(root,bg="red",height=50,width=100)
        # label = tk.Label(can, text=email, font="none 12 bold", height=0, width=len(email),bg="red")
        # label.place_configure(x=15, y=15)

        can = tk.Button(root, text=email, bg="red", border=0, font="none 12 bold", command=lambda: func(email))
        return can

    @staticmethod
    def create_post_label(root, h1, text, func=None, post_id=None):

        root.config(bg="cyan")
        can = tk.Canvas(root, height=200, width=500, bg="red")
        label = tk.Label(can, text=h1, font="none 20 bold", height=0, width=len(h1) + 1)
        txt = tk.Label(can, text=text, font="none 12", height=0, width=len(text) + 1, bg="red")
        txt.place_configure(x=100, y=100)

        def wrap():
            func(post_id)

        if func:
            btn = tk.Button(can, text="del", command=wrap)
            btn.place_configure(x=470, y=1)
        label.place_configure(x=10, y=10)
        can.pack_configure(padx=250, pady=50)
        return can

    @staticmethod
    def create_entry(root, text_var):
        return tk.Entry(root, textvariable=text_var, font="none 20", bg="light blue", border=1)

    @staticmethod
    def create_button(root, text, func, state, size=None):
        if not size:
            return tk.Button(root, text=text, command=func, state=state,
                             highlightbackground="blue", bg="deepskyblue")
        return tk.Button(root, text=text, command=func, state=state,
                         highlightbackground="blue", height=size[0], width=size[1], bg="deepskyblue")


class BasicWin:
    def __init__(self, win: tk.Tk, geometry, app):
        self.win = win
        self.app = app
        self.win.geometry(geometry)

    def load(self): ...

    def kill(self):
        for w in self.win.winfo_children():
            w.destroy()

    def mainloop(self):
        self.win.mainloop()


class ScrolledWin(BasicWin):
    def __init__(self, win, geometry, app):
        self.my_canvas = None
        self.second_frame = None
        self.my_scrollbar = None
        super(ScrolledWin, self).__init__(win, geometry, app)

    def update_win(self):
        self.win.update()
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

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


class ExploreWin(ScrolledWin):

    def __init__(self, win, geometry, app):
        super(ExploreWin, self).__init__(win, geometry, app)
        self.posts = []
        self.logged_user = self.app.user
        self.post_data = tk.StringVar()
        self.add_post_entry = None

    def move_to_home_page(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    def load(self):
        super().load()
        btn = tk.Button(self.second_frame, text="create",
                        command=lambda: self.onclick(self.my_canvas, self.second_frame))

        ComponentCreator.create_text_label(self.second_frame, "Your Feed").pack(pady=5)
        ComponentCreator.create_button(self.second_frame, "HOME", self.move_to_home_page, "normal").pack(pady=5)
        self.add_post_entry = ComponentCreator.create_entry(self.second_frame, self.post_data)
        self.add_post_entry.pack(pady=5)
        btn.pack(pady=10)

        self.fetch_all_posts()

    def fetch_all_posts(self, ):
        for post in self.posts:
            post.destroy()
        self.posts.clear()
        for i, post in enumerate(self.app.get_posts(self.app.user)):
            if i > 25:
                break
            p = ComponentCreator.create_post_label(self.second_frame, post.user_email, post.text,
                                                   self.delete_post_onclick, post.post_id)
            self.posts.append(p)

            p.pack(pady=10)
        print(self.posts)
        self.update_win()

    def delete_post_onclick(self, post_id):
        print(post_id)
        if self.app.delete_post(post_id):
            self.fetch_all_posts()

    def onclick(self, c, root):
        # c means canvas to update scrollbar
        code, post = self.app.create_post(self.post_data.get())
        if not code:
            return
        self.fetch_all_posts()
        self.update_win()


class ProfileWin(ScrolledWin):
    def __init__(self, win, geometry, app):
        super(ProfileWin, self).__init__(win, geometry, app)

    def go_back_onclick(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    def fetch_all_posts(self, ):
        for i, post in enumerate(self.app.get_posts(self.app.temp_user_profile)):
            if i > 25:
                break
            p = ComponentCreator.create_post_label(self.second_frame, post.user_email, post.text)

            p.pack()

        self.update_win()

    def load(self):
        super().load()
        ComponentCreator.create_text_label(self.second_frame, f"{self.app.temp_user_profile} Profile").pack()
        back_btn = ComponentCreator.create_button(
            self.second_frame, "Back", self.go_back_onclick, "normal"
        )
        back_btn.pack()
        self.fetch_all_posts()


class HomeWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(HomeWin, self).__init__(win, geometry, app)
        self.search_query = tk.StringVar()
        self.search_bar = ComponentCreator.create_entry(self.win, self.search_query)
        self.explore_btn = ComponentCreator.create_button(self.win, "EXPLORE", self.explore_page_onclick, "normal")
        self.results = []
        self.result_labels = []
        self.run = True
        threading.Thread(target=self.search_thread, daemon=True).start()

    def kill(self):
        super().kill()
        self.run = False

    def explore_page_onclick(self):
        self.app.state = AppStates.EXPLORE
        self.app.update_content()

    def search_onclick(self):
        if self.search_query.get():
            self.fetch_results(self.app.search(self.search_query.get()))

    def search_thread(self):
        temp = None
        while self.run:
            time.sleep(0.1)

            if self.search_query.get() != temp:
                temp = self.search_query.get()
                self.search_onclick()

    def move_to_user_page(self, email):
        print("*****************move")
        self.app.state = AppStates.PROFILE
        self.app.temp_user_profile = email
        self.app.update_content()

    def clear_results(self):
        for l in self.result_labels:
            l.destroy()

    def fetch_results(self, res):
        print(res)
        self.clear_results()
        self.result_labels.clear()
        for u in res:
            a = ComponentCreator.create_user_label(self.win, u.email, self.move_to_user_page)
            a.pack(pady=10)
            self.result_labels.append(a)

    def load(self):
        self.explore_btn.pack(pady=10)
        ComponentCreator.create_text_label(self.win, "Search for Users", "cyan").pack(pady=5)
        self.search_bar.pack(pady=10)


class RegisterWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(RegisterWin, self).__init__(win, geometry, app)
        self.register_btn = ComponentCreator.create_button(self.win, "Register",
                                                           self.register_btn_onclick, "normal", (5, 60))
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.re_password_var = tk.StringVar()
        self.email_field = ComponentCreator.create_entry(self.win, self.email_var)
        self.password_field = ComponentCreator.create_entry(self.win, self.password_var)
        self.re_password_field = ComponentCreator.create_entry(self.win, self.re_password_var)
        self.validate_job = None
        self.email_text = ComponentCreator.create_text_label(self.win, "Your Email:", color="light blue")
        self.pass_text = ComponentCreator.create_text_label(self.win, "Your Password:", color="light blue")
        self.re_pass_text = ComponentCreator.create_text_label(self.win, "Your Password Again:", color="light blue")

    def register_btn_onclick(self):

        response = self.app.register(self.email_var.get(),
                                     self.password_var.get(), self.re_password_var.get())
        if response == 1:
            self.kill()
            self.app.state = AppStates.LOGIN
            self.app.update_content()

        else:
            # show error
            print(response)
            self.password_field.delete(0, tk.END)
            self.re_password_field.delete(0, tk.END)

    def validate_input(self):
        if len(self.email_var.get()) < 3:
            self.register_btn.config(state="disabled")
        else:
            self.register_btn.config(state="active")
        self.validate_job = self.win.after(1, self.validate_input)

    def load(self):
        pad = 10

        self.email_text.pack(pady=pad)
        self.email_field.pack(pady=pad)
        self.pass_text.pack(pady=pad)
        self.password_field.pack(pady=pad)
        self.re_pass_text.pack(pady=pad)
        self.re_password_field.pack(pady=pad)

        self.register_btn.pack(pady=pad)


class LoginWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(LoginWin, self).__init__(win, geometry, app)
        img = load_assets()
        self.win.resizable(False, False)
        self.bg = tk.Label(self.win, image=img)
        self.bg.image = img
        self.login_btn = ComponentCreator.create_button(self.win, "Login",
                                                        self.login_btn_onclick, "normal", (5, 60))
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.email_field = ComponentCreator.create_entry(self.win, self.email_var)
        self.password_field = ComponentCreator.create_entry(self.win, self.password_var)
        self.validate_job = None
        self.email_text = ComponentCreator.create_text_label(self.win, "Your Email:", color="light blue")
        self.pass_text = ComponentCreator.create_text_label(self.win, "Your Password:", color="light blue")
        self.register_btn = ComponentCreator.create_button(self.win, "sign up", self.sign_up_page, "normal", (5, 60))

    def sign_up_page(self):
        self.app.state = AppStates.REGISTER
        self.app.update_content()

    def login_btn_onclick(self):

        response = self.app.login(self.email_var.get(), self.password_var.get())
        if response == 1:
            self.win.after_cancel(self.validate_job)
            self.app.state = AppStates.HOME
            self.app.update_content()

        else:
            # show error
            print(response)
            self.password_field.delete(0, tk.END)

    def validate_input(self):
        if self.app.state == AppStates.LOGIN:
            if len(self.email_var.get()) < 3:
                self.login_btn.config(state="disabled")
            else:
                self.login_btn.config(state="active")
            self.validate_job = self.win.after(1, self.validate_input)

    def load(self):
        self.bg.place(y=0, x=0)
        self.register_btn.place(x=290, y=800)
        self.email_text.place(y=480, x=330)
        self.email_field.place(y=450, x=330)
        self.pass_text.place(y=580, x=330)
        self.password_field.place(y=545, x=330)
        self.login_btn.place(y=680, x=290)

        self.validate_input()


class App:
    def __init__(self):
        self.state = AppStates.LOGIN
        self.win = tk.Tk()
        self.user = None
        self.MAXSIZE = "1000x1000"
        self.root = LoginWin(self.win, self.MAXSIZE, self)
        self.root.load()
        self.temp_user_profile = None

    def search(self, query):
        with api_fecth.UsersAPI(requests.session()) as session:
            res = session.search(query)
        return res

    def delete_post(self, post):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.delete_post(post)
            print(res[0])
            if res[1] == 200:
                return 1
            return 0

    def register(self, email, password, re_password):
        if password != re_password:
            return 0
        with api_fecth.UsersAPI(requests.session()) as session:

            res = session.register(email, password)
            print(res)
        if type(res) == str:
            return 0
        return 1

    def create_post(self, text):
        from api_fecth import CreatePost, Post
        post = CreatePost(text)
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.create_post(post, self.user)
            if type(res) == Post:

                return 1, res
            else:
                return 0, res

    def get_posts(self, email):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_posts_by_user(email)
            if type(res) == list:
                return res
            else:
                print(res)
                return []

    def login(self, email, password):

        # requests login
        # response 200 -> return ok
        # response bad return not ok
        with api_fecth.UsersAPI(requests.session()) as session:
            res = session.login(email, password)
        if res[1] == 200:
            print(res)
            self.user = email
            return 1
        return res[0]

    def update_content(self):
        threading.Thread(target=self.state_gui, daemon=True).start()

    def switch_page(self, page: type):
        if type(self.root) != page:
            self.root.kill()
            self.root = page(self.win, self.MAXSIZE, self)
            self.root.load()

    def state_gui(self):

        if self.state == AppStates.EXPLORE:
            page = ExploreWin

        elif self.state == AppStates.REGISTER:

            page = RegisterWin
        elif self.state == AppStates.LOGIN:

            page = LoginWin

        elif self.state == AppStates.HOME:

            page = HomeWin

        elif self.state == AppStates.PROFILE:

            page = ProfileWin

        else:
            raise Exception("we run for some errors right now...")
        self.switch_page(page)


def run_app():
    app = App()
    app.root.mainloop()
