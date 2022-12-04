import tkinter as tk
import threading
import time

from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait
from .base import BasicWin


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

    def search_async(self):
        if self.search_query.get():
            self.fetch_results(self.app.search(self.search_query.get()))

    def search_thread(self):
        temp = None
        while self.run:
            time.sleep(0.1)

            if self.search_query.get() != temp:
                temp = self.search_query.get()
                self.search_async()

    def move_to_user_page(self, email):
        self.app.state = AppStates.PROFILE
        self.app.temp_user_profile = email
        self.app.update_content()

    def clear_results(self):
        for l in self.result_labels:
            l.destroy()

    def fetch_results(self, res):

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

    # ON CLICK METHODS *******************************************

    def my_profile_onclick(self):
        self.move_to_user_page(self.app.user.email)

    def explore_page_onclick(self):
        self.app.state = AppStates.EXPLORE
        self.app.update_content()

    @loading_if_wait
    def logout_onclick(self):
        if self.app.logout() == 1:
            self.app.state = AppStates.LOGIN
            self.app.update_content()

    def load(self):

        self.bg.place(x=0, y=0)
        profile_btn = ComponentCreator.create_button(self.win, "My Profile", self.my_profile_onclick, "normal",
                                                     size=(2, 10))
        profile_btn.config(border=0, font="none 12 bold", bg="deepskyblue3")
        profile_btn.place(x=650, y=70)
        self.explore_btn.place(x=300, y=70)
        logout_btn = ComponentCreator.create_button(self.win, "logout", self.logout_onclick, "normal", size=(2, 10))
        logout_btn.config(border=0, font="none 12 bold", bg="deepskyblue3")
        logout_btn.place(x=470, y=30)
        ComponentCreator.create_text_label(self.win, "Search for Users", "cyan", font_size=17).place(x=430, y=110)
        self.search_bar.place(x=370, y=150)
