import socket
import requests




class API:
    def __init__(self, session: requests.Session):
        from friend_zone.scripts import app_config
        self._session = session
        url = f"{app_config.net_host}:{app_config.port}"
        self.base_url = f"http://{url}/api"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def test_connection(self):
        print("test connection begin..", end=" -> ")
        return_code: int
        try:
            print("try to connect...", end=" -> ")
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 5000))
        except ConnectionError:
            print("connection failed...", end=" -> ")
            return_code = 0
        else:
            print("connection success... -> close connection testing", end=" -> ")
            conn.close()
            return_code = 1
        finally:
            print(f"done test connection with code {return_code}")
            return return_code

