import dataclasses

import requests


class Model:

    def to_json(self):
        return self.__dict__


@dataclasses.dataclass
class Post(Model):
    post_id: int
    text: str
    user_email: str


@dataclasses.dataclass
class User(Model):
    email: str
    password: str


class API:
    def __init__(self, session: requests.Session):
        self._session = session
        self.base_url = "http://127.0.0.1:5000"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


class UsersAPI(API):
    def __init__(self, session):
        super().__init__(session)

    def register(self, email, password):
        user = User(email, password)
        res = self._session.post(self.base_url + "/register", json=user.to_json())
        if res.ok:
            return User(**res.json())
        return res.text

    def login(self, email, password):
        user = User(email, password)
        res = self._session.post(self.base_url + "/login", json=user.to_json())
        return res.text, res.status_code

    def create_post(self, post_data: Post, user):
        res = self._session.post(self.base_url + f"/{user}/post", json=post_data.to_json())
        print(res.text)

    def get_posts_by_user(self, user):
        res = self._session.get(self.base_url + f"/{user}/post")
        print(res.text)


if __name__ == '__main__':
    with UsersAPI(requests.Session()) as s:
        code = s.get_posts_by_user("adim333")

        print(code)
