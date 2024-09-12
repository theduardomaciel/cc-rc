import socket
from ..utils import Settings

# instantiate
settings = Settings()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = Settings.ip_address
        self.address = (self.server, settings.port)
        # self.id = self.connect()
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode("utf-8")
        except:
            pass
