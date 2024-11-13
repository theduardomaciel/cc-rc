import sys
import math
import random

import pygame

from network import Network
from utils.strings import format_seconds, format_players_amount
from utils.settings import Settings
from utils.assets import load_image, load_font, rotate_image
from classes.player import Player
from classes.button import Button
from classes.match import Match

settings = Settings()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dash Muse")

        self.settings = Settings()

        self.width = self.settings.width
        self.height = self.settings.height

        pygame_icon = pygame.image.load('data/images/icon.png')
        pygame.display.set_icon(pygame_icon)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.assets = {
            "stars": load_image("stars.png"),
            "background": load_image("background.png"),
            "entity": load_image("entity_v4.png"),
            "eye": load_image("eye.png"),
            "damage": load_image("damage.png"),
        }

        self.border_offset = 20

        # Escala os elementos do menu principal para o tamanho da tela
        self.assets["background"] = pygame.transform.scale(
            self.assets["background"], (self.width, self.height)
        )
        # Overlay vermelho para indicar dano que aparece suavemente
        self.assets["damage"] = pygame.transform.scale(
            self.assets["damage"], (self.width, self.height)
        )

        # Escala a entidade para metade do tamanho original
        entity_width = self.assets["entity"].get_width() // 2
        entity_height = self.assets["entity"].get_height() // 2
        self.assets["entity"] = pygame.transform.scale(
            self.assets["entity"], (entity_width, entity_height)
        )

        self.background_rotation = 0
        self.entity_rotation = 0
        self.screenshake = 0
        self.damage_alpha = 0

        self.main_menu = MainMenu(self)

        self.font = load_font("ReemKufiInk-Regular.ttf", 14)

        self.state = "menu"  # pode ser: menu, game, gameover

        def join_match(self):
            try:
                self.network = Network()
            except Exception as e:
                print(f"Erro ao conectar ao servidor: {e}")
                pygame.quit()

            return self.network.get_player()

        self.network = None
        self.player: Player = join_match(self)

        print(f"Jogador conectado: {self.player}")

    def render_players(self, players: list[Player]):
        if self.player.lives > 0:
            self.player.draw(self.screen, self.font, True)

            """ self.screen.blit(
                self.font.render(
                    "Ping: " + str(self.ping) + "ms",
                    True,
                    (255, 255, 255),
                ),
                (self.border_offset + 25, self.border_offset + 25),
            ) """

        if players is not None:
            for player in players:
                player.draw(self.screen, self.font)

    def on_shake(self, intensity: int):
        # print("Tremeu!")
        self.screenshake = intensity
 
    def on_damage(self):
        # print("Tomou dano!")
        self.damage_alpha = 255

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.screenshake = max(0, self.screenshake - 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Saindo do jogo...")
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            # Atualiza as rotações
            self.background_rotation = (self.background_rotation + 0.1) % 360  # Lenta
            self.entity_rotation = (self.entity_rotation - 0.5) % 360  # Mais rápida

            # Chama os métodos que desenha os elementos visuais
            main_deco(self)
            damage_overlay(self)

            if self.network and self.player.is_ready:
                match: Match = None

                start = pygame.time.get_ticks()

                try:
                    match = self.network.send(self.player)
                except Exception as e:
                    print(f"Erro ao obter a partida: {e}")
                    pygame.quit()

                end = pygame.time.get_ticks()

                # print(f"Tempo de resposta: {end - start}ms")
                self.player.ping = end - start

                # Administra o estado do jogo na rede
                if match:
                    ready_players_count = len([player for player in match.players if player.is_ready])

                    if match.state == "running":
                        # Jogo em andamento
                        self.state = "game"

                        # Remove o jogador local da lista de jogadores e filtrar os jogadores mortos
                        players = [
                            player
                            for player in match.players
                            if player.id != self.player.id and player.lives > 0
                        ]

                        # Atualiza a posição do jogador local (se ainda estiver vivo)
                        if self.player.lives > 0:
                            self.player.move(
                                {
                                    "on_shake": self.on_shake,
                                    "on_damage": self.on_damage,
                                },
                                players,
                            )
                        else:
                            spectate_overlay(self)

                        self.render_players(players)

                    elif match.state == "ended":
                        # Partida finalizada
                        game_over_overlay(self, match)

                        if self.state == "game":
                            print(
                                "Partida acabou, agora o o novo player é: ",
                                match.players[self.player.id],
                            )
                            self.player = match.players[self.player.id]
                            self.player.reset()
                            self.state = "gameover"

                    elif (
                        match.state == "waiting"
                        and ready_players_count >= settings.min_players
                    ):
                        intermission_timer_overlay(self, match)
                    else:
                        wait_lobby_overlay(self)
            else:
                self.main_menu.run(self)

            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2,
            )
            self.screen.blit(
                pygame.transform.scale(self.screen, self.screen.get_size()),
                screenshake_offset,
            )

            # Atualiza a tela
            pygame.display.update()


