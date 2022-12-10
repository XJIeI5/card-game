import random
import typing

import pygame

from source.cell_types import CellType
from source.generate_mod import GenerateMod, GenerateModType
from source.simplex_noise import Noise
from source.cell import Cell


class Map:
    def __init__(self, width: int, height: int, fill: CellType):
        """** args **
        width  -  width of the map
        height  -  height of the map
        fill  -  default cell type"""

        # contains all cells on map
        self._cells: list = [[Cell(i, j, fill) for j in range(height)] for i in range(width)]
        # size
        self._width = width
        self._height = height
        # visualize params
        self._cell_width: int = 15
        self._cell_height: int = 15
        self._vertical_distance_between_cells = 3
        self._horizontal_distance_between_cells = 3
        # the beginning from which to draw the map
        self._draw_start = (0, 0)
        # generate map params
        self._scale = 0.1  # de-facto, it affects how chaotic the map will be
        self._basic_cell_appearance_threshold = 130  # affects how often the base blocks will appear

    @property
    def cells(self):
        return self._cells

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

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

    def generate_map(self, cell_dict: typing.Dict[CellType, GenerateMod]):
        """** args **
        size  -  sets the size of the generated map
        cell_dict  -  specifies which cell type corresponds to which location

        ** description **
        randomly generates a map of specified sizes with cells of a specific type arranged according to certain rules"""

        base_cells = [(key, value) for key, value in cell_dict.items() if value.type == GenerateModType.Base]
        values = Noise().calc2D(self._width, self._height, self._scale)
        for array_index, value_array in enumerate(values):
            for element_index, element in enumerate(value_array):
                is_cell = True if element < self._basic_cell_appearance_threshold else False
                if not is_cell:
                    continue
                new_cell = random.choices(population=base_cells, weights=[i.value for i in cell_dict.values()], k=1)[0]
                self._cells[array_index][element_index] = Cell(array_index, element_index, new_cell[0])

    def draw(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
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

    def move(self, new_pos: typing.Tuple[int, int]) -> None:
        """** args **
        new_pos  -  new draw start position

        ** description **
        sets new draw start position"""
        self._draw_start = new_pos
