import pygame
from classes.player import Player

pygame.init()


class Match:
    def __init__(self, id):
        self.id = id
        self.players = list()
        self.state = "waiting"
        self.max_players = 4
        self.connected_players = 0

        self.intermission_duration = 5 * 1000  # 10 segundos em milissegundos
        self.last_intermission_time = 0

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player):
        self.players.remove(player)

    def start(self):
        self.state = "running"

    def end(self):
        self.state = "ended"

    def schedule_intermission(self):
        self.state = "intermission"
        self.last_intermission_time = pygame.time.get_ticks()

    def check_intermission_timer(self):
        """Check if the intermission time has passed and start the match if it has."""
        current_time = pygame.time.get_ticks()
        # print("Tempo atual: ", current_time)
        # print("Tempo da última intermissão: ", self.last_intermission_time)
        print("Diferença: ", current_time - self.last_intermission_time)
        if (
            self.state == "intermission"
            and (current_time - self.last_intermission_time)
            >= self.intermission_duration
        ):
            print("Intervalo encerrado! Iniciando partida...")
            self.last_intermission_time = 0
            self.start()  # Start the match