def main_deco(game: Game):
    # Preenche a tela com fundo preto
    game.screen.fill((0, 0, 0))

    # Desenha as estrelas atrás do background
    game.screen.blit(game.assets["stars"], (0, 0))  # atrás do background

    # Rotaciona e desenha o background
    bg_center = (game.width // 2, game.height // 2)
    rotated_bg, bg_rect = rotate_image(
        game.assets["background"], game.background_rotation, bg_center
    )
    game.screen.blit(rotated_bg, bg_rect)

    # Desenha as bordas
    border_radius = 10
    pygame.draw.rect(
        game.screen,
        (255, 255, 255),
        (
            game.border_offset,  # Coordenada x inicial
            game.border_offset,  # Coordenada y inicial
            game.width - 2 * game.border_offset,  # Largura ajustada
            game.height - 2 * game.border_offset,  # Altura ajustada
        ),
        2,
        border_radius,
    )


def damage_overlay(game: Game):
    if game.damage_alpha > 0:
        game.damage_alpha = max(0, game.damage_alpha - 5)
        game.assets["damage"].set_alpha(game.damage_alpha)
        game.screen.blit(game.assets["damage"], (0, 0))

        if game.player and game.player.lives <= 0:
            # Adiciona o texto de eliminação no centro da tela
            font = load_font("ReemKufiInk-Bold.ttf", 36)
            text_surface = font.render("ELIMINADO!", True, (255, 255, 255))
            text_surface.set_alpha(game.damage_alpha)

            game.screen.blit(
                text_surface,
                (
                    game.width // 2 - text_surface.get_width() // 2,
                    game.height // 2 - text_surface.get_height() // 2,
                ),
            )


def game_over_overlay(game: Game, match: Match):
    # Adiciona o texto "Jogador {nome} venceu!" no centro da tela
    font = load_font("ReemKufiInk-Bold.ttf", 36)

    text_surface = font.render(f"{game.player.name} venceu!", True, (255, 255, 255))

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2,
        ),
    )

    # Adiciona o texto "Aguardando partida..." no centro da tela
    font = load_font("ReemKufiInk-Regular.ttf", 18)

    remaining_time = match.intermission_duration - (
        pygame.time.get_ticks() - match.last_intermission_time
    )  # Tempo restante em milissegundos
    text_surface = font.render(
        f"Nova partida iniciando em {format_seconds(remaining_time)}...",
        True,
        (255, 255, 255),
    )

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2 + 50,
        ),
    )


def intermission_timer_overlay(game: Game, match: Match):
    # Adiciona o texto "Intermissão" no centro da tela
    font = load_font("ReemKufiInk-Bold.ttf", 36)
    text_surface = font.render("Aguardando jogadores...", True, (255, 255, 255))

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2,
        ),
    )

    # Adiciona o texto "Aguardando partida..." no centro da tela
    remaining_time = match.remaining_intermission_time  # Tempo restante em milissegundos

    font = load_font("ReemKufiInk-Regular.ttf", 18)
    text_surface = font.render(
        f"A partida iniciará em {format_seconds(remaining_time)}...",
        True,
        (255, 255, 255),
    )

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2 + 50,
        ),
    )

    # Adiciona o texto "Tempo restante: X segundos" no canto inferior direito
    font = load_font("ReemKufiInk-Regular.ttf", 14)
    text_surface = font.render(
        f"{match.connected_players}/{match.max_players} jogadores",
        True,
        (255, 255, 255),
    )

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height - text_surface.get_height() - game.border_offset - 25,
        ),
    )


