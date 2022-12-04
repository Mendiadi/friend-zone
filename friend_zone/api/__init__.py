
from .models import *
from .endpoints import *



class Services:
    def __init__(self, session):
        self._users_api = UsersAPI(session)
        self._posts_api = PostsAPI(session)
        self._chat_api = ChatAPI(session)

    @property
    def chat_api(self):
        return self._chat_api

    @property
    def posts_api(self):
        return self._posts_api

    @property
    def users_api(self):
        return self._users_api