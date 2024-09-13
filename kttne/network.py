import socket
from utils.settings import Settings

settings = Settings()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = settings.ip_address
        self.port = settings.port
        self.address = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            # Conecta ao servidor
            self.client.connect(self.address)

            # Recebe a resposta do servidor
            return self.client.recv(2048).decode("utf-8")
        except:
            pass

    def send(self, data):
        try:
            # Envia dados ao servidor
            self.client.send(str.encode(data))

            # Recebe a resposta do servidor
            return self.client.recv(2048).decode("utf-8")
        except socket.error as e:
            print(e)
