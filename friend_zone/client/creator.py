import tkinter as tk
from typing import Literal


from friend_zone.api.models import Message


def load_assets():
    img = tk.PhotoImage(file="assets/bg_login.png")
    return img

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

        can = tk.Button(root, text=email, bg="red", border=0, font="none 12 bold", command=lambda: func(email))
        return can

    @staticmethod
    def create_post_label(root, post, user_email, func_del=None, func_edit=None, like_count=None, func_like=None):

        class PostComponent:
            def __init__(self, can, can2, label, txt, like_label, like_btn, post, time_label):
                self.can = can
                self.can2 = can2
                self.label = label
                self.txt = txt
                self.like_label = like_label
                self.like_btn = like_btn
                self.post = post
                self.time_label = time_label

            def refresh(self, likes_count, app):
                self.txt.config(state="normal")
                self.txt.delete(0.0, tk.END)
                self.txt.insert(0.0, post.text)
                self.txt.config(state="disabled", width=len(post.text), height=can2.winfo_height() - 10)
                self.like_label.config(text=f"likes: {likes_count}")
                self.like_count = likes_count
                self.time_label.config(text=f"{self.post.time}")
                if self.post.post_id not in [p.post_id for p in app.get_likes_by_email(app.user.email)]:
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
        label = tk.Label(can2, text=user_email, font="none 20 bold", height=0,
                         width=len(user_email) + 1, bg=color_bg2)
        txt = tk.Text(can2, font="none 12", bg=color_bg, border=0,
                      width=len(post.text), height=can2.winfo_height() - 10)
        txt.insert(0.0, post.text, tk.END)
        txt.config(state="disabled")
        txt.place_configure(x=50, y=50)
        like_btn = tk.Button(can, text="like", bg=color_bg2,
                             command=lambda: func_like(post.post_id),
                             border=0, font="none 10 bold")
        like_btn.place_configure(x=468, y=178)
        time_label = tk.Label(can, text=f"{post.time}", width=len(post.time), bg=color_bg2,
                              font="none 7")
        time_label.place_configure(x=1, y=1)
        like_count = tk.Label(can, text=f"likes: {like_count}",
                              font="none 8", bg=color_bg2, width=len(f"likes: {like_count}") + 1)

        like_count.place_configure(x=1, y=180)

        if func_del:
            btn = tk.Button(can, text="X", command=lambda: func_del(post.post_id),
                            font="none 12 bold", bg=color_bg2,
                            border=0
                            , activebackground="blue", highlightbackground="blue",
                            highlightcolor="blue", fg="red")
            btn.place_configure(x=480, y=5)
        if func_edit:
            btn = tk.Button(can, text="E", command=lambda: func_edit(post),
                            font="none 12 bold", bg=color_bg2, border=0
                            , activebackground="blue", highlightbackground="blue",
                            highlightcolor="blue")
            btn.place_configure(x=480, y=40)
        label.place_configure(x=0, y=0)
        can2.place_configure(x=10, y=10)
        can.pack_configure(padx=250, pady=50)
        label_post_created = PostComponent(can, can2, label, txt, like_count,
                                           like_btn, post, time_label)

        return label_post_created

    @staticmethod
    def create_message_label(root, message: Message,
                             side: Literal['e', 'w'],
                             ):

        time = message.time[16:25:]

        base = tk.Canvas(root,
                         width=200 if side == "e" else 100,
                         bg="cyan" if side == "w" else "deepskyblue")
        time_label = tk.Label(base, width=len(time),
                              text=time, font="none 10 bold")
        label = tk.Text(base, height=5,
                        width=len(message.text),
                        bg="cyan", border=0)
        label.insert(0.0, message.text)
        label.config(state="disabled")
        base.config(height=60)
        label.place_configure(x=10, y=20)
        time_label.place_configure(x=0, y=0)

        label.config(bg="cyan" if side == "w" else "deepskyblue")
        time_label.config(bg="cyan" if side == "w" else "deepskyblue")
        base.pack_configure(anchor=side, fill=tk.BOTH,
                            padx=0 if side == "w" else 350,
                            )

        return base

    @staticmethod
    def create_entry(root, text_var, hide=False):

        hide = None if not hide else "*"

        return tk.Entry(root, textvariable=text_var, font="none 20", bg="light blue", border=1, show=hide)

    @staticmethod
    def create_button(root, text, func, state, size=None, font="none 10 bold"):
        btn = tk.Button(root, text=text, command=func, state=state,
                        highlightbackground="blue",
                        bg="deepskyblue3", border=0, font=font, cursor="hand2")
        if size:
            btn.config(height=size[0], width=size[1])
        return btn
