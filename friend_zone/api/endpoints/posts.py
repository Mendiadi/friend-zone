from .base import API
from friend_zone.api.models import (
        CreatePost,
        Post,
        CreateLike,
        Like
)


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

