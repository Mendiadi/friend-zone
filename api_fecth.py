import dataclasses

import requests


class Model:

    def to_json(self):
        return self.__dict__


@dataclasses.dataclass
class CreatePost(Model):
    text: str


@dataclasses.dataclass
class Post(Model):
    post_id: int
    text: str
    user_email: str


@dataclasses.dataclass
class Like(Model):
    user_email: str
    post_id: int


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
        print(user)
        res = self._session.post(self.base_url + "/register", json=user.to_json())
        if res.ok:
            return User(**res.json())
        return res.text

    def login(self, email, password):
        user = User(email, password)
        print(user)
        res = self._session.post(self.base_url + "/login", json=user.to_json())
        return res.text, res.status_code

    def search(self, query):
        if query == "":
            query = " "
        print(query)
        res = self._session.get(self.base_url + f"/search/{query}")
        return [User(**user) for user in res.json()['users']]


class PostsAPI(API):
    def __init__(self, session):
        super().__init__(session)

    def create_post(self, post_data: CreatePost, user):
        res = self._session.post(self.base_url + f"/{user}/post", json=post_data.to_json())
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
        print(post)
        res = self._session.put(self.base_url + f"/post/edit/{post.post_id}", json=post.to_json())
        if res.ok:
            return Post(**res.json()['post'])
        return res.text

    def like_post(self, like: Like):
        res = self._session.post(self.base_url + f"/post/like/{like.post_id}", json=like.to_json())
        return res.text, res.status_code

    def get_likes_by_post(self, post_id):
        print(self.base_url + f"/post/like/{post_id}")
        res = self._session.get(self.base_url + f"/post/like/{post_id}")
        if not res.ok:
            return  res.text
        return res.json()['count']

    def dislike_post(self, like):
        res = self._session.delete(self.base_url + f"/post/like/{like.post_id}/{like.user_email}")
        return res.text, res.status_code


if __name__ == '__main__':
    with PostsAPI(requests.session()) as session:
        a = session.get_posts_by_user("adim")
        print(a)
        print(session.get_likes_by_post(132))
        print(session.dislike_post(Like("moshe12", 132)))
        print(session.get_likes_by_post(132))
