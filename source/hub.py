import pygame
from source.ui import Label
from source.data.sprites.primitives import GrayBackgroundSprite


class Hub:
    def __init__(self, draw_rect: pygame.Rect):
        self._draw_rect = draw_rect
        self._planet_choose_button = Label(GrayBackgroundSprite().image, (100, 100))

    def draw(self, screen: pygame.Surface):
        place = self._planet_choose_button.image.get_rect(center=self._draw_rect.center)
        self._planet_choose_button.draw(screen, place.topleft)

    @property
    def draw_rect(self):
        return self._draw_rect

    @property
    def planet_choose_button(self):
        return self._planet_choose_button
