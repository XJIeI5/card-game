import typing
import pygame
from source.ui import Label, Alignment
from source.data.sprites.primitives import BlueBackgroundSprite


class Skill(pygame.sprite.Sprite):
    def __init__(self, name: str, max_level: int, level_effects: typing.List, description: typing.Dict[int, str],
                 current_level: int = 0):
        super(Skill, self).__init__()
        self.image = BlueBackgroundSprite().image
        self.rect = self.image.get_rect()
        self._name = name
        if len(level_effects) > max_level:
            raise ValueError('level_effects cannot be less than max_level')
        if description and max(description.keys()) > max_level:
            raise ValueError('description cannot be less than max_level')

        self._max_level = max_level
        self._current_level = current_level
        self._description = description
        self._level_effects = level_effects
        self._max_level_is_reached = False

    def apply_effect(self, entity):
        if not self._level_effects:
            return
        if self._max_level_is_reached:
            return
        if not self._current_level:
            return

        self._level_effects[self._current_level - 1](entity)

    def level_up(self):
        self._current_level += 1
        if self._current_level > self._max_level:
            self._max_level_is_reached = True
            self._current_level = self._max_level

    def draw(self, screen: pygame.Surface, draw_rect: pygame.rect.Rect, font_size: int = 20):
        self.image = pygame.transform.scale(self.image, (draw_rect.width, draw_rect.height))
        self.rect = pygame.Rect(*draw_rect.topleft,
                                self.image.get_rect().width, self.image.get_rect().height + 5)

        label = Label(self.image, (draw_rect.width, 30),
                      self._name, font_size=font_size, alignment=Alignment.Left)
        label.draw(screen, (draw_rect.x, draw_rect.y))

        pygame.draw.rect(screen, pygame.Color('gray'), (draw_rect.x, draw_rect.y + draw_rect.height,
                                                        draw_rect.width, 5))
        try:
            one_piece = draw_rect.width // self._max_level
            pygame.draw.rect(screen, pygame.Color('blue'), (draw_rect.x, draw_rect.y + draw_rect.height,
                                                            one_piece * self._current_level, 5))
        except ZeroDivisionError:
            pass

    @property
    def max_level(self):
        return self._max_level

    @property
    def current_level(self):
        return self._current_level

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
