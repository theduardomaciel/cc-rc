import sys
import math
import random

import pygame

from network import Network
from utils.settings import Settings
from utils.assets import load_image, load_font, rotate_image
from classes.player import Player
from classes.button import Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dash Muse")

        self.settings = Settings()

        self.width = self.settings.width
        self.height = self.settings.height

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.assets = {
            "stars": load_image("stars.png"),
            "background": load_image("background.png"),
            "entity": load_image("entity_v4.png"),
            "eye": load_image("eye.png"),
        }

        self.border_offset = 20

        # Escala os elementos do menu principal para o tamanho da tela
        self.assets["background"] = pygame.transform.scale(
            self.assets["background"], (self.width, self.height)
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

        self.state = "menu"  # pode ser: menu, game, spectate, endgame, elimination

        self.main_menu = MainMenu(self)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualiza as rotações
            self.background_rotation = (self.background_rotation + 0.1) % 360  # Lenta
            self.entity_rotation = (self.entity_rotation - 0.5) % 360  # Mais rápida

            # Chama o método que desenha os elementos
            main_deco(self)

            if self.state == "menu":
                self.main_menu.run(self)
            elif self.state == "spectate":
                wait_lobby_overlay(self)

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


def play_game(game: Game):
    print("Entrando no jogo...")
    game.state = "spectate"


def wait_lobby_overlay(game: Game):
    # Adiciona o texto "Aguardando partida..." no centro da tela
    font = load_font("ReemKufiInk-Regular.ttf", 28)
    text_surface = font.render(
        "Aguardando por mais 1 jogador...", True, (255, 255, 255)
    )

    # Adiciona o texto "Pressione ESC para sair" no canto inferior direito
    """ font = load_font("ReemKufiInk-Regular.ttf", 14)
    text_surface_esc = font.render("Pressione ESC para sair", True, (255, 255, 255)) """

    game.screen.blit(
        text_surface,
        (
            game.width // 2 - text_surface.get_width() // 2,
            game.height // 2 - text_surface.get_height() // 2,
        ),
    )

    """ game.screen.blit(
        text_surface_esc,
        (
            game.width - text_surface_esc.get_width() - game.border_offset - 10,
            game.height - text_surface_esc.get_height() - game.border_offset,
        ),
    )

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Saindo da partida...")
                game.state = "menu" """


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

        # Texto de quantidade de jogadores online
        font = load_font("ReemKufiInk-Regular.ttf", 14)
        text_surface = font.render("2 jogadores online", True, (255, 255, 255))

        game.screen.blit(
            text_surface,
            (
                game.width // 2 - text_surface.get_width() // 2,
                game.height - text_surface.get_height() - game.border_offset - 35,
            ),
        )


Game().run()
