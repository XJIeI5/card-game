import typing
import pygame
from source.game_map import GameMap
from source.cell import CellModifierType, Cell
from source.generate_mod import GenerateMod
from source.data.sprites.primitives import PlayerCellSprite, UnopenedCellSprite


def draw_cell(screen: pygame.surface.Surface, rect: pygame.Rect, sprite: pygame.sprite.Sprite) -> None:
    sprite_image = pygame.transform.scale(sprite.image, (rect.width, rect.height))
    screen.blit(sprite_image, (rect.x, rect.y))


class PlayerViewMap(GameMap):
    def __init__(self, rect: pygame.rect.Rect, fill: CellModifierType):
        super(PlayerViewMap, self).__init__(rect, fill)
        self._player_position: typing.Tuple[int, int] = None
        self._opened_cells: list[list[Cell]] = []

    def generate_map(self, size: typing.Tuple[int, int],
                     cell_dict: typing.Dict[CellModifierType, GenerateMod]) -> None:
        super(PlayerViewMap, self).generate_map(size, cell_dict)
        self.init_player()
        self._opened_cells = [[(-1, (j, i)) for j in range(size[0])] for i in range(size[1])]
        self.update_opened_cells()

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        for row_index in range(len(self._cells)):
            for col_index in range(len(self._cells[row_index])):
                if self._opened_cells[row_index][col_index][0] == -1:
                    continue

                cell_rect = pygame.Rect((self._draw_start[0] + col_index *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + row_index *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height))

                if self._opened_cells[row_index][col_index][0] == 0:
                    draw_cell(surface, cell_rect, UnopenedCellSprite())
                self._cells[row_index][col_index].draw(surface, cell_rect)
                if [col_index, row_index] == self._player_position:
                    draw_cell(surface, cell_rect, PlayerCellSprite())
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def init_player(self) -> None:
        """** description **
        sets the player on the map"""

        for i in self._cells:
            for j in i:
                if j.modifier is None:
                    continue
                self._player_position = [j.y, j.x]
                break

    def move_player(self, offset: typing.Tuple[int, int]) -> None:
        """** args **
        offset  - the offset by which the player's coordinates will increase

        ** description **
        moves the player around the map"""

        self._player_position[0] += offset[0]
        self._player_position[1] += offset[1]
        if self._cells[self._player_position[1]][self._player_position[0]].modifier is None:
            self._player_position[0] -= offset[0]
            self._player_position[1] -= offset[1]
        self.update_opened_cells()

    def update_opened_cells(self):
        far = self.get_neighbors(self._opened_cells, *self._player_position, [3, 3])
        for value, coords in far:
            self._opened_cells[coords[1]][coords[0]] = (0, coords)
        closely = self.get_neighbors(self._opened_cells, *self._player_position, [1, 1])
        for value, coords in closely:
            self._opened_cells[coords[1]][coords[0]] = (1, coords)
