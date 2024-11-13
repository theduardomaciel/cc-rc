import pygame
from typing import List
from random import randrange, randint

from classes.player import Player

pygame.init()

from utils.settings import Settings

settings = Settings()


class Match:
    def __init__(self, id):
        self.id = id
        self.players: List[Player] = list()
        self.state = "idle"  # idle, waiting, running, ended
        self.max_players = settings.max_players
        self.connected_players = 0

        self.intermission_duration = 5 * 1000  # 10 segundos em milissegundos
        self.last_intermission_time = 0

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.insert(player.id, player)
            return True
        return False

    def remove_player(self, player):
        self.players.remove(player)

    def start(self):
        print("Iniciando partida...")
        self.state = "running"

    def reset(self):
        self.state = "ended"
        self.schedule_intermission()

        new_players = list()
        for player in self.players:
            new_players.insert(player.id, self.generate_player(player.id))

        self.players = new_players

    def generate_player(self, id: int) -> Player:
        random_position = randrange(0, settings.width - 50), randrange(
            0, settings.height - 50
        )
        random_color = (
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
        )

        return Player(id, random_position[0], random_position[1], 50, 50, random_color)

    def schedule_intermission(self):
        self.last_intermission_time = pygame.time.get_ticks()

    def check_intermission_timer(self):
        """Check if the intermission time has passed."""
        current_time = pygame.time.get_ticks()
        # print("Tempo atual: ", current_time)
        # print("Tempo da última intermissão: ", self.last_intermission_time)
        # print("Diferença: ", current_time - self.last_intermission_time)
        if (current_time - self.last_intermission_time) >= self.intermission_duration:
            self.last_intermission_time = 0
            return True
        else:
            return False

    def check_game_over(self):
        """Check if the game is over and reset the match."""
        alive_players = [p for p in self.players if p.lives > 0]
        print("Jogadores vivos: ", len(alive_players))

        if len(alive_players) < settings.min_players:
            print("Fim de jogo! Aguardando próxima partida...")
            self.reset()
