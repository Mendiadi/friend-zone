import tkinter as tk


from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait
from .post_view import PostViewWin



class ExploreWin(PostViewWin):

    def __init__(self, win, geometry, app):
        super(ExploreWin, self).__init__(win, geometry, app)
        self.post_data = tk.StringVar()
        self.add_post_entry = None
        self.post_btn = None

    @loading_if_wait
    def refresh_feed(self):
        self.fetch_all_posts(from_all=True)

    def move_to_home_page(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    @loading_if_wait
    def load(self):
        self.win.config(bg="cyan")
        ComponentCreator.create_text_label(self.win, "Your Feed").pack(pady=5)
        ComponentCreator.create_button(self.win, "HOME", self.move_to_home_page,
                                       "normal", size=(2, 10)).pack(pady=5)
        ComponentCreator.create_button(self.win, "refresh", self.refresh_feed,
                                       "normal", size=(2, 10)).pack(pady=5)
        self.add_post_entry = ComponentCreator.create_entry(self.win, self.post_data)
        self.add_post_entry.pack(pady=5)
        ComponentCreator.create_button(self.win,
                                       text="POST", func=self.post_onclick,
                                       state="normal", font="none 15").pack(pady=10)
        super().load()

        self.fetch_all_posts(from_all=True)

    @loading_if_wait
    def post_onclick(self):
        data = self.post_data.get()
        self.add_post_entry.delete(0, tk.END)
        if not data:
            return
        code, post = self.app.create_post(data)
        print(f"post -> {post}")
        if not code:
            return
        self.fetch_all_posts(from_all=True, shuffled=False, show_current_user=True)
        self.update_win()

