import sys
import math
import random

import pygame

from network import Network
from utils.settings import Settings
from utils.assets import load_image, load_font, rotate_image
from classes.player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dash Muse")

        self.settings = Settings()

        self.width = self.settings.width
        self.height = self.settings.height

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))
        self.display_rotation = 0

        self.clock = pygame.time.Clock()

        self.assets = {
            "stars": load_image("stars.png"),
            "background": load_image("background.png"),
            "entity": load_image("entity_v2.png"),
        }

        # Escala os elementos do menu principal para o tamanho da tela
        self.assets["background"] = pygame.transform.scale(
            self.assets["background"], (self.width, self.height)
        )

        # Adiciona as decorações da tela
        """ main_deco(self)
        main_menu(self) """

        self.background_rotation = 0
        self.entity_rotation = 0
        self.screenshake = 0

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
            main_menu(self)

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

    # Rotaciona e desenha a entidade
    entity_center = (game.width // 2, game.height // 2 + 65)
    rotated_entity, entity_rect = rotate_image(
        game.assets["entity"], game.entity_rotation, entity_center
    )
    game.screen.blit(rotated_entity, entity_rect)

    # Desenha as bordas
    border_offset = 20
    border_radius = 10
    pygame.draw.rect(
        game.screen,
        (255, 255, 255),
        (
            border_offset,  # Coordenada x inicial
            border_offset,  # Coordenada y inicial
            game.width - 2 * border_offset,  # Largura ajustada
            game.height - 2 * border_offset,  # Altura ajustada
        ),
        2,
        border_radius,
    )


def main_menu(game: Game):
    # Adiciona o título do jogo
    font = load_font("ReemKufiInk-Bold.ttf", 72)
    text_surface = font.render("Dash Muse", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(game.width // 2, 150))
    game.screen.blit(text_surface, text_rect)


Game().run()
