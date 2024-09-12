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
        self.rect = (x, y, width, height)

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity = 5
        self.acceleration = 0.5  # Aceleração reduzida para movimento mais gradual
        self.friction = 0.35  # Fricção menor para deslizar mais
        self.bounce_factor = 0.5  # Fator de rebote (suavidade)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def isOutOfBoundsX(self, pos):
        return pos < 0 or pos > width - self.width

    def isOutOfBoundsY(self, pos):
        return pos < 0 or pos > height - self.height

    def move(self):
        keys = pygame.key.get_pressed()

        delta = [0, 0]

        # Movimento com aceleração
        if keys[pygame.K_LEFT]:
            delta[0] = -1
            self.velocity_x -= self.acceleration
        if keys[pygame.K_RIGHT]:
            delta[0] = 1
            self.velocity_x += self.acceleration
        if keys[pygame.K_UP]:
            delta[1] = -1
            self.velocity_y -= self.acceleration
        if keys[pygame.K_DOWN]:
            delta[1] = 1
            self.velocity_y += self.acceleration

        # Limitar velocidade máxima
        if self.velocity_x > self.max_velocity:
            self.velocity_x = self.max_velocity
        elif self.velocity_x < -self.max_velocity:
            self.velocity_x = -self.max_velocity

        if self.velocity_y > self.max_velocity:
            self.velocity_y = self.max_velocity
        elif self.velocity_y < -self.max_velocity:
            self.velocity_y = -self.max_velocity

        # Aplicar fricção se nenhuma tecla for pressionada
        if delta[0] == 0:
            if self.velocity_x > 0:
                self.velocity_x -= self.friction
            elif self.velocity_x < 0:
                self.velocity_x += self.friction

        if delta[1] == 0:
            if self.velocity_y > 0:
                self.velocity_y -= self.friction
            elif self.velocity_y < 0:
                self.velocity_y += self.friction

        # Parar se a velocidade estiver muito baixa
        if abs(self.velocity_x) < self.friction:
            self.velocity_x = 0
        if abs(self.velocity_y) < self.friction:
            self.velocity_y = 0

        # Checar e aplicar o rebote nas bordas
        if self.isOutOfBoundsX(self.x + self.velocity_x):
            self.velocity_x = -self.velocity_x * self.bounce_factor  # Rebote horizontal

        if self.isOutOfBoundsY(self.y + self.velocity_y):
            self.velocity_y = -self.velocity_y * self.bounce_factor  # Rebote vertical

        # Atualizar posição
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.rect = (self.x, self.y, self.width, self.height)

        print("Velocidade X: ", self.velocity_x)
        print("Velocidade Y: ", self.velocity_y)


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
