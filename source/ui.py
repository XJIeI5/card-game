import pygame
import typing
from enum import Enum


class Alignment(Enum):
    Center = 0
    Left = 1
    Right = 2


class Label(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], text: str = '', font_size: int = 12,
                 alignment=Alignment.Center):
        super(Label, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self._rect = self.image.get_rect()
        self._text = text
        self._font_size = font_size
        self._offset = (0, 0)
        self._alignment = alignment

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self._offset = position
        screen.blit(self.image, position)
        text = pygame.font.Font(None, self._font_size).render(self._text, True, pygame.Color('white'))
        if self._alignment == Alignment.Center:
            place = text.get_rect(center=self.rect.center)
        elif self._alignment == Alignment.Left:
            place = text.get_rect(topleft=self.rect.topleft)
            place.x += 5
        else:
            place = text.get_rect(topright=self.rect.topright)
            place.x -= 5
        screen.blit(text, (place.x, self.rect.center[1] - self.rect.height // 4))

    def set_text(self, new_text: str):
        self._text = new_text

    @property
    def rect(self):
        return pygame.Rect(self._rect.x + self._offset[0],
                           self._rect.y + self._offset[1],
                           self._rect.width, self._rect.height)

    @property
    def offset(self):
        return self._offset
