import pygame
from network import Network
from utils.settings import Settings

from classes.Player import Player

settings = Settings()

print(settings.width, type(settings.width))

width = settings.width
height = settings.height

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, players):
    win.fill((255, 255, 255))

    for player in players:
        player.draw(win)

    pygame.display.update()


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    start_positions = Player.read_pos(n.getPos())
    colors = Player.read_color(n.getColors())
    players = []

    for i in range(len(start_positions)):
        Player(start_positions[i][0], start_positions[i][1], 100, 100, (255, 0, 0))

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for player in players:
            pos = Player.read_pos(n.send(player.make_pos((player.x, player.y))))
            player.x = pos[0]
            player.y = pos[1]
            player.update()

        player.move()
        redrawWindow(win, players)


main()
