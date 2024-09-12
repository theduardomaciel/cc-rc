import pygame
from network import Network

width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 5
        self.rect = (x, y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def isOutOfBoundsX(self, pos):
        return pos < 0 or pos > width - self.width

    def isOutOfBoundsY(self, pos):
        return pos < 0 or pos > height - self.height

    def move(self):
        keys = pygame.key.get_pressed()

        delta = list(0 for _ in range(2))

        if keys[pygame.K_LEFT]:
            delta[0] = -self.velocity
        if keys[pygame.K_RIGHT]:
            delta[0] = self.velocity
        if keys[pygame.K_UP]:
            delta[1] = -self.velocity
        if keys[pygame.K_DOWN]:
            delta[1] = self.velocity

        if self.isOutOfBoundsX(self.x + delta[0]):
            delta[0] = 0
        if self.isOutOfBoundsY(self.y + delta[1]):
            delta[1] = 0

        self.x += delta[0]
        self.y += delta[1]

        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(50, 50, 100, 100, (0, 255, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()

        redrawWindow(win, p)


main()
