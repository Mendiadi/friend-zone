import dataclasses
import os

from friend_zone.client.utils import parse_yaml

PATH_CONFIGURE = "app_config.yaml"




@dataclasses.dataclass
class AppConfigure:
    db_host: str
    user: str
    password: str
    database: str
    port: int
    net_host: str
    name: str

    @staticmethod
    def load():
        conf = parse_yaml(PATH_CONFIGURE)
        if not conf:
            return None
        db = conf['db']
        net = conf['net']
        return AppConfigure(db['host'], db['user'], db['password'],
                            db['database'], net['port'], net['host'], net['name'])


app_config = AppConfigure.load()

if __name__ == '__main__':
    print(AppConfigure.load())
