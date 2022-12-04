import tkinter as tk


from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait
from .base import BasicWin



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

    @loading_if_wait
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


