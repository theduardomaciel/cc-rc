import pygame
from network import Network
from classes.player import Player

from utils.settings import Settings

settings = Settings()

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(window, player: Player, player2: Player):
    window.fill((255, 255, 255))

    player.draw(window)
    player2.draw(window)

    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    player = n.get_player()

    while run:
        clock.tick(60)

        player2 = n.send(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        redraw_window(window, player, player2)


main()
