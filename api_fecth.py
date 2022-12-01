import dataclasses
import socket
import time

import requests

import configure


class Model:

    def to_json(self):
        return self.__dict__


@dataclasses.dataclass
class CreatePost(Model):
    text: str


@dataclasses.dataclass
class CreateLike(Model):
    post_id: int


@dataclasses.dataclass
class Post(Model):
    post_id: int
    text: str
    user_id: str
    time: str


@dataclasses.dataclass
class Like(Model):
    user_id: int
    post_id: int


@dataclasses.dataclass
class CreateUser(Model):
    email: str
    password: str


@dataclasses.dataclass
class User(Model):
    user_id: int
    email: str
    password: str
    followers: list[int]
    following: list[int]


class API:
    def __init__(self, session: requests.Session):
        self._session = session
        url = f"{configure.app_config.net_host}:{configure.app_config.port}"
        self.base_url = f"http://{url}/api"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def test_connection(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 5000))
            return 1
        except ConnectionError:
            return 0


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
        res = self._session.post(self.base_url + f"/user/follow/{user.user_id}",data='{}')
        return res.text if not res.ok else res.json()

    def logout(self):
        res = self._session.get(self.base_url + "/logout")
        return (0, res.text) if not res.ok else (1, res.text)


class PostsAPI(API):
    def __init__(self, session):
        super().__init__(session)

    def create_post(self, post_data: CreatePost):
        res = self._session.post(self.base_url + f"/post", json=post_data.to_json())
        if res.ok:
            return Post(**res.json())
        else:
            return res.text

    def get_posts_by_user(self, user):
        res = self._session.get(self.base_url + f"/{user}/post")
        if res.ok:
            return [Post(**post) for post in res.json()['posts']]
        return res.text

    def delete_post(self, post_id):
        res = self._session.delete(self.base_url + f"/post/delete/{post_id}")
        return res.text, res.status_code

    def get_all_posts(self):
        res = self._session.get(self.base_url + f"/posts")
        if res.ok:
            return [Post(**p) for p in res.json()['posts']]
        return res.text

    def edit_post(self, post: Post):

        res = self._session.put(self.base_url + f"/post/edit/{post.post_id}", json=post.to_json())
        if res.ok:
            return Post(**res.json()['post'])
        return res.text

    def like_post(self, like: CreateLike):
        res = self._session.post(self.base_url + f"/post/like/{like.post_id}", json=like.to_json())
        return res.text, res.status_code

    def get_likes_by_post(self, post_id):

        res = self._session.get(self.base_url + f"/post/like/{post_id}")
        if not res.ok:
            return res.text
        return res.json()['count']

    def dislike_post(self, like):
        res = self._session.delete(self.base_url + f"/post/like/{like.post_id}/{like.user_email}")
        return res.text, res.status_code

    def get_post_by_id(self, post_id):

        res = self._session.get(self.base_url + f"/post/{post_id}")
        if not res.ok:
            return res.text
        return Post(**res.json()['post'])

    def get_likes_by_email(self, email):

        res = self._session.get(self.base_url + f"/like/{email}")
        if res.ok:
            return [Like(**like) for like in res.json()['likes']]
        return res.text if not res.ok else 1


class Services:
    def __init__(self, session):
        self._users_api = UsersAPI(session)
        self._posts_api = PostsAPI(session)

    @property
    def posts_api(self):
        return self._posts_api

    @property
    def users_api(self):
        return self._users_api


if __name__ == '__main__':
    d = ("taltal1","doron80","tamir445","gamer3")
    r = requests.session()
    papi = PostsAPI(r)
    uapi = UsersAPI(r)
    for d in d:
        uapi.register(d,"12345")
        uapi.login(d,"12345")

        for _ in range(3):
            papi.create_post(CreatePost(f"my name is {d}"))
        uapi.logout()

    uapi.__exit__(1,1,1)
    papi.__exit__(1,1,1)
    # s = requests.session()
    # with PostsAPI(s) as session:
    #     with UsersAPI(s) as se:
    #         se.login("adim333", "12345")
    #         print(se.get_user_by_email("adim333"))
    #         print(se.get_user_by_id(1000))
    #     time.sleep(5)
    #     print(session.like_post(CreateLike(1)))
    #     print(session.create_post(CreatePost("hkli")))
    # with PostsAPI(s) as session:
    #     with UsersAPI(s) as se:
    #         print(se.get_user_by_email("adim333"))
    #         print(se.get_user_by_id(1000))
    #     time.sleep(5)
    #     print(session.like_post(CreateLike(1)))
    #     print(session.create_post(CreatePost("hkli")))
    # with PostsAPI(s) as session:
    #     with UsersAPI(s) as se:
    #         print(se.get_user_by_email("adim333"))
    #         print(se.get_user_by_id(1000))
    #         se.logout()
    #     time.sleep(5)
    #     print(session.like_post(CreateLike(1)))
    #     print(session.create_post(CreatePost("hkli")))
