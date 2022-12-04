import json
import requests


from friend_zone.client.states import AppStates
from .utils import require_connection
from friend_zone.api import Services
from friend_zone.api.models import (
            Message,
            CreatePost,
            Post
)
from friend_zone.client.pages import (

            LikesViewWin,
            LoginWin,
            ProfileWin,
            ExploreWin,
            RegisterWin,
            HomeWin

)





class App:

    def __init__(self, win):
        self.state = AppStates.LOGIN
        self.win = win
        self.win.title("MY FRIEND ZONE")
        self.user = None
        self.MAXSIZE = "1000x1000"
        self.root = LoginWin(self.win, self.MAXSIZE, self)
        self.root.load()
        self.temp_user_profile = None
        session = requests.session()
        self._api_fetch = Services(session)

    # API CALLS METHODS *****************************************************

    @require_connection
    def get_messages_by_chat(self, chat_id) -> list[Message]:
        with self._api_fetch.chat_api as session:
            res = session.get_messages_by_chat(chat_id)
            print(res)
        return res

    @require_connection
    def get_chat(self, chat_id):
        with self._api_fetch.chat_api as session:
            res = session.get_chat(chat_id)
            print(res)
        return res

    @require_connection
    def create_chat(self, chat):
        with self._api_fetch.chat_api as session:
            res = session.create_chat(chat)
            print(res)
        return res

    @require_connection
    def send_message(self, receiver, text, chat_id):
        with self._api_fetch.chat_api as session:
            res = session.send_message(Message(chat_id, None, self.user.email,
                                                         receiver, None, text))
            print(res)

    @require_connection
    def search(self, query):
        with self._api_fetch.users_api as session:
            res = session.search(query)
            print(f"[LOG] {res}")
        return res

    @require_connection
    def follow_user(self, email):
        with self._api_fetch.users_api as session:
            res = session.follow_user(email)
            print(res)
        return res

    @require_connection
    def edit_post(self, post):
        with self._api_fetch.posts_api as session:
            res = session.edit_post(post)
            print(f"[LOG] {res}")

    @require_connection
    def delete_post(self, post):
        with self._api_fetch.posts_api as session:
            res = session.delete_post(post)
            print(f"[LOG] {res}")
            if res[1] == 200:
                return 1
            return 0

    @require_connection
    def post_like(self, like):
        with self._api_fetch.posts_api as session:
            res = session.like_post(like)
            print(f"[LOG] {res}")
        if res[1] == 201:
            return 1
        return 0

    @require_connection
    def register(self, email, password, re_password):
        if password != re_password:
            return 0
        with self._api_fetch.users_api as session:

            res = session.register(email, password)
            print(f"[LOG] {res}")
        if type(res) == str:
            return 0
        return 1

    @require_connection
    def create_post(self, text):

        post = CreatePost(text)
        with self._api_fetch.posts_api as session:
            res = session.create_post(post)
            print(f"[LOG] {res}")
            if type(res) == Post:

                return 1, res
            else:
                return 0, res

    @require_connection
    def get_posts(self, user):
        with self._api_fetch.posts_api as session:
            res = session.get_posts_by_user(user)
            print(f"[LOG] {res}")
            if type(res) == list:
                return res
            else:

                return []

    @require_connection
    def get_all_posts(self):
        with self._api_fetch.posts_api as session:
            res = session.get_all_posts()
            print(f"[LOG] {res}")
        if type(res) == list:
            return res
        else:
            return []

    @require_connection
    def get_likes_by_post(self, post_id):
        with self._api_fetch.posts_api as session:
            res = session.get_likes_by_post(post_id)
            print(f"[LOG] {res}")
        return res

    @require_connection
    def get_post_by_id(self, post_id):
        with self._api_fetch.posts_api as session:
            res = session.get_post_by_id(post_id)
            print(f"[LOG] {res}")
        return res

    @require_connection
    def get_likes_by_email(self, email):

        with self._api_fetch.posts_api as session:
            res = session.get_likes_by_email(email)
            print(f"[LOG] {res}")
        return res

    @require_connection
    def logout(self):
        with self._api_fetch.users_api as session:
            code_, res = session.logout()
            print(f"[LOG] {res}")
        return code_

    @require_connection
    def get_user_by_email(self, email):
        with self._api_fetch.users_api as session:
            user = session.get_user_by_id(email)
        return user

    @require_connection
    def get_user_by_id(self, user_id):
        with self._api_fetch.users_api as session:
            user = session.get_user_by_id(user_id)
        return user

    @require_connection
    def login(self, email, password):

        with self._api_fetch.users_api as session:
            res = session.login(email, password)
            print(f"[LOG] {res}")
        if res[1] == 200:
            self.user = self.get_user_by_email(email)
            return 1
        return json.loads(res[0])

    # UPDATE GUI METHODS *********************************************

    def switch_page(self, page: type, ignore_same_page=False):
        if type(self.root) != page or ignore_same_page:
            self.root.kill()

            self.root = page(self.win, self.MAXSIZE, self)
            self.root.load()

    def update_content(self, ignore_same_page=False):

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
            raise
        self.switch_page(page, ignore_same_page)

