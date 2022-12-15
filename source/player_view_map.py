import typing
import pygame
from source.game_map import GameMap
from source.cell import CellModifierType
from source.data.sprites.primitives import PlayerCellSprite


def draw_player(screen: pygame.surface.Surface, rect: pygame.Rect) -> None:
    sprite_image = pygame.transform.scale(PlayerCellSprite().image, (rect.width, rect.height))
    screen.blit(sprite_image, (rect.x, rect.y))


class PlayerViewMap(GameMap):
    def __init__(self, rect: pygame.rect.Rect, fill: CellModifierType):
        super(PlayerViewMap, self).__init__(rect, fill)
        self._player_position = None

    def init_player(self) -> None:
        for i in self._cells:
            for j in i:
                if j.modifier is None:
                    continue
                self._player_position = [j.x, j.y]
                break

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        for row_index in range(len(self._cells)):
            for col_index in range(len(self._cells[row_index])):
                cell_rect = pygame.Rect((self._draw_start[0] + col_index *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + row_index *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height))
                self._cells[row_index][col_index].draw(surface, cell_rect)
                if [col_index, row_index] == self._player_position:
                    draw_player(surface, cell_rect)
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def move_player(self, offset: typing.Tuple[int, int]) -> None:
        self._player_position[0] += offset[0]
        self._player_position[1] += offset[1]
