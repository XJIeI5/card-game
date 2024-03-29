import typing
import pygame
from source.game_map import GameMap
from source.cell import CellModifierType, Cell
from source.generate_mod import GenerateMod
from source.data.sprites.primitives import PlayerCellSprite


def draw_cell(screen: pygame.surface.Surface, rect: pygame.Rect, sprite: pygame.sprite.Sprite) -> None:
    sprite_image = pygame.transform.scale(sprite.image, (rect.width, rect.height))
    screen.blit(sprite_image, (rect.x, rect.y))


class PlayerViewMap(GameMap):
    def __init__(self, rect: pygame.rect.Rect, fill: CellModifierType):
        super(PlayerViewMap, self).__init__(rect, fill)
        self._player_position: typing.Tuple[int, int] = None
        self._start_cells: typing.List[Cell] = []
        self._opened_cells: typing.List[typing.List[Cell]] = []
        self._game_map_image: pygame.Surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))

    def save_to_txt(self, file_name: str):
        cell_dict = {None: ' ', CellModifierType.EmptyCell: '#', CellModifierType.EnemyCell: 'e',
                     CellModifierType.StartCell: 's'}
        opened_dict = {-1: '-', 0: '+'}
        with open(file_name, mode='w+', encoding='utf-8') as file:
            for i in range(len(self._cells)):
                for j in range(len(self._cells[0])):
                    cell = cell_dict[self._cells[i][j].modifier]
                    opened = opened_dict[self._opened_cells[i][j][0]]
                    file.write(cell + opened)
                file.write('\n')

    def load_from_txt(self, file_name: str) -> None:
        cell_dict = {' ': None, '#': CellModifierType.EmptyCell, 'e': CellModifierType.EnemyCell,
                     's': CellModifierType.StartCell}
        opened_dict = {'-': -1, '+': 0}
        with open(file_name, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            self._height = len(lines)
            self._width = len(lines[0])
            for line_index in range(self._height):
                result = []
                opened_result = []
                for symbol_index in range(0, self._width, 2):
                    if self._width < symbol_index:
                        self._width = symbol_index
                    line = lines[line_index]
                    symbol = line[symbol_index]
                    if symbol == '\n':
                        continue
                    result.append(Cell(line_index, symbol_index // 2, cell_dict[symbol]))
                    opened_result.append((opened_dict[line[symbol_index + 1]], (symbol_index // 2, line_index)))
                self._cells.append(result)
                self._opened_cells.append(opened_result)
        self.init_player()
        # print(*self._cells, sep='\n', end='\n\n')
        # print(*self._opened_cells, sep='\n', end='\n\n')

    def generate_map(self, size: typing.Tuple[int, int],
                     cell_dict: typing.Dict[CellModifierType, GenerateMod]) -> None:
        super(PlayerViewMap, self).generate_map(size, cell_dict)
        self.init_player()
        self._opened_cells = [[(-1, (i, j)) for j in range(size[0])] for i in range(size[1])]
        self.update_opened_cells()
        # print(*self._cells, sep='\n', end='\n\n')
        # print(*self._opened_cells, sep='\n', end='\n\n')

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        for row_index in range(len(self._cells)):
            for col_index in range(len(self._cells[row_index])):
                if self._cells[row_index][col_index].modifier is None:
                    continue
                if self._opened_cells[row_index][col_index][0] == -1:
                    continue
                cell_rect = pygame.Rect((self._draw_start[0] + col_index *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + row_index *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height))
                self._cells[row_index][col_index].draw(surface, cell_rect)
        draw_cell(surface, pygame.Rect((self._draw_start[0] + self._player_position[0] *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + self._player_position[1] *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height)), PlayerCellSprite())
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def init_player(self) -> None:
        """** description **
        sets the player on the map"""

        for i in range(len(self._cells)):
            if self._cells[i][i].modifier is None:
                continue
            self._player_position = [i, i]
            break
        x, y = self._player_position
        self._cells[y][x] = Cell(x, y, CellModifierType.StartCell)
        self._start_cells.append(self._cells[y][x])

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

    def update_opened_cells(self) -> None:
        far = self.get_neighbors(self._opened_cells, *self._player_position, [2, 2])
        for value, coords in far:
            self._opened_cells[coords[0]][coords[1]] = (0, coords)

    @property
    def player_position(self):
        return self._player_position

    @property
    def start_cells(self):
        return self._start_cells
