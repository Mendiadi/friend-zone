import dataclasses


from .base import Model





@dataclasses.dataclass
class CreatePost(Model):
    text: str


@dataclasses.dataclass
class Post(Model):
    post_id: int
    text: str
    user_id: str
    time: str
