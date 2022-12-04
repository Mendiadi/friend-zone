import tkinter as tk
import random


from .scrolled import ScrolledWin
from friend_zone.api.models import CreateLike
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait


class PostViewWin(ScrolledWin):
    def __init__(self, win, geometry, app):
        super(PostViewWin, self).__init__(win, geometry, app)
        self.posts = {}

    @loading_if_wait
    def like_post_onclick(self, post_id):
        like = CreateLike(post_id)
        self.app.post_like(like)

        self.fetch_post(post_id)

    def edit_post_onclick(self, post):

        pop_win = tk.Tk("edit")
        pop_win.geometry("300x300")
        e_entry = tk.Text(pop_win, height=5)
        e_entry.insert(0.0, post.text)

        def edit_click(post_):
            post_.text = e_entry.get(0.0, tk.END).strip()

            self.app.edit_post(post_)

            self.fetch_post(post.post_id)
            pop_win.destroy()

        e_entry.pack(pady=10)
        ComponentCreator.create_button(pop_win, "edit", lambda: edit_click(post), "normal").pack(pady=10)

    @loading_if_wait
    def delete_post_onclick(self, post_id):
        print(post_id, "delete onclick")
        if self.app.delete_post(post_id):
            label = self.posts.pop(post_id)
            label.can.destroy()

    def fetch_post(self, post_id):
        post = self.app.get_post_by_id(post_id)
        likes_count = self.app.get_likes_by_post(post_id)
        self.posts[post.post_id].post = post
        self.posts[post.post_id].refresh(likes_count, self.app)

    def fetch_liked_posts(self):

        for post in self.posts.values():
            post.can.destroy()
        posts = [like.post_id for like in self.app.get_likes_by_email(self.app.user.email)]
        for post in posts:

            p = self.app.get_post_by_id(post)
            user_email = self.app.get_user_by_id(p.user_id).email
            likes_count = self.app.get_likes_by_post(post)

            if user_email == self.app.user.email:
                conf_label = self.delete_post_onclick, self.edit_post_onclick, likes_count
            else:
                conf_label = (None, None, likes_count)
            self.posts[post] = ComponentCreator.create_post_label(
                self.second_frame, p,
                user_email, *conf_label,
                func_like=self.like_post_onclick
            )
            self.posts[post].refresh(likes_count, self.app)
            self.posts[post].can.pack()

        self.update_win()

    def fetch_all_posts(self, from_all=False,
                        max_for_fetch=10, shuffled=True, show_current_user=False):

        for post in self.posts.values():
            post.can.destroy()
        self.posts.clear()
        posts = self.app.get_posts(self.app.temp_user_profile) if not from_all else self.app.get_all_posts()
        if "error" in posts:
            return
        if shuffled:
            random.shuffle(posts)
        for i, post in enumerate(posts):
            if i >= max_for_fetch:
                break
            if not show_current_user:
                if post.user_id == self.app.user.user_id and from_all:
                    continue
            user_email = self.app.get_user_by_id(post.user_id).email
            likes_count = self.app.get_likes_by_post(post.post_id)

            if user_email == self.app.user.email:
                conf_label = self.delete_post_onclick, self.edit_post_onclick, likes_count
            else:
                conf_label = (None, None, likes_count)

            p = ComponentCreator.create_post_label(self.second_frame, post,
                                                   user_email,
                                                   *conf_label, func_like=self.like_post_onclick)
            self.posts[post.post_id] = p
            self.posts[post.post_id].refresh(likes_count, self.app)
            p.can.pack()

        self.update_win()

