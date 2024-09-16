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

        # Lives
        self.lives = 10

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_movement_velocity = 5
        self.acceleration = 0.5  # Aceleração reduzida para movimento mais gradual
        self.friction = 0.02  # Fricção menor para deslizar mais
        self.bounce_factor = 0.5  # Fator de rebote (suavidade)

        # Dash
        self.is_dashing = False
        self.dash_speed = 8.5  # Velocidade durante o dash
        self.dash_cooldown = 500  # Duração do dash em milissegundos
        self.last_dash_time = 0  # Tempo do último dash

        # Direction
        self.last_direction = [0, 0]

    def draw(self, win, font: pygame.font.Font = None):
        pygame.draw.rect(win, self.color, self.rect)

        if font is not None:
            lives_text = font.render(f"{self.lives} vida{self.lives != 1 and "s" or ""}", True, (255, 255, 255))
            win.blit(lives_text, (self.x + self.width/2 - lives_text.get_width()/2, self.y - 30))

            # Exibir o cooldown acima do jogador
            current_time = pygame.time.get_ticks()
            time_since_dash = current_time - self.last_dash_time
            if time_since_dash < self.dash_cooldown:
                # Calcular tempo restante
                remaining_time = (self.dash_cooldown - time_since_dash) / 1000

                # Desenhar texto acima do jogador
                cooldown_text = font.render(f"{remaining_time:.1f}s", True, (255, 255, 255))
                win.blit(cooldown_text, (self.x + self.width/2 - cooldown_text.get_width()/2, self.y + 40))

    def is_out_of_bounds_x(self, pos):
        return pos < 0 or pos > window_width - self.width

    def is_out_of_bounds_y(self, pos):
        return pos < 0 or pos > window_height - self.height

    def check_collision(self, other_player):
        """Verifica se há colisão com outro jogador"""
        # Checa se os retângulos se sobrepõem (colisão)
        return (
            self.x < other_player.x + other_player.width
            and self.x + self.width > other_player.x
            and self.y < other_player.y + other_player.height
            and self.y + self.height > other_player.y
        )

    def check_collision(self, other_player):
        """Verifica se há colisão com outro jogador"""
        # Checa se os retângulos se sobrepõem (colisão)
        return (
            self.x < other_player.x + other_player.width
            and self.x + self.width > other_player.x
            and self.y < other_player.y + other_player.height
            and self.y + self.height > other_player.y
        )

    def notify_collision(self, attacker, on_shake):
        """Notifica o jogador de que ele foi atingido, aplicando o impacto"""
        push_factor = 0.8  # Quanto do impulso é transferido
        self.velocity_x -= min(10, attacker.velocity_x * push_factor)
        self.velocity_y -= min(10, attacker.velocity_y * push_factor)

        on_shake(10)

    def on_death(self):
        # Game over
        print("Game over!")
        # pygame.quit()

    def move(self, interactions, players: list = None):
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

        # print("Velocidade X: ", self.velocity_x)
        # print("Velocidade Y: ", self.velocity_y)

        # Se o dash estiver ativo, continua a lógica de dash
        if self.is_dashing:
            # TODO: Animação de dash

            # Verificar se o dash acabou
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
            self.lives -= 1
            interactions["on_damage"]()

            if self.lives <= 0:
                self.on_death()
                interactions["on_shake"](15)
            else:
                interactions["on_shake"](50)

            # Prevenir que o jogador saia da tela (empurrado por outros jogadores)
            if self.x < 0:
                self.x = 0
            elif self.x > window_width - self.width:
                self.x = window_width - self.width

            self.velocity_x = -self.velocity_x * self.bounce_factor

        if self.is_out_of_bounds_y(self.y + self.velocity_y):
            self.lives -= 1
            interactions["on_damage"]()

            if self.lives <= 0:
                self.on_death()
                interactions["on_shake"](15)
            else:
                interactions["on_shake"](50)

            # Prevenir que o jogador saia da tela (empurrado por outros jogadores)
            if self.y < 0:
                self.y = 0
            elif self.y > window_height - self.height:
                self.y = window_height - self.height

            self.velocity_y = -self.velocity_y * self.bounce_factor

        # Atualizar posição
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.update()

        # Verificar colisões com outros jogadores
        if players is not None:
            for other_player in players:
                if self.check_collision(other_player):
                    self.velocity_x = -self.velocity_x * self.bounce_factor
                    self.velocity_y = -self.velocity_y * self.bounce_factor

                    if self.x < other_player.x:
                        self.x -= 1

                    if self.x > other_player.x:
                        self.x += 1

                    if self.y < other_player.y:
                        self.y -= 1

                    if self.y > other_player.y:
                        self.y += 1
                        
                    interactions["on_shake"](10)

                    # Notifica o jogador que foi atingido
                    self.notify_collision(other_player, interactions["on_shake"])

        # print("Velocidade X: ", self.velocity_x)
        # print("Velocidade Y: ", self.velocity_y)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
