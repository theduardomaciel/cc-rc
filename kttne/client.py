import pygame
from network import Network
from classes.player import Player

from utils.settings import Settings
settings = Settings()

width = settings.width
height = settings.height

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(window, player):
    window.fill((255, 255, 255))

    player.draw(window)
    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    player = Player(100, 50, 100, 100, (255, 0, 0))

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()

        redraw_window(window, player)

main()
