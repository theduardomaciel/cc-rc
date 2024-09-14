import pygame
from network import Network

from classes.font import Font
from classes.player import Player

from utils.settings import Settings

settings = Settings()

width = settings.width
height = settings.height

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(window, font, local_player: Player, players: list[Player]):
    window.fill((255, 255, 255))

    local_player.draw(window, font)

    if players is not None:
        for player in players:
            player.draw(window)

    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    # Inicializa a fonte
    font = Font("comicsans", 24)

    local_player = n.get_player()

    while run:
        clock.tick(60)

        # Enviar dados do jogador local e receber dados de outros jogadores
        players = n.send(local_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        local_player.move()

        redraw_window(window, font, local_player, players)


main()
