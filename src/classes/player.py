import pygame

from utils.settings import Settings

settings = Settings()

window_width = settings.width
window_height = settings.height


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
        self.friction = 0.02  # Fricção menor para deslizar mais
        self.bounce_factor = 0.5  # Fator de rebote (suavidade)

        # Dash
        self.is_dashing = False
        self.dash_speed = 15  # Velocidade durante o dash
        self.dash_duration = 500  # Duração do dash em milissegundos
        self.last_dash_time = 0  # Tempo do último dash

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def is_out_of_bounds_x(self, pos):
        return pos < 0 or pos > window_width - self.width

    def is_out_of_bounds_y(self, pos):
        return pos < 0 or pos > window_height - self.height

    def move(self):
        keys = pygame.key.get_pressed()

        # Controle do tempo para dash
        current_time = pygame.time.get_ticks()

        # Verifica se o dash pode ser ativado
        if (
            keys[pygame.K_SPACE]
            and not self.is_dashing
            and current_time - self.last_dash_time > self.dash_duration
        ):
            self.is_dashing = True
            self.last_dash_time = current_time

        # Se estiver em dash, aumenta temporariamente a velocidade
        if self.is_dashing:
            dash_multiplier = self.dash_speed / self.max_velocity
            if current_time - self.last_dash_time >= self.dash_duration:
                self.is_dashing = False
            else:
                dash_multiplier = 3  # Multiplicador durante o dash
        else:
            dash_multiplier = 1  # Movimento normal

        delta = [0, 0]

        # Movimento com aceleração
        if keys[pygame.K_LEFT]:
            delta[0] = -1
            self.velocity_x -= self.acceleration * dash_multiplier
        if keys[pygame.K_RIGHT]:
            delta[0] = 1
            self.velocity_x += self.acceleration * dash_multiplier
        if keys[pygame.K_UP]:
            delta[1] = -1
            self.velocity_y -= self.acceleration * dash_multiplier
        if keys[pygame.K_DOWN]:
            delta[1] = 1
            self.velocity_y += self.acceleration * dash_multiplier

        # Limitar velocidade máxima
        if self.velocity_x > self.max_velocity * dash_multiplier:
            self.velocity_x = self.max_velocity * dash_multiplier
        elif self.velocity_x < -self.max_velocity * dash_multiplier:
            self.velocity_x = -self.max_velocity * dash_multiplier

        if self.velocity_y > self.max_velocity * dash_multiplier:
            self.velocity_y = self.max_velocity * dash_multiplier
        elif self.velocity_y < -self.max_velocity * dash_multiplier:
            self.velocity_y = -self.max_velocity * dash_multiplier

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
        if self.is_out_of_bounds_x(self.x + self.velocity_x):
            self.velocity_x = -self.velocity_x * self.bounce_factor

        if self.is_out_of_bounds_y(self.y + self.velocity_y):
            self.velocity_y = -self.velocity_y * self.bounce_factor

        # Atualizar posição
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.update()

        # print("Velocidade X: ", self.velocity_x)
        # print("Velocidade Y: ", self.velocity_y)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
