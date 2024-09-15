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


""" def blit_rotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    pygame.draw.rect(
        surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2
    )
 """


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
