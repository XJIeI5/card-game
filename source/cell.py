import pygame.surface
from enum import Enum
from source.data.sprites import primitives


class CellModifierType(Enum):
    EmptyCell = primitives.EmptyCellSprite()
    EnemyCell = primitives.EnemyCellSprite()
    NPCCell = primitives.NPCCellSprite()
    StartCell = primitives.StartCellSprite()


class Cell:
    def __init__(self, x: int, y: int, mod_type: CellModifierType):
        self._x = x
        self._y = y
        self._modifier_type = mod_type

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def modifier(self):
        return self._modifier_type

    def draw(self, screen: pygame.surface.Surface, rect: pygame.Rect):
        """ ** args **
        screen  -  the surface on which the map will be drawn
        rect  -  the rectangle in which the map should be inscribed

        ** description **
        draws a cell"""

        if not self._modifier_type:
            return
        sprite_image = pygame.transform.scale(self._modifier_type.value.image, (rect.width, rect.height))
        screen.blit(sprite_image, (rect.x, rect.y))

    def __repr__(self):
        return f'{self._modifier_type}: {self._x}, {self._y}'
