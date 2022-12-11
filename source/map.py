import random
import typing

import pygame

from source.generate_mod import GenerateMod, GenerateModType
from source.simplex_noise import Noise
from source.cell import Cell, CellType


def get_cells_with_same_generate_mod(cell_dict: typing.Dict[CellType, GenerateMod], condition: GenerateModType) \
        -> list[typing.Tuple[CellType, GenerateMod]]:
    """** args **
    cell_dict  -  dictionary with all types of cells
    condition  -  searchable generate mod type

    ** description **
    returns a list of tuples that matches the condition
    """

    return [(key, value) for key, value in cell_dict.items() if value.type == condition]


class Map:
    def __init__(self, width: int, height: int, fill: CellType):
        """** args **
        width  -  width of the map
        height  -  height of the map
        fill  -  default cell type"""

        # contains all cells on map
        self._cells: list = [[Cell(i, j, fill) for j in range(height)] for i in range(width)]
        self._fill = fill
        # size
        self._width: int = width
        self._height: int = height
        # visualize params
        self._cell_width: int = 20
        self._cell_height: int = 20
        self._horizontal_distance_between_cells: int = 3
        self._vertical_distance_between_cells: int = 3
        # the beginning from which to draw the map
        self._draw_start: tuple = (0, 0)
        # generate map params
        self._noise = Noise()
        self._scale: float = 0.08  # de-facto, it affects how chaotic the map will be
        self._basic_cell_appearance_threshold: float = 130  # affects how often the base blocks will appear
        self._general_chance_to_appear_probability_cell: float = 0.03
        self._general_chance_to_appear_count_cell: float = 0.03

    @property
    def cells(self):
        return self._cells

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def noise(self):
        return self._noise

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

        base_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Base)
        probability_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Probability)
        count_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Count)

        self._cells = [[Cell(i, j, self._fill) for j in range(self._height)] for i in range(self._width)]
        self._noise.update_perm()
        values = self._noise.calc2D_smooth(self._width, self._height, self._scale, 3)
        for array_index, value_array in enumerate(values):
            for element_index, element in enumerate(value_array):
                if not self.is_cell_placed(element):
                    continue
                new_cell_couple = self.get_base_cell(base_cells)

                new_probability_cell_couple = self.get_probability_cell(probability_cells)
                if new_probability_cell_couple is not None:
                    new_cell_couple = new_probability_cell_couple

                new_count_cell_couple = self.get_count_cell(count_cells)
                if new_count_cell_couple is not None:
                    new_cell_couple = new_count_cell_couple

                self._cells[array_index][element_index] = Cell(array_index, element_index, new_cell_couple[0])

    def is_cell_placed(self, random_probability: float) -> bool:
        """** args **
        random_probability  -  random number

        ** description **
        return True or False, based on input number and self._basic_cell_appearance_threshold"""

        return True if random_probability > self._basic_cell_appearance_threshold else False

    @staticmethod
    def get_base_cell(base_cells: list[typing.Tuple[CellType, GenerateMod]]) -> typing.Tuple[CellType, GenerateMod]:
        """** args **
        base_cells  -  list of cells to choose one

        ** description **
        return a random cell, based on weights on their generate mod"""
        return random.choices(population=base_cells, weights=[i[1].value for i in base_cells], k=1)[0]

    def get_probability_cell(self, probability_cells: list[typing.Tuple[CellType, GenerateMod]]) \
            -> typing.Union[None, typing.Tuple[CellType, GenerateMod]]:
        """** args **
        probability_cells  -  list of cells to choose one

        ** description **
        return a random cell or None, based on weights on their generate mod and
         self._general_chance_to_appear_probability_cell"""

        if random.random() > self._general_chance_to_appear_probability_cell:
            return None
        return random.choices(population=probability_cells, weights=[i[1].value for i in probability_cells], k=1)[0]

    def get_count_cell(self, count_cells: list[typing.Tuple[CellType, GenerateMod]]) \
            -> typing.Union[None, typing.Tuple[CellType, GenerateMod]]:
        """** args **
        count_cells  -  list of cells to choose one
        
        ** description **
        return a random cell or None, based on weights on their generate mod,
         self._general_chance_to_appear_count_cell and value of generate mod"""

        if random.random() > self._general_chance_to_appear_probability_cell:
            return None

        new_count_cell_type, generate_mod = random.choice(count_cells)
        if generate_mod.value <= 0 or generate_mod.type != GenerateModType.Count:
            return None

        generate_mod.value = generate_mod.value - 1
        return new_count_cell_type, generate_mod

    def draw(self, screen: pygame.Surface, rect: pygame.Rect) -> None:
        """** args **
        screen  -  the surface on which the map will be drawn
        rect  -  the rectangle in which the map should be inscribed

        ** description **
        draws a map"""

        surface = pygame.Surface((rect.width, rect.height))
        for row_index in range(len(self._cells)):
            for col_index in range(len(self._cells[row_index])):
                cell_rect = pygame.Rect((self._draw_start[0] + col_index *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + row_index *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height))
                self._cells[row_index][col_index].draw(surface, cell_rect)
        screen.blit(surface, (rect.x, rect.y))

    def move(self, new_pos: typing.Tuple[int, int]) -> None:
        """** args **
        new_pos  -  new draw start position

        ** description **
        sets new draw start position"""
        self._draw_start = new_pos
