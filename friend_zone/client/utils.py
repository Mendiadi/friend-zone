import functools
import os
import threading
import time
import requests
import yaml
import json
from tkinter import messagebox



from friend_zone.api.endpoints.base import API




def parse_yaml(path: str):
    try:

        with open(path, "r") as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        with open(os.path.join("friend_zone",path),"r") as stream:
            return yaml.safe_load(stream)


def load_json(path):
    try:
        with open(path, "r") as f:
            j = json.load(f)
            return j
    except(FileNotFoundError):
        return None

def require_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        with API(requests.session()) as session:
            res = session.test_connection()

        if res == 0:
            messagebox.showerror("no connection", "your connection is disabled")
        else:
            return func(*args, **kwargs)

        return {"error": "no connection"}

    return wrapper



def loading_if_wait(func):
    @functools.wraps(func)
    def wrapper(self, *args):
        print(args)
        t = threading.Thread(target=func, args=(self, *args), name="handle network")
        t.start()
        self.win.config(cursor="wait")

        def load():
            while t.is_alive():
                time.sleep(0.5)
            self.win.config(cursor="arrow")

        threading.Thread(target=load, name="load thread").start()

    return wrapper
