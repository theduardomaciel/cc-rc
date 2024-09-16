import os

import pygame

pygame.font.init()

BASE_IMG_PATH = "data/images/"
BASE_FONT_PATH = "data/fonts/"


def load_font(path, font_size):
    return pygame.font.Font(BASE_FONT_PATH + path, font_size)


def load_image(path, transparent=True, opacity=1):
    img = pygame.image.load(BASE_IMG_PATH + path)
    if transparent:
        img = img.convert_alpha()

        # Aplica opacidade na imagem
        if opacity < 1:
            alpha_surface = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, int(255 * opacity)))
            img.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    else:
        img = img.convert()
        img.set_colorkey((0, 0, 0))  # Faz a cor preta ser transparente

    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images


def rotate_image(image, angle, center):
    """Função para rotacionar uma imagem em torno de seu centro."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect


class Animation:
    def __init__(self, images, img_dur=1, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
