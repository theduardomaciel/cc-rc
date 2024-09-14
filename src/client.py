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


def redraw_window(window, font, player: Player, player2: Player):
    window.fill((255, 255, 255))

    if player is not None:
        player.draw(window, font)

    if player2 is not None:
        player2.draw(window, font)

    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    # Inicializa a fonte
    font = Font("comicsans", 24)

    player = n.get_player()

    while run:
        clock.tick(60)

        player2 = n.send(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if player is not None:
            player.move()

        redraw_window(window, font, player, player2)


main()
