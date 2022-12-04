import tkinter as tk



from friend_zone.client.creator import ComponentCreator
from friend_zone.api.models.misc import Chat
from .scrolled import ScrolledWin


class ChatWin(ScrolledWin):
    def __init__(self, win, geometry, app, chat_room):
        super(ChatWin, self).__init__(win, geometry, app)

        self.chat_room = chat_room
        self.headline = ComponentCreator.create_text_label(self.win, "Chat Room", font_size=15)
        self.text_entry = ComponentCreator.create_entry(self.win, None)
        self.send_btn = ComponentCreator.create_button(self.win,
                                                       "Send", self.send_message_onclick, state="normal")
        self.messages = []

    @staticmethod
    def create_chat_window(app):
        root = tk.Tk()
        receiver = app.get_user_by_email(app.temp_user_profile)

        chat_room = app.create_chat(Chat(None, [app.user.user_id,
                                                          receiver.user_id]))
        chat_win = ChatWin(root, "500x500", app, chat_room)
        return chat_win

    def send_message_onclick(self):
        self.app.send_message(self.app.temp_user_profile,
                              self.text_entry.get(), self.chat_room.chat_id)
        self.load_messages()
        self.text_entry.delete(0, tk.END)

    def load_messages(self):
        for msg_label in self.messages:
            msg_label.destroy()
        self.messages.clear()
        msg_data = self.app.get_messages_by_chat(self.chat_room.chat_id)

        for i, msg in enumerate(msg_data):

            if msg.sender == self.app.user.email:
                l = ComponentCreator.create_message_label(self.second_frame,
                                                          message=msg, side="e")
            else:
                l = ComponentCreator.create_message_label(self.second_frame,
                                                          message=msg, side="w")
            self.messages.append(l)
        self.update_win()

    def load(self):
        self.win.config(bg="cyan")
        self.headline.pack()
        self.text_entry.pack()
        self.send_btn.pack()

        super().load()

        self.load_messages()