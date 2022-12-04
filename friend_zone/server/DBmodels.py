import flask_login

class user(flask_login.UserMixin):
    def __init__(self, user_id, email, password, followers, following):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.followers = followers
        self.following = following

    def get_id(self):
        return str(self.user_id)


class post:
    def __init__(self, post_id, text, user_id, time):
        self.post_id = post_id
        self.text = text
        self.user_id = user_id
        self.time = time


class likes:
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class chat:
    def __init__(self, chat_id, members):
        self.chat_id = chat_id
        self.members = members


class message:
    def __init__(self, msg_id, sender, receiver, time, text, chat_id):
        self.chat_id = chat_id
        self.msg_id = msg_id
        self.sender = sender
        self.receiver = receiver
        self.time = time
        self.text = text
