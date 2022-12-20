import pygame
import typing
from enum import Enum


def blit_text(screen, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = screen.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class CardType(Enum):
    Attack = pygame.Color('red')
    Defend = pygame.Color('blue')
    Weak = pygame.Color('green')
    Buff = pygame.Color('gray')


class Card(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, description: str, card_type: CardType, action):
        super(Card, self).__init__()
        self._width, self._height = 100, 200
        self._mini_image = pygame.transform.scale(sprite.image, (70, 70))
        self.rect = pygame.Rect((0, 0, self._width, self._height))

        self._name = name
        self._description = description
        self._card_type = card_type
        self._action = action

        self._picked = False

    @property
    def image(self):
        surface = pygame.Surface((100, 200))
        start_pos = (0, 0)

        pygame.draw.rect(surface, pygame.Color(253, 244, 227), (*start_pos, self._width, self._height))
        pygame.draw.rect(surface, self._card_type.value, (*start_pos, self._width, self._height), 5)

        title = pygame.font.Font(None, 18).render(self._name, True, pygame.Color('black'))
        place = title.get_rect(center=(start_pos[0] + 50, start_pos[1] + 20))
        surface.blit(title, place)

        surface.blit(self._mini_image, (15, 40))

        blit_text(surface, self._description, (7, 120), pygame.font.Font(None, 18))

        return surface

    @property
    def picked(self):
        return self._picked

    @picked.setter
    def picked(self, value):
        self._picked = value

    def __str__(self):
        return self._name
