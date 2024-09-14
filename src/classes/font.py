import pygame

# Inicializamos a fonte na classe Font
pygame.font.init()


class Font:
    def __init__(self, font_name: str, font_size: int):
        self.font = pygame.font.SysFont(font_name, font_size)

    def render(self, text: str, antialias: bool, color: tuple[int, int, int]):
        return self.font.render(text, antialias, color)
