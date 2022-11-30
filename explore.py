import dataclasses
import enum
import json
import threading
import time
import tkinter as tk
from collections import OrderedDict
from tkinter import messagebox
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
    LIKE_VIEW = 5


class ComponentCreator:
    @staticmethod
    def create_text_label(root, text, color="white", fg_color="black", font_size=10, bold=True):
        font = f"none {str(font_size)}"
        if bold:
            font += " bold"
        label = tk.Label(root, text=text,
                         font=font,
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
    def create_post_label(root, h1, text, func_del=None, func_edit=None, post=None, like_count=None, func_like=None):

        class PostComponent:
            def __init__(self, can, can2, label, txt, like_label, like_btn, post):
                self.can = can
                self.can2 = can2
                self.label = label
                self.txt = txt
                self.like_label = like_label
                self.like_btn = like_btn
                self.post = post

            def refresh(self, likes_count, app):
                self.txt.config(text=self.post.text)
                self.like_label.config(text=f"likes: {likes_count}")
                self.like_count = likes_count
                if self.post.post_id not in [p.post_id for p in app.get_likes_by_email(app.user)]:
                    self.like_btn.config(text="like", )
                    self.like_btn.place_configure(x=468)
                else:
                    self.like_btn.config(text="dislike")
                    self.like_btn.place_configure(x=450)

        color_bg2 = "cyan"
        color_bg = "deepskyblue3"
        root.config(bg="deepskyblue")
        can = tk.Canvas(root, height=200, width=500, bg=color_bg2)
        can2 = tk.Canvas(can, height=175, width=450, bg=color_bg)
        label = tk.Label(can2, text=h1, font="none 20 bold", height=0, width=len(h1) + 1, bg=color_bg2)
        txt = tk.Label(can2, text=text, font="none 12", height=0, width=len(text) + 1, bg=color_bg)
        txt.place_configure(x=100, y=100)
        like_btn = tk.Button(can, text="like", bg=color_bg2, command=lambda: wrap(0), border=0, font="none 10 bold")
        like_btn.place_configure(x=468, y=178)
        like_count = tk.Label(can, text=f"likes: {like_count}",
                              font="none 8", bg=color_bg2, width=len(f"likes: {like_count}") + 1)
        like_count.place_configure(x=1, y=180)
        print(post)

        def wrap(key):
            print(key)
            if key == 1:
                func_del(post.post_id)
            elif key == 2:
                func_edit(post)
            else:

                func_like(post.post_id)

        if func_del:
            btn = tk.Button(can, text="X", command=lambda: wrap(1), font="none 12 bold", bg=color_bg2, border=0
                            , activebackground="blue", highlightbackground="blue", highlightcolor="blue", fg="red")
            btn.place_configure(x=480, y=5)
        if func_edit:
            btn = tk.Button(can, text="E", command=lambda: wrap(2), font="none 12 bold", bg=color_bg2, border=0
                            , activebackground="blue", highlightbackground="blue", highlightcolor="blue")
            btn.place_configure(x=480, y=40)
        label.place_configure(x=0, y=0)
        can2.place_configure(x=10, y=10)
        can.pack_configure(padx=250, pady=50)
        label_post_created = PostComponent(can, can2, label, txt, like_count, like_btn, post)

        return label_post_created

    @staticmethod
    def create_entry(root, text_var, hide=False):

        hide = None if not hide else "*"

        return tk.Entry(root, textvariable=text_var, font="none 20", bg="light blue", border=1, show=hide)

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
        self.win.resizable(False, False)

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


class PostViewWin(ScrolledWin):
    def __init__(self, win, geometry, app):
        super(PostViewWin, self).__init__(win, geometry, app)
        self.posts = OrderedDict()

    def like_post_onclick(self, post_id):

        like = api_fecth.Like(self.app.user, post_id)
        self.app.post_like(like)

        self.fecth_post(post_id)

    def edit_post_onclick(self, post):
        pop_win = tk.Tk("edit")
        pop_win.geometry("300x300")

        e_entry = ComponentCreator.create_entry(pop_win, None)

        def edit_click(post_):
            post_.text = e_entry.get()

            self.app.edit_post(post_)
            # from_all = True if self.app.state == AppStates.EXPLORE else False
            self.fecth_post(post.post_id)
            pop_win.destroy()

        e_entry.pack(pady=10)
        ComponentCreator.create_button(pop_win, "edit", lambda: edit_click(post), "normal").pack(pady=10)

    def delete_post_onclick(self, post_id):
        print(post_id)
        if self.app.delete_post(post_id):
            from_all = True if self.app.state == AppStates.EXPLORE else False
            self.fetch_all_posts(from_all)

    def fecth_post(self, post_id):
        post = self.app.get_post_by_id(post_id)
        likes_count = self.app.get_likes_by_post(post_id)
        self.posts[post.post_id].post = post
        self.posts[post.post_id].refresh(likes_count, self.app)

    def fetch_liked_posts(self):
        for post in self.posts.values():
            post.can.destroy()
        posts = [like.post_id for like in self.app.get_likes_by_email(self.app.user)]
        for post in posts:
            p = self.app.get_post_by_id(post)
            likes_count = self.app.get_likes_by_post(post)

            if p.user_email == self.app.user:
                conf_label = self.delete_post_onclick, self.edit_post_onclick, p, likes_count
            else:
                conf_label = (None, None, p, likes_count)
            self.posts[post] = ComponentCreator.create_post_label(self.second_frame, p.user_email,
                                                                  p.text, *conf_label, func_like=self.like_post_onclick)
            self.posts[post].refresh(likes_count, self.app)
            self.posts[post].can.pack()

        self.update_win()

    def fetch_all_posts(self, from_all=False):
        for post in self.posts.values():
            post.can.destroy()
        self.posts.clear()
        posts = self.app.get_posts(self.app.temp_user_profile) if not from_all else self.app.get_all_posts()
        print(posts)
        for i, post in enumerate(posts):
            likes_count = self.app.get_likes_by_post(post.post_id)
            if i > 25:
                break
            if post.user_email == self.app.user:
                conf_label = self.delete_post_onclick, self.edit_post_onclick, post, likes_count
            else:
                conf_label = (None, None, post, likes_count)
            print(conf_label)
            p = ComponentCreator.create_post_label(self.second_frame, post.user_email, post.text,
                                                   *conf_label, func_like=self.like_post_onclick)
            self.posts[post.post_id] = p
            self.posts[post.post_id].refresh(likes_count, self.app)
            p.can.pack()

        self.update_win()


class ExploreWin(PostViewWin):

    def __init__(self, win, geometry, app):
        super(ExploreWin, self).__init__(win, geometry, app)
        self.post_data = tk.StringVar()
        self.add_post_entry = None

    def refresh_feed(self):
        self.fetch_all_posts(from_all=True)

    def move_to_home_page(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    def load(self):
        super().load()
        btn = tk.Button(self.second_frame, text="POST",
                        command=lambda: self.onclick(self.my_canvas, self.second_frame),
                        bg="deepskyblue3", border=0, font="none 15")

        ComponentCreator.create_text_label(self.second_frame, "Your Feed").pack(pady=5)
        home_btn = ComponentCreator.create_button(self.second_frame, "HOME", self.move_to_home_page,
                                                  "normal", size=(2, 10))

        home_btn.config(border=0, font="none 10 bold", bg="deepskyblue3")
        home_btn.pack(pady=5)
        ref_btn = ComponentCreator.create_button(self.second_frame, "refresh", self.refresh_feed,
                                                 "normal", size=(2, 10))
        ref_btn.config(border=0, font="none 10 bold", bg="deepskyblue3")

        ref_btn.pack(pady=5)
        self.add_post_entry = ComponentCreator.create_entry(self.second_frame, self.post_data)
        self.add_post_entry.pack(pady=5)
        btn.pack(pady=10)

        self.fetch_all_posts(from_all=True)

    def onclick(self, c, root):
        # c means canvas to update scrollbar
        data = self.post_data.get()
        self.add_post_entry.delete(0, tk.END)
        if not data:
            return
        code, post = self.app.create_post(data)
        if not code:
            return
        self.fetch_all_posts(from_all=True)

        self.update_win()


class LikesViewWin(PostViewWin):
    def __init__(self, win, geometry, app):
        super(LikesViewWin, self).__init__(win, geometry, app)

    def on_back_click(self):
        self.app.state = AppStates.PROFILE
        self.app.update_content()

    def load(self):
        super(LikesViewWin, self).load()
        ComponentCreator.create_button(self.second_frame, "back", self.on_back_click, "normal").pack()
        self.fetch_liked_posts()


class ProfileWin(PostViewWin):
    def __init__(self, win, geometry, app):
        super(ProfileWin, self).__init__(win, geometry, app)

    def go_back_onclick(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    def my_likes_onclick(self):
        self.app.state = AppStates.LIKE_VIEW
        self.app.update_content()

    def load(self):
        super().load()
        ComponentCreator.create_text_label(self.second_frame, f"{self.app.temp_user_profile} Profile").pack()
        if self.app.user == self.app.temp_user_profile:
            ComponentCreator.create_button(
                self.second_frame, "my likes", self.my_likes_onclick, "normal"
            ).pack()
        back_btn = ComponentCreator.create_button(
            self.second_frame, "Back", self.go_back_onclick, "normal"
        )
        back_btn.pack()
        self.fetch_all_posts()


class HomeWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(HomeWin, self).__init__(win, geometry, app)
        self.search_query = tk.StringVar()
        self.win.config(bg="grey")
        img = tk.PhotoImage(file="assets/bg_cool.png")
        self.bg = tk.Label(self.win, image=img)
        self.bg.image = img

        self.search_bar = ComponentCreator.create_entry(self.win, self.search_query)
        self.explore_btn = ComponentCreator.create_button(self.win, "EXPLORE", self.explore_page_onclick,
                                                          "normal", size=(2, 10))
        self.explore_btn.config(border=0, font="none 12 bold", bg="deepskyblue3")
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
        for i, u in enumerate(res):
            a = ComponentCreator.create_user_label(self.win, u.email, self.move_to_user_page)
            if i == 0:
                y = 200
            else:
                y = 200 + (50 * i)

            a.place(x=450, y=y)
            self.result_labels.append(a)

    def my_profile_onclick(self):
        self.move_to_user_page(self.app.user)

    def logout_onclick(self):
        if self.app.logout() == 1:
            self.app.state = AppStates.LOGIN
            self.app.update_content()


    def load(self):

        self.bg.place(x=0, y=0)
        profile_btn = ComponentCreator.create_button(self.win, "My Profile", self.my_profile_onclick, "normal", size=(2, 10))
        profile_btn.config(border=0, font="none 12 bold", bg="deepskyblue3")
        profile_btn.place(x=650, y=70)
        self.explore_btn.place(x=300, y=70)
        logout_btn = ComponentCreator.create_button(self.win,"logout",self.logout_onclick,"normal",size=(2,10))
        logout_btn.config(border=0, font="none 12 bold", bg="deepskyblue3")
        logout_btn.place(x=470,y=30)
        ComponentCreator.create_text_label(self.win, "Search for Users", "cyan", font_size=17).place(x=430, y=110)
        self.search_bar.place(x=370, y=150)


class RegisterWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(RegisterWin, self).__init__(win, geometry, app)
        self.win.config(bg="cyan")
        self.register_btn = ComponentCreator.create_button(self.win, "Register",
                                                           self.register_btn_onclick, "normal", (5, 60))
        self.back_btn = ComponentCreator.create_button(self.win, "Back",
                                                       self.back_to_login, "normal", (5, 60))
        self.back_btn.config(border=0)
        self.register_btn.config(border=0)
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.re_password_var = tk.StringVar()
        self.email_field = ComponentCreator.create_entry(self.win, self.email_var)
        self.password_field = ComponentCreator.create_entry(self.win, self.password_var, hide=True)
        self.re_password_field = ComponentCreator.create_entry(self.win, self.re_password_var, hide=True)
        self.validate_job = None
        self.email_text = ComponentCreator.create_text_label(self.win, "Your Email:",
                                                             color="light blue", font_size=12)
        self.pass_text = ComponentCreator.create_text_label(self.win, "Your Password:",
                                                            color="light blue", font_size=12)
        self.re_pass_text = ComponentCreator.create_text_label(self.win, "Your Password Again:",
                                                               color="light blue", font_size=12)
        self.email_field.config(border=0)
        self.password_field.config(border=0)
        self.re_password_field.config(border=0)
        self.email_text.config(bg="cyan")
        self.pass_text.config(bg="cyan")
        self.re_pass_text.config(bg="cyan")

    def back_to_login(self):
        self.app.state = AppStates.LOGIN
        self.app.update_content()

    def register_btn_onclick(self):

        response = self.app.register(self.email_var.get(),
                                     self.password_var.get(), self.re_password_var.get())
        if response == 1:
            self.win.after_cancel(self.validate_job)
            self.kill()
            self.app.state = AppStates.LOGIN
            self.app.update_content()

        else:
            # show error
            print(response)
            self.password_field.delete(0, tk.END)
            self.re_password_field.delete(0, tk.END)

    def validate_input(self):
        if self.app.state == AppStates.REGISTER:
            if len(self.email_var.get()) < 3 or len(self.re_password_var.get()) < 3 \
                    or len(self.password_var.get()) < 3:
                self.register_btn.config(state="disabled")
            else:
                self.register_btn.config(state="normal")

            self.validate_job = self.win.after(1, self.validate_input)

    def load(self):
        pad = 15
        a = ComponentCreator.create_text_label(self.win, "", fg_color="cyan")
        a.config(border=0, bg="cyan", pady=50)
        a.pack(pady=pad)
        self.email_text.pack(pady=pad)
        self.email_field.pack(pady=pad)
        self.pass_text.pack(pady=pad)
        self.password_field.pack(pady=pad)
        self.re_pass_text.pack(pady=pad)
        self.re_password_field.pack(pady=pad)

        self.register_btn.pack(pady=pad)
        self.back_btn.pack(pady=pad)
        self.validate_input()

    def kill(self):
        super().kill()


class LoginWin(BasicWin):
    def __init__(self, win, geometry, app):
        super(LoginWin, self).__init__(win, geometry, app)
        img = load_assets()
        self.win.resizable(False, False)
        self.bg = tk.Label(self.win, image=img)
        self.bg.image = img
        self.login_btn = ComponentCreator.create_button(self.win, "Login",
                                                        self.login_btn_onclick, "normal", (5, 60))
        self.login_btn.config(border=0)
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.email_field = ComponentCreator.create_entry(self.win, self.email_var)
        self.password_field = ComponentCreator.create_entry(self.win, self.password_var, hide=True)
        self.validate_job = None
        self.email_text = ComponentCreator.create_text_label(self.win, "Your Email:", color="light blue")
        self.pass_text = ComponentCreator.create_text_label(self.win, "Your Password:", color="light blue")
        self.register_btn = ComponentCreator.create_button(self.win, "sign up", self.sign_up_page, "normal", (5, 60))
        self.register_btn.config(border=0)
        self.error_plot = None

    def plot_error(self, info):
        if self.error_plot:
            self.error_plot.destroy()
        self.error_plot = ComponentCreator.create_text_label(self.win, f"Error: {info['error']}", fg_color="red",
                                                             color="deepskyblue", font_size=20, bold=True)
        self.error_plot.place(x=400, y=50)

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
            print(response, type(response))
            self.plot_error(response)

            self.password_field.delete(0, tk.END)

    def validate_input(self):
        if self.app.state == AppStates.LOGIN:
            if len(self.email_var.get()) < 3 or len(self.password_var.get()) < 3:
                self.login_btn.config(state="disabled")
            else:
                self.login_btn.config(state="normal")
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


def require_connection(func):
    def wrapper(*args, **kwargs):

        with api_fecth.API(requests.session()) as session:
            res = session.test_connection()

        if res == 0:
            messagebox.showerror("no connection", "your connection is disabled")
        else:
            return func(*args, **kwargs)

        return {"error":"no connection"}

    return wrapper


class App:

    def __init__(self):
        self.state = AppStates.LOGIN
        self.win = tk.Tk()
        self.win.title("MY FRIEND ZONE")
        self.user = None
        self.MAXSIZE = "1000x1000"
        self.root = LoginWin(self.win, self.MAXSIZE, self)
        self.root.load()
        self.temp_user_profile = None

    @require_connection
    def search(self, query):
        with api_fecth.UsersAPI(requests.session()) as session:
            res = session.search(query)
        return res

    @require_connection
    def edit_post(self, post):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.edit_post(post)
            print(res)

    @require_connection
    def delete_post(self, post):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.delete_post(post)
            print(res[0])
            if res[1] == 200:
                return 1
            return 0

    @require_connection
    def post_like(self, like):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.like_post(like)
            print(res[0])
        if res[1] == 201:
            return 1
        return 0

    @require_connection
    def register(self, email, password, re_password):
        if password != re_password:
            return 0
        with api_fecth.UsersAPI(requests.session()) as session:

            res = session.register(email, password)
            print(res)
        if type(res) == str:
            return 0
        return 1

    @require_connection
    def create_post(self, text):
        from api_fecth import CreatePost, Post
        post = CreatePost(text)
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.create_post(post)
            if type(res) == Post:

                return 1, res
            else:
                return 0, res

    @require_connection
    def get_posts(self, email):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_posts_by_user(email)
            if type(res) == list:
                return res
            else:
                print(res)
                return []

    @require_connection
    def get_all_posts(self):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_all_posts()

        return res

    @require_connection
    def get_likes_by_post(self, post_id):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_likes_by_post(post_id)

        return res

    @require_connection
    def get_post_by_id(self, post_id):
        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_post_by_id(post_id)
            print(res)
        return res

    @require_connection
    def logout(self):
        with api_fecth.UsersAPI(requests.session()) as session:
            code_,res = session.logout()
            print(res)
        return code_

    @require_connection
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
        return json.loads(res[0])

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
        elif self.state == AppStates.LIKE_VIEW:
            page = LikesViewWin
        else:
            raise Exception("we run for some errors right now...")
        self.switch_page(page)

    @require_connection
    def get_likes_by_email(self, email):

        with api_fecth.PostsAPI(requests.session()) as session:
            res = session.get_likes_by_email(email)
        return res


def run_app():
    app = App()
    app.root.mainloop()

if __name__ == '__main__':
    app = App()
    print(app.login("email", "pass"))
