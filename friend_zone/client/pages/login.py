import tkinter as tk


from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator,load_assets
from friend_zone.client.utils import loading_if_wait
from .base import BasicWin

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
        self.email_field.config(bg="deepskyblue2", borderwidth=0)
        self.password_field.config(bg="deepskyblue2", borderwidth=0)
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

    @loading_if_wait
    def login_btn_onclick(self):
        response = self.app.login(self.email_var.get(), self.password_var.get())
        if response == 1:
            self.win.after_cancel(self.validate_job)
            self.app.state = AppStates.HOME
            self.app.update_content()

        else:
            # show error
            self.plot_error(response)
            self.password_field.delete(0, tk.END)

    def validate_input(self):
        if self.app.state == AppStates.LOGIN:
            if len(self.email_var.get()) <= 3 or len(self.password_var.get()) < 3:
                self.login_btn.config(state="disabled")
            else:
                self.login_btn.config(state="normal")
            self.validate_job = self.win.after(1, self.validate_input)

    def load(self):
        self.bg.place(y=0, x=0)
        self.register_btn.place(x=290, y=800)

        self.email_field.place(y=460, x=335)

        self.password_field.place(y=552, x=335)
        self.login_btn.place(y=680, x=290)
        self.validate_input()
