

from friend_zone.client.states import AppStates
from friend_zone.client.creator import ComponentCreator
from friend_zone.client.utils import loading_if_wait
from .post_view import PostViewWin


class LikesViewWin(PostViewWin):
    def __init__(self, win, geometry, app):
        super(LikesViewWin, self).__init__(win, geometry, app)

    # ONCLICK METHODS ********************************************

    def on_back_click(self):
        self.app.state = AppStates.PROFILE
        self.app.update_content()

    @loading_if_wait
    def load(self):
        super(LikesViewWin, self).load()
        ComponentCreator.create_button(self.second_frame, "back", self.on_back_click, "normal").pack()
        self.fetch_liked_posts()


