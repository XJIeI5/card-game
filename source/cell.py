import pygame.surface
from enum import Enum
from source.data.sprites import primitives


class CellType(Enum):
    NoneCell = primitives.NoneCellSprite()  # background color
    EmptyCell = primitives.EmptyCellSprite()
    CellWithEnemy = primitives.CellWithEnemySprite()
    CellWithNPC = primitives.CellWithNPCSprite()


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

        sprite_image = pygame.transform.scale(self._type.value.image, (rect.width, rect.height))
        screen.blit(sprite_image, (rect.x, rect.y))

    def __repr__(self):
        return f'{self._type} Cell: {self._y}, {self._x}'
