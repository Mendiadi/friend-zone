import tkinter as tk


from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait
from .post_view import PostViewWin
from .chat import ChatWin



class ProfileWin(PostViewWin):
    def __init__(self, win, geometry, app):
        super(ProfileWin, self).__init__(win, geometry, app)
        self.follow_btn = None
        self.is_my_profile = False

    # ONCLICK METHODS ********************************************
    @loading_if_wait
    def follow_user_onclick(self, user):

        r = self.app.follow_user(user.email)
        if "stop" != r['follow']:
            self.follow_btn.config(text="unfollow")
        else:
            self.follow_btn.config(text="follow")

    def message_room_onclick(self):
        ChatWin.create_chat_window(self.app).load()

    def go_back_onclick(self):
        self.app.state = AppStates.HOME
        self.app.update_content()

    def my_likes_onclick(self):
        self.app.state = AppStates.LIKE_VIEW
        self.app.update_content()

    def followers_view_onclick(self, flag, user):
        # flag can be 1 or 0

        if flag:
            h1 = "view followers"
            data = user.followers
        else:
            h1 = "view following"
            data = user.following

        pop_win = tk.Tk(h1)
        pop_win.geometry("300x300")

        def move_to_profile(email):
            pop_win.destroy()
            self.app.temp_user_profile = email
            self.app.update_content(ignore_same_page=True)

        for i, u in enumerate(data):
            if i == 0:
                continue
            u = self.app.get_user_by_id(u)
            print(u)
            ComponentCreator.create_user_label(pop_win, u.email, move_to_profile).pack(pady=5)

    @loading_if_wait
    def load(self):
        self.win.config(bg="cyan")
        if self.app.user.email != self.app.temp_user_profile:

            user = self.app.get_user_by_email(self.app.temp_user_profile)
        else:
            self.is_my_profile = True
            user = self.app.get_user_by_id(self.app.user.user_id)

        pad = 5
        ComponentCreator.create_text_label(self.win,
                                           f"{self.app.temp_user_profile} Profile").pack(pady=pad)

        ComponentCreator.create_button(self.win,
                                       f"FOLLOWERS {len(user.followers) - 1}",
                                       lambda: self.followers_view_onclick(1, user)
                                       , "normal").pack(pady=pad)
        ComponentCreator.create_button(self.win,
                                       f"FOLLOWING {len(user.following) - 1}",
                                       lambda: self.followers_view_onclick(0, user)
                                       , "normal").pack(pady=pad)
        if not self.is_my_profile:
            if self.app.user.user_id in user.followers:
                follow_btn_txt = "unfollow"
            else:
                follow_btn_txt = "follow"

            self.follow_btn = ComponentCreator.create_button(self.win, follow_btn_txt,
                                                             func=lambda: self.follow_user_onclick(user),
                                                             state="normal")
            self.follow_btn.pack(pady=pad)
            ComponentCreator.create_button(
                self.win, "send_message", self.message_room_onclick, "normal"
            ).pack(pady=pad)
        else:
            ComponentCreator.create_button(
                self.win, "my likes", self.my_likes_onclick, "normal"
            ).pack(pady=pad)

        ComponentCreator.create_button(
            self.win, "Back", self.go_back_onclick, "normal"
        ).pack(pady=pad)

        super().load()
        self.fetch_all_posts()

