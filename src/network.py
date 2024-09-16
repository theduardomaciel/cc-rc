import socket
import pickle

from classes.match import Match
from utils.settings import Settings

settings = Settings()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = settings.ip_address
        self.port = settings.port
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            # Conecta ao servidor
            self.client.connect(self.address)

            # Recebe a resposta do servidor
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.client.close()

    def send(self, data) -> Match:
        try:
            # print("Dados enviados:", data)

            # Envia dados ao servidor (jogador local)
            self.client.send(pickle.dumps(data))

            # Recebe a resposta do servidor (outros jogadores)
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
