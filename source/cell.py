import pygame.surface

from source.cell_types import CellType


class Cell:
    def __init__(self, x: int, y: int, type: CellType):
        self._x = x
        self._y = y
        self._type = type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def type(self):
        return self._type

    def draw(self, screen: pygame.surface.Surface, rect: pygame.Rect):
        """ ** args **
        screen  -  the surface on which the map will be drawn
        rect  -  the rectangle in which the map should be inscribed

        ** description **
        draws a cell"""

        pygame.draw.rect(screen, self._type.value, rect)
