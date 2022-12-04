import dataclasses

from .base import Model


@dataclasses.dataclass
class CreateLike(Model):
    post_id: int




@dataclasses.dataclass
class Like(Model):
    user_id: int
    post_id: int




@dataclasses.dataclass
class Chat(Model):
    chat_id: int
    members: list


@dataclasses.dataclass
class Message(Model):
    chat_id: int
    msg_id: int
    sender: str
    receiver: str
    time: str
    text: str