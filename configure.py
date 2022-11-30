import dataclasses
import json

PATH_CONFIGURE = "config_app.json"

def load_json(path):
    try:
        with open(PATH_CONFIGURE,"r") as f:
            j = json.load(f)
            return j
    except(FileNotFoundError):
        return None

@dataclasses.dataclass
class AppConfigure:
    db_host: str
    user: str
    password: str
    database:str
    port:int
    net_host: str
    name:str

    @staticmethod
    def load():
        conf = load_json(PATH_CONFIGURE)
        if not conf:
            return None
        db = conf['db']
        net = conf['net']
        return AppConfigure(db['host'],db['user'],db['password'],
                            db['database'],net['port'],net['host'],net['name'])

if __name__ == '__main__':
    print(AppConfigure.load())