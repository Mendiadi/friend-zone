from .base import API
from friend_zone.api.models import (
        CreateUser,
        User

)

class UsersAPI(API):
    def __init__(self, session):
        super().__init__(session)

    def register(self, email, password):
        user = CreateUser(email, password)

        res = self._session.post(self.base_url + "/register", json=user.to_json())
        if res.ok:
            return User(**res.json())
        return res.text

    def login(self, email, password):
        user = CreateUser(email, password)
        res = self._session.post(self.base_url + "/login", json=user.to_json())
        return res.text, res.status_code

    def get_user_by_email(self, email):
        res = self._session.get(self.base_url + f"/user/{email}")
        return User(**res.json()) if res.ok else res.text

    def get_user_by_id(self, user_id):
        res = self._session.get(self.base_url + f"/user/{user_id}")
        return User(**res.json()) if res.ok else res.text

    def search(self, query):
        if query == "":
            query = " "

        res = self._session.get(self.base_url + f"/search/{query}")
        return [User(**user) for user in res.json()['users']]

    def follow_user(self, email):
        user = self.get_user_by_email(email)
        res = self._session.post(self.base_url + f"/user/follow/{user.user_id}", data='{}')
        return res.text if not res.ok else res.json()

    def logout(self):
        res = self._session.get(self.base_url + "/logout")
        return (0, res.text) if not res.ok else (1, res.text)