def play_game(game: Game):
    game.player.is_ready = True


def wait_lobby_overlay(game: Game):
    # Adiciona o texto de espera no centro da tela
    font = load_font("ReemKufiInk-Regular.ttf", 28)
    text_surface = font.render(
        "Aguardando por mais 1 jogador...", True, (255, 255, 255)
    )

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2,
        ),
    )

    # Adiciona o texto de saída no canto central inferior
    font = load_font("ReemKufiInk-Regular.ttf", 14)
    text_surface = font.render("Pressione ESC para sair", True, (255, 255, 255))

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height - text_surface.get_height() - game.border_offset - 25,
        ),
    )

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.player.is_ready = False
                game.state = "menu"


def spectate_overlay(game: Game):
    # Carrega o ícone do olho e define o tamanho
    eye_icon = game.assets["eye"]
    icon_size = 32  # Defina o tamanho desejado para o ícone
    eye_icon = pygame.transform.scale(eye_icon, (icon_size, icon_size))

    # Fonte e texto para "Espectando"
    font = load_font("ReemKufiInk-Bold.ttf", 36)
    text_surface = font.render("Espectando", True, (255, 255, 255))

    # Defina o gap entre o ícone e o texto
    gap = 10

    # Posição inicial do ícone e do texto
    total_width = eye_icon.get_width() + gap + text_surface.get_width()
    icon_x = game.width // 2 - total_width // 2
    text_x = icon_x + eye_icon.get_width() + gap
    y = 50

    # Desenhar o ícone do olho
    game.screen.blit(eye_icon, (icon_x, y + 12))

    # Desenhar o texto "Espectando" ao lado do ícone
    game.screen.blit(text_surface, (text_x, y))

    # Adiciona o texto "Aguardando partida..." no centro da tela
    font = load_font("ReemKufiInk-Regular.ttf", 14)
    text_surface = font.render("Aguardando partida...", True, (255, 255, 255))

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height - game.border_offset - 65,
        ),
    )


class MainMenu:
    def __init__(self, game: Game):
        # Configurações do botão de jogar
        button_font = load_font("ReemKufiInk-Bold.ttf", 18)
        button_width = 165
        button_height = 50

        self.button_play = Button(
            game.width // 2 - button_width / 2,
            game.height - button_height - game.border_offset - 75,
            button_width,
            button_height,
            "Entrar no jogo",
            (255, 255, 255),
            button_font,
            (0, 0, 0),
            border_radius=4,
            action=play_game,
        )

    def run(self, game: Game):
        # Adiciona o título do jogo
        font = load_font("ReemKufiInk-Bold.ttf", 72)
        text_surface = font.render("Dash Muse", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(game.width // 2, 100))
        game.screen.blit(text_surface, text_rect)

        # Rotaciona e desenha a entidade
        entity_center = (game.width // 2, game.height // 2)
        rotated_entity, entity_rect = rotate_image(
            game.assets["entity"], game.entity_rotation, entity_center
        )
        game.screen.blit(rotated_entity, entity_rect)

        # Botão de jogar
        button_surface = self.button_play.draw(game.screen)
        button_rect = button_surface.get_rect(
            topleft=(self.button_play.x, self.button_play.y)
        )
        is_hover = button_rect.collidepoint(pygame.mouse.get_pos())

        if is_hover:
            # print("Mouse em cima do botão")
            self.button_play.change_bg_color((0, 0, 0))
            self.button_play.change_text_color((255, 255, 255))
        else:
            self.button_play.change_bg_color((255, 255, 255))
            self.button_play.change_text_color((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hover:
                    self.button_play.execute(game)

        # Obtemos a quantidade de jogadores online
        connected_players = 0

        if game.network:
            try:
                match = game.network.send(game.player)
                connected_players = match.connected_players
            except Exception as e:
                print(f"Erro ao obter a quantidade de jogadores: {e}")

        # Texto de quantidade de jogadores online
        font = load_font("ReemKufiInk-Regular.ttf", 14)
        text_surface = font.render(f"{format_players_amount(connected_players)} online", True, (255, 255, 255))

        game.screen.blit(
            text_surface,
            (
                game.width // 2 - text_surface.get_width() // 2,
                game.height - text_surface.get_height() - game.border_offset - 35,
            ),
        )


Game().run()
