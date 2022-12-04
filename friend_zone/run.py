import os

from friend_zone.server.routes import app
from friend_zone.scripts.configure import app_config



if __name__ == '__main__':

    app.run(debug=True, host=app_config.net_host, port=app_config.port)