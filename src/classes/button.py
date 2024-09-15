import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        bg_color,
        font,
        text_color,
        border_radius=0,
        action=None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.bg_color = bg_color

        self.font = font
        self.text = text
        self.text_color = text_color

        self.border_width = 0
        self.border_color = (0, 0, 0)
        self.border_radius = border_radius

        self.action = action

    def draw(self, win):
        button_surface = pygame.Surface((self.width, self.height))

        # print("Cor: ", self.bg_color)

        # Desenha o botão
        # button_surface.fill(self.bg_color)
        pygame.draw.rect(
            button_surface,
            self.bg_color,
            (0, 0, self.width, self.height),
            self.border_width,
            border_radius=self.border_radius,
        )

        # Adiciona o texto
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        button_surface.blit(text_surface, text_rect)

        win.blit(button_surface, (self.x, self.y))

        return button_surface

    def click(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        return False

    def change_text(self, text):
        self.text = text

    def change_bg_color(self, color):
        self.bg_color = color

    def change_text_color(self, color):
        self.text_color = color

    def change_border(self, color, width):
        self.border_color = color
        self.border_width = width

    def change_action(self, action):
        self.action = action

    def execute(self, args):
        if self.action is not None:
            self.action(args)
