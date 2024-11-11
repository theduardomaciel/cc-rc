import math
import pygame

from utils.settings import Settings

settings = Settings()

window_width = settings.width
window_height = settings.height


class Player:
    def __init__(self, id, x, y, width, height, color):
        self.id = id
        self.name = settings.name

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.current_color = color
        self.rect = (x, y, width, height)

        # Lives
        self.lives = 10

        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_movement_velocity = 4
        self.acceleration = 0.5  # Aceleração reduzida para movimento mais gradual
        self.friction = 0.02  # Fricção menor para deslizar mais
        self.bounce_factor = 0.5  # Fator de rebote (suavidade)

        # Dash
        self.is_dashing = False
        self.dash_speed = 7.5  # Velocidade durante o dash
        self.dash_cooldown = 500  # Duração do dash em milissegundos
        self.last_dash_time = 0  # Tempo do último dash

        # Direction
        self.last_direction = [0, 0]

        self.transparency = 255  # Transparência inicial (completa)
        self.invulnerability_duration = 1500  # Duração da invulnerabilidade (em ms)
        self.invulnerability_start_time = 0  # Tempo em que a invulnerabilidade começou

        # Variável para controlar a pulsação da transparência
        self.pulse_speed = 5

        # Direções bloqueadas temporariamente após a colisão
        self.blocked_directions = [[False, False], [False, False]]

        self.ping = 0

    def reset(self):
        self.lives = 10
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_dashing = False
        self.last_dash_time

    def is_out_of_bounds_x(self, pos):
        if pos < 0:
            return -1
        elif pos > window_width - self.width:
            return 1

    def is_out_of_bounds_y(self, pos):
        if pos < 0:
            return -1
        elif pos > window_height - self.height:
            return 1

        return False

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

        push_factor = 5 if attacker.is_dashing else 1  # Aumenta o empurrão se estiver no dash

        # Calcula o vetor de empurrão na direção do atacante
        dx = self.x - attacker.x
        dy = self.y - attacker.y
        distance = math.hypot(dx, dy)

        # Evita divisões por zero para direções exatas
        if distance != 0:
            dx /= distance
            dy /= distance

        # Aplica uma velocidade com base na direção do empurrão
        self.velocity_x += dx * push_factor * 5  # Ajusta a força do empurrão aqui
        self.velocity_y += dy * push_factor * 5

        # Executa a função de shake
        on_shake(10)


    def on_death(self):
        # Game over
        print("Game over!")
        # pygame.quit()

    def on_damage(self, damage: int, interactions: dict):
        self.lives -= damage
        interactions["on_damage"]()

        if self.lives <= 0:
            self.on_death()
            interactions["on_shake"](15)
        else:
            interactions["on_shake"](50)

    def move(self, interactions, players: list = None):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Verifica se o jogador está no cooldown após a colisão
        if (
            current_time - self.invulnerability_start_time
            < self.invulnerability_duration
        ):
            # Durante o cooldown, a transparência oscila (animação de pulsação)
            elapsed_time = current_time - self.invulnerability_start_time
            self.transparency = 128 + int(
                127 * (math.sin(elapsed_time / self.pulse_speed))
            )
        else:
            # Quando o cooldown termina, a transparência volta ao normal
            self.transparency = 255

        # Verifica se o dash pode ser ativado (respeitando o cooldown)
        if (
            keys[pygame.K_2]
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
            self.transparency = 128
            # Não é necessário retornar a transparência para 255 pois o bloco de código acima já faz isso

            # Verificar se o dash acabou
            if current_time - self.last_dash_time >= self.dash_cooldown:
                self.is_dashing = False

        delta = [0, 0]

        # Movimento com aceleração, se a direção não estiver bloqueada
        if not self.blocked_directions[0][0] and keys[pygame.K_LEFT]:
            delta[0] = -1
            self.velocity_x -= (
                self.velocity_x > -self.max_movement_velocity and self.acceleration or 0
            )

        if not self.blocked_directions[0][1] and keys[pygame.K_RIGHT]:
            delta[0] = 1
            self.velocity_x += (
                self.velocity_x < self.max_movement_velocity and self.acceleration or 0
            )

        if not self.blocked_directions[1][0] and keys[pygame.K_UP]:
            delta[1] = -1
            self.velocity_y -= (
                self.velocity_y > -self.max_movement_velocity and self.acceleration or 0
            )

        if not self.blocked_directions[1][1] and keys[pygame.K_DOWN]:
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
        direction_x = self.is_out_of_bounds_x(self.x + self.velocity_x)
        if direction_x:
            if not self.is_dashing:
                self.on_damage(1, interactions)

                # Bloqueia o movimento na direção X temporariamente
                self.blocked_directions[0][direction_x > 0 and 1 or 0] = True

                # Inicia a invulnerabilidade
                self.invulnerability_start_time = current_time

            # Prevenir que o jogador saia da tela (empurrado por outros jogadores)
            if direction_x < 0:
                self.x = 0
            elif direction_x > window_width - self.width:
                self.x = window_width - self.width

            # Rebote na direção oposta
            self.velocity_x = -self.velocity_x * self.bounce_factor

        direction_y = self.is_out_of_bounds_y(self.y + self.velocity_y)
        if direction_y:
            if not self.is_dashing:
                self.on_damage(1, interactions)

                # Bloqueia o movimento na direção X temporariamente
                self.blocked_directions[1][direction_y > 0 and 1 or 0] = True

                # Inicia a invulnerabilidade
                self.invulnerability_start_time = current_time

                # Rebote na direção oposta
                self.velocity_x = -self.velocity_x * self.bounce_factor

            # Prevenir que o jogador saia da tela (empurrado por outros jogadores)
            if direction_y < 0:
                self.y = 0
            elif direction_y > window_height - self.height:
                self.y = window_height - self.height

            self.velocity_y = -self.velocity_y * self.bounce_factor

        # Desbloquear movimento após o rebote e tempo de bloqueio
        if (
            current_time - self.invulnerability_start_time > 300
        ):  # Exemplo de tempo de bloqueio
            self.blocked_directions = [[False, False], [False, False]]

        # Atualizar posição
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.update()

        # Verificar colisões com outros jogadores
        if players is not None:
            for other_player in players:
                if self.check_collision(other_player):
                    if self.x < other_player.x:
                        self.x -= 0.1

                    if self.x > other_player.x:
                        self.x += 0.1

                    if self.y < other_player.y:
                        self.y -= 0.1

                    if self.y > other_player.y:
                        self.y += 0.1

                    self.velocity_x = -self.velocity_x * self.bounce_factor
                    self.velocity_y = -self.velocity_y * self.bounce_factor

                    # Notifica o jogador que foi atingido
                    self.notify_collision(other_player, interactions["on_shake"])

                    interactions["on_shake"](10)


        # print("Velocidade X: ", self.velocity_x)
        # print("Velocidade Y: ", self.velocity_y)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win, font: pygame.font.Font, is_player: bool = False):
        # Aplicar o valor de transparência à cor do jogador
        color_with_transparency = (*self.current_color[:3], self.transparency)

        # Cria uma superfície temporária com transparência
        player_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            player_surface, color_with_transparency, (0, 0, self.width, self.height)
        )
        win.blit(player_surface, (self.x, self.y))

        lives_text = font.render(f"{self.lives} HP", True, (255, 255, 255))
        win.blit(
            lives_text,
            (self.x + self.width / 2 - lives_text.get_width() / 2, self.y - 30),
        )

        if is_player:
            # Exibir o cooldown acima do jogador
            current_time = pygame.time.get_ticks()
            time_since_dash = current_time - self.last_dash_time
            if time_since_dash < self.dash_cooldown:
                # Calcular tempo restante
                remaining_time = (self.dash_cooldown - time_since_dash) / 1000

                # Desenhar texto acima do jogador
                cooldown_text = font.render(
                    f"{remaining_time:.1f}s", True, (255, 255, 255)
                )
                win.blit(
                    cooldown_text,
                    (
                        self.x + self.width / 2 - cooldown_text.get_width() / 2,
                        self.y + 40,
                    ),
                )
        else:
            # Desenhar nome do jogador
            name_text = font.render(self.name, True, (255, 255, 255))

            win.blit(
                name_text,
                (
                    self.x + self.width / 2 - name_text.get_width() / 2,
                    self.y + 40,
                ),
            )
