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
        self.match = None

    def get_player(self):
        return self.player

    def connect(self):
        try:
            # Conecta ao servidor
            self.client.connect(self.address)

            # Recebe a resposta do servidor (dados recebe seus dados jogador)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.client.close()

    def send(self, data) -> Match:
        # Envia dados (jogador local) ao servidor
        self.client.send(pickle.dumps(data))
        # print("Dados enviados:", data)

        try:
            # Recebe a resposta do servidor (partida)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
