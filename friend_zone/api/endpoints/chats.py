from .base import API
from friend_zone.api.models import (
        Chat,
        Message
)


class ChatAPI(API):

    def __init__(self, session):
        super().__init__(session)

    def send_message(self, msg):
        res = self._session.post(self.base_url + "/chat/message", json=msg.to_json())
        return res.text

    def get_chat(self, chat_id):
        res = self._session.get(self.base_url + f"/chat/{chat_id}")
        return Chat(**res.json()) if res.ok else None

    def get_messages_by_chat(self, chat_id):
        res = self._session.get(self.base_url + f"/chat/message/{chat_id}")
        if res.ok:
            msgs = []
            for msg in res.json()['messages']:
                msgs.append(Message(**msg))
            return msgs
        return []

    def create_chat(self, chat: Chat):
        res = self._session.post(self.base_url + "/chat", json=chat.to_json())
        return Chat(**res.json()['chat']) if res.ok else res.text
