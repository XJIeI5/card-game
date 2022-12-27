import pygame
import typing


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int]):
        super(Button, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self._rect = self.image.get_rect()
        self._offset = (0, 0)

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self._offset = position
        screen.blit(self.image, position)

    @property
    def rect(self):
        return pygame.Rect(self._rect.x + self._offset[0],
                           self._rect.y + self._offset[1],
                           self._rect.width, self._rect.height)
