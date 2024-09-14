import pygame

from utils.settings import Settings

settings = Settings()

window_width = settings.width
window_height = settings.height


class Player:
    def __init__(self, id, x, y, width, height, color):
        self.id = id

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_movement_velocity = 5
        self.acceleration = 0.5  # Aceleração reduzida para movimento mais gradual
        self.friction = 0.02  # Fricção menor para deslizar mais
        self.bounce_factor = 0.5  # Fator de rebote (suavidade)

        # Dash
        self.is_dashing = False
        self.dash_speed = 15  # Velocidade durante o dash
        self.dash_cooldown = 500  # Duração do dash em milissegundos
        self.last_dash_time = 0  # Tempo do último dash

        # Direction
        self.last_direction = [0, 0]

    # Inicializar a fonte para exibir o cooldown
    pygame.font.init()

    def draw(self, win, font: pygame.font.Font = None):
        pygame.draw.rect(win, self.color, self.rect)

        if font is not None:
            # Exibir o cooldown acima do jogador
            current_time = pygame.time.get_ticks()
            time_since_dash = current_time - self.last_dash_time
            if time_since_dash < self.dash_cooldown:
                # Calcular tempo restante
                remaining_time = (self.dash_cooldown - time_since_dash) / 1000

                # Desenhar texto acima do jogador
                cooldown_text = font.render(f"{remaining_time:.1f}s", True, (0, 0, 0))
                win.blit(cooldown_text, (self.x, self.y - 30))

    def is_out_of_bounds_x(self, pos):
        return pos < 0 or pos > window_width - self.width

    def is_out_of_bounds_y(self, pos):
        return pos < 0 or pos > window_height - self.height

    def move(self):
        keys = pygame.key.get_pressed()

        # Controle do tempo para dash
        current_time = pygame.time.get_ticks()

        # Verifica se o dash pode ser ativado (respeitando o cooldown)
        if (
            keys[pygame.K_SPACE]
            and not self.is_dashing
            and current_time - self.last_dash_time > self.dash_cooldown
        ):
            self.is_dashing = True
            self.last_dash_time = current_time

            print("DASH!")

            # Aplicar impulso na direção atual ou última direção de movimento
            self.velocity_x += self.last_direction[0] * self.dash_speed
            self.velocity_y += self.last_direction[1] * self.dash_speed

        print("Velocidade X: ", self.velocity_x)
        print("Velocidade Y: ", self.velocity_y)

        # Se o dash estiver ativo, continua a lógica de dash
        if self.is_dashing:
            if current_time - self.last_dash_time >= self.dash_cooldown:
                self.is_dashing = False

        delta = [0, 0]

        # Movimento com aceleração
        if keys[pygame.K_LEFT]:
            delta[0] = -1
            self.velocity_x -= (
                self.velocity_x > -self.max_movement_velocity and self.acceleration or 0
            )
        if keys[pygame.K_RIGHT]:
            delta[0] = 1
            self.velocity_x += (
                self.velocity_x < self.max_movement_velocity and self.acceleration or 0
            )
        if keys[pygame.K_UP]:
            delta[1] = -1
            self.velocity_y -= (
                self.velocity_y > -self.max_movement_velocity and self.acceleration or 0
            )
        if keys[pygame.K_DOWN]:
            delta[1] = 1
            self.velocity_y += (
                self.velocity_y < self.max_movement_velocity and self.acceleration or 0
            )

        if delta != [0, 0]:
            self.last_direction = delta

        """ # Limitar velocidade máxima
        if self.velocity_x > self.max_movement_velocity:
            self.velocity_x = self.max_movement_velocity
        elif self.velocity_x < -self.max_movement_velocity:
            self.velocity_x = -self.max_movement_velocity

        if self.velocity_y > self.max_movement_velocity:
            self.velocity_y = self.max_movement_velocity
        elif self.velocity_y < -self.max_movement_velocity:
            self.velocity_y = -self.max_movement_velocity """

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
