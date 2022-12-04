import dataclasses
import json
import yaml

PATH_CONFIGURE = "app_config.yaml"


def parse_yaml(path: str):
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_json(path):
    try:
        with open(PATH_CONFIGURE, "r") as f:
            j = json.load(f)
            return j
    except(FileNotFoundError):
        return None


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
