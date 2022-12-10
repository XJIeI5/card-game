import typing

import pygame

from source.cell_types import CellType
from source.generate_mod import GenerateMod
from source.generate_mod import GenerateModType
from source.cell import Cell


class Map:
    def __init__(self):
        self._cells: list = []
        self._cell_width: int = 15
        self._cell_height: int = 15
        self._vertical_distance_between_cells = 3
        self._horizontal_distance_between_cells = 3
        self._draw_start = (0, 0)

    @property
    def cells(self):
        return self._cells

    def load_from_txt(self, file: str, cell_dict: typing.Dict[str, CellType]) -> None:
        """** args **
        file  -  path to .txt file on which the map will be built
        cell_dict  -  which characters in the .txt file are responsible for which types of cells

         ** description **
         reads the file and sets the cells attribute value based on it"""

        with open(file, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_index, line in enumerate(lines):
                result = []
                for symbol_index, symbol in enumerate(line):
                    if symbol == '\n':
                        continue
                    result.append(Cell(line_index, symbol_index, cell_dict[symbol]))
                self._cells.append(result)

    def generate_map(self, size: typing.Tuple[int, int], cell_dict: typing.Dict[CellType, GenerateMod]):
        """** args **
        size  -  sets the size of the generated map
        cell_dict  -  specifies which cell type corresponds to which location

        ** description **
        randomly generates a map of specified sizes with cells of a specific type arranged according to certain rules"""

        base_cells = {i: j for i, j in cell_dict.items() if j.type == GenerateModType.Base}
        # for i in range

    def draw(self, screen: pygame.Surface, rect: pygame.Rect):
        """** args **
        screen  -  the surface on which the map will be drawn
        rect  -  the rectangle in which the map should be inscribed

        ** description **
        draws a map"""

        surface = pygame.Surface((rect.width - self._draw_start[0], rect.height - self._draw_start[1]))
        for col_index in range(len(self._cells)):
            for row_index in range(len(self._cells[col_index])):
                cell_rect = pygame.rect.Rect((rect.x + row_index *
                                              (self._cell_width + self._horizontal_distance_between_cells),
                                              rect.y + col_index *
                                              (self._cell_height + self._vertical_distance_between_cells),
                                              self._cell_width, self._cell_height))
                self._cells[col_index][row_index].draw(surface, cell_rect)
        screen.blit(surface, (self._draw_start[0] + rect.x, self._draw_start[1] + rect.y), rect)

    def move(self, new_pos: typing.Tuple[int, int]):
        """** args **
        new_pos  -  new draw start position

        ** description **
        sets new draw start position"""
        self._draw_start = new_pos
