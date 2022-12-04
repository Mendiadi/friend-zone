import dataclasses


from .base import Model

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
