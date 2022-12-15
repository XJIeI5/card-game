import math
import random
import typing

import pygame

from source.generate_mod import GenerateMod, GenerateModType
from source.simplex_noise import Noise
from source.cell import Cell, CellModifierType
from source.triangulation import get_lines_from_triangulation


def get_cells_with_same_generate_mod(cell_dict: typing.Dict[CellModifierType, GenerateMod], condition: GenerateModType) \
        -> list[typing.Tuple[CellModifierType, GenerateMod]]:
    """** args **
    cell_dict  -  dictionary with all types of cells
    condition  -  searchable generate mod type

    ** description **
    returns a list of tuples that matches the condition
    """

    return [(key, value) for key, value in cell_dict.items() if value.type == condition]


def check_neighbour(board: list, col_index: int, row_index: int):
    """** args **
    board  -  the board on which the search will be performed
    row_index  -  the row index of the element around which the search will take place
    col_index  -  the col index of the element around which the search will take place

    ** description **
    return True if col_index and row_index within the board sizes"""

    is_within_borders = 0 <= col_index < len(board[0]) and 0 <= row_index < len(board)
    # is_cell_not_none = board[col_index][row_index].modifier is not None
    return is_within_borders


class GameMap:
    def __init__(self, rect: pygame.rect.Rect, fill: CellModifierType):
        """** args **
        rect  -  rect in which the map will be drawn
        fill  -  default cell type"""

        # size
        self._width: int = 0
        self._height: int = 0
        # contains all cells on map
        self._fill = fill
        self._cells = []
        self._entity_cells = []
        self.fill_map()
        # visualize params
        self._cell_width: int = 8
        self._cell_height: int = 8
        self._horizontal_distance_between_cells: int = 2
        self._vertical_distance_between_cells: int = 2
        # the beginning from which to draw the map
        self._draw_start: tuple = (0, 0)
        self._draw_rect = rect
        # generate map params
        self._noise = Noise()
        self._scale: float = 0.08  # de-facto, it affects how chaotic the map will be
        self._basic_cell_appearance_threshold: float = 130  # affects how often the base blocks will appear
        self._general_chance_to_appear_probability_cell: float = 0.03
        self._general_chance_to_appear_count_cell: float = 0.03

    def load_from_txt(self, file: str, cell_dict: typing.Dict[str, CellModifierType]) -> None:
        """** args **
        file  -  path to .txt file on which the map will be built
        cell_dict  -  which characters in the .txt file are responsible for which types of cells

         ** description **
         reads the file and sets the cells attribute value based on it"""
        self._cells = []
        with open(file, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            self._height = len(lines)
            self._width = len(lines[0])
            for line_index, line in enumerate(lines):
                result = []
                for symbol_index, symbol in enumerate(line):
                    if self._width < symbol_index:
                        self._width = symbol_index
                    if symbol == '\n':
                        continue
                    result.append(Cell(line_index, symbol_index, cell_dict[symbol]))
                self._cells.append(result)

    def fill_map(self):
        """** description **
        recreates the self._cells from the Cell.modifier = self._fill"""
        self._cells = [[Cell(j, i, self._fill) for j in range(self._height)] for i in range(self._width)]

    def generate_map(self, size: typing.Tuple[int, int],
                     cell_dict: typing.Dict[CellModifierType, GenerateMod]) -> None:
        """** args **
        size  -  sets the size of the generated map
        cell_dict  -  specifies which cell type corresponds to which location

        ** description **
        randomly generates a map of specified sizes with cells of a specific type arranged according to certain rules"""

        self._width, self._height = size

        base_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Base)
        probability_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Probability)
        count_cells = get_cells_with_same_generate_mod(cell_dict, GenerateModType.Count)

        self.fill_map()
        self._noise.update_perm()

        placed_cell_indexes = self.place_base_type_cells(base_cells)
        placed_cell_indexes += self.place_bridge_cells(base_cells)
        self.place_probability_type_cells(probability_cells, placed_cell_indexes)
        self.place_count_type_cells(count_cells, base_cells, placed_cell_indexes)

    def place_base_type_cells(self, base_cells: list[typing.Tuple[CellModifierType, GenerateMod]]) \
            -> list[typing.Tuple[int, int]]:
        """** args **
        base_cells  -  list of CellTypes and GenerateMod with GenerateMod.type == Base

        ** description **
        places base type cells on map arranges according to the generated noise
         and returns the coordinates to which they were placed"""

        values = self._noise.calc2D_smooth(self._width, self._height, self._scale, 3)
        base_cells_placed_cell_indexes = []
        for array_index, value_array in enumerate(values):
            for element_index, element in enumerate(value_array):
                if not self.is_cell_placed(element):
                    continue
                new_cell_couple = (None, GenerateMod(GenerateModType.Base, 1))
                if base_cells:
                    new_cell_couple = self.get_base_type_cell(base_cells)
                self._cells[array_index][element_index] = \
                    Cell(array_index, element_index, new_cell_couple[0])
                base_cells_placed_cell_indexes.append((array_index, element_index))
        return base_cells_placed_cell_indexes

    def place_bridge_cells(self, base_cells: list[typing.Tuple[CellModifierType, GenerateMod]]) \
            -> list[typing.Tuple[int, int]]:
        """** args **
        base_cells  - list of CellTypes and GenerateMod with GenerateMod.type == Base

         ** description **
         places base type cells on map to connect islands and returns the coordinates to which they were placed"""

        bridge_cells_placed_cell_indexes = []
        bridge_cell_indexes = self.connect_cells(self.get_cell_on_each_island())
        for cell_index in bridge_cell_indexes:
            array_index, element_index = cell_index
            new_cell_couple = (None, GenerateMod(GenerateModType.Base, 1))
            if base_cells:
                new_cell_couple = self.get_base_type_cell(base_cells)
            self._cells[array_index][element_index] = \
                Cell(array_index, element_index, new_cell_couple[0])
            bridge_cells_placed_cell_indexes.append((array_index, element_index))
        return bridge_cells_placed_cell_indexes

    def place_probability_type_cells(self, probability_cells: list[typing.Tuple[CellModifierType, GenerateMod]],
                                     placed_cell_indexes: list[typing.Tuple[int, int]]) -> list[typing.Tuple[int, int]]:
        """** args **
        probability_cells  -  list of CellTypes and GenerateMod with GenerateMod.type == Probability
        placed_cell_indexes  -  indexes of GenerateMod.type == Base cells on map

        ** description **
        places probability type cells on the map on base type cells
         and returns the coordinates to which they were placed"""

        probability_cells_placed_cell_indexes = []
        for cell_index in placed_cell_indexes:
            array_index, element_index = cell_index
            new_cell_couple = (CellModifierType.EmptyCell, GenerateMod(GenerateModType.Base, 1))
            if not probability_cells:
                break
            new_probability_cell_couple = self.get_probability_type_cell(probability_cells)
            if new_probability_cell_couple is not None:
                new_cell_couple = new_probability_cell_couple
            new_cell = Cell(array_index, element_index, new_cell_couple[0])
            self._cells[array_index][element_index] = new_cell
            probability_cells_placed_cell_indexes.append((array_index, element_index))
        return probability_cells_placed_cell_indexes

    def place_count_type_cells(self, count_cells: list[typing.Tuple[CellModifierType, GenerateMod]],
                               base_cells: list[typing.Tuple[CellModifierType, GenerateMod]],
                               placed_cell_indexes: list[typing.Tuple[int, int]]) -> list[typing.Tuple[int, int]]:
        """** args **
        count_cells  -  list of CellTypes and GenerateMod with GenerateMod.type == Count
        base_cells  -  list of CellTypes and GenerateMod with GenerateMod.type == Base
        placed_cell_indexes  -  indexes of GenerateMod.type == Base cells on map

        ** description **
        places count type cells on the map on base type cells and returns the coordinates to which they were placed"""

        count_cells_placed_cell_indexes = []
        base_cell_types: list[CellModifierType] = [i[0] for i in base_cells]
        count_cell_amount = sum([i[1].value for i in count_cells])
        print(count_cell_amount)
        try:
            count_cell_place_indexes = random.sample(placed_cell_indexes, count_cell_amount)
        except ValueError:
            return []
        while count_cell_amount > 0:
            count_cell_amount -= 1
            new_cell_couple = self.get_count_type_cell(count_cells)
            current_count_cell_place_index = count_cell_place_indexes[count_cell_amount]
            array_index, element_index = current_count_cell_place_index
            if new_cell_couple is None:
                continue
            if self._cells[array_index][element_index].modifier \
                    not in base_cell_types:
                count_cell_place_indexes = random.sample(placed_cell_indexes, count_cell_amount + 1)
                continue
            new_cell = Cell(array_index, element_index, new_cell_couple[0])
            self._cells[array_index][element_index] = new_cell
            count_cells_placed_cell_indexes.append(current_count_cell_place_index)
            count_cells.remove(new_cell_couple)
        return count_cells_placed_cell_indexes

    def is_cell_placed(self, random_probability: float) -> bool:
        """** args **
        random_probability  -  random number

        ** description **
        return True or False, based on input number and self._basic_cell_appearance_threshold"""

        return True if random_probability > self._basic_cell_appearance_threshold else False

    @staticmethod
    def get_base_type_cell(base_cells: list[typing.Tuple[CellModifierType, GenerateMod]]) \
            -> typing.Tuple[CellModifierType, GenerateMod]:
        """** args **
        base_cells  -  list of cells to choose one

        ** description **
        return a random cell, based on weights on their generate mod"""

        return random.choices(population=base_cells, weights=[i[1].value for i in base_cells], k=1)[0]

    def get_probability_type_cell(self, probability_cells: list[typing.Tuple[CellModifierType, GenerateMod]]) \
            -> typing.Union[None, typing.Tuple[CellModifierType, GenerateMod]]:
        """** args **
        probability_cells  -  list of cells to choose one

        ** description **
        return a random cell or None, based on weights on their generate mod and
         self._general_chance_to_appear_probability_cell"""

        if random.random() > self._general_chance_to_appear_probability_cell:
            return None
        return random.choices(population=probability_cells, weights=[i[1].value for i in probability_cells], k=1)[0]

    @staticmethod
    def get_count_type_cell(count_cells: list[typing.Tuple[CellModifierType, GenerateMod]]) \
            -> typing.Union[None, typing.Tuple[CellModifierType, GenerateMod]]:
        """** args **
        count_cells  -  list of cells to choose one

        ** description **
        return a random cell or None, based on weights on their generate mod,
         self._general_chance_to_appear_count_cell and value of generate mod"""

        new_count_cell_type, generate_mod = random.choice(count_cells)
        if generate_mod.value <= 0 or generate_mod.type != GenerateModType.Count:
            return None

        generate_mod.value = generate_mod.value - 1
        return new_count_cell_type, generate_mod

    def connect_cells(self, coordinates: list[typing.Tuple[int, int]]) -> list:
        """** args **
        coordinates  -  points to build bridges

        ** description **
        triangulates and builds bridges between points, which indexes returns"""

        result = []
        lines = get_lines_from_triangulation(coordinates, self._width, self._height)
        for line_index in range(len(lines) - 1):
            line_points = self.bresenham_algorithm(lines[line_index], lines[line_index + 1])
            for point in line_points[1:]:
                if self._cells[point[0]][point[1]].modifier != self._fill:
                    break
                result.append(point)
        return result

    def get_cell_on_each_island(self) -> list[pygame.Vector2]:
        """** description **
        return random cell from each island"""

        islands = self.get_islands()
        coordinates = []
        for cells in islands:
            closest_cell = None
            shortest_distance = -1
            center_cell = self._cells[self._width // 2][self._height // 2]
            for cell in cells:
                distance = ((cell.x - center_cell.x) ** 2) + ((cell.y - center_cell.y) ** 2)
                if distance < shortest_distance or shortest_distance == -1:
                    shortest_distance = distance
                    closest_cell = cell
            coordinates.append(pygame.Vector2(closest_cell.x, closest_cell.y))
        return coordinates

    @staticmethod
    def bresenham_algorithm(point1, point2) -> list[typing.Tuple[int, int]]:
        """** args **
        point1  -  start of line
        point2  -  end of line

        ** description **
        returns the coordinates of the points that need to be traversed to move from point1 to point2"""

        points = []
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]

        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if dx < 0:
            dx = -dx
        if dy < 0:
            dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = point1
        error, t = el / 2, 0
        points.append([x, y])
        while t < el:
            error -= es
            if error < 0:
                error += el
                points.append([x + pdx, y + pdy])
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            points.append([x, y])
        return points

    def get_islands(self) -> list[list[Cell]]:
        """** description **
        returns a list of 'islands' (a list of cells that are separated from the rest by self._fill cells)"""

        islands = []
        for row_index, row in enumerate(self._cells):
            for cell_index, cell in enumerate(row):
                if cell.modifier == self._fill:
                    continue
                if any([cell in i for i in islands]):
                    continue
                islands.append(self.get_connected_cells(row_index, cell_index))
        return islands

    def get_connected_cells(self, row_index: int, col_index: int) -> list:
        """** args **
        row_index  -  the index of row of the cell from which you want to get docked
        col_index  -  the index of col of the cell from which you want to get docked

        ** description **
        returns a list of cells that are separated from the rest by self._fill cells"""

        connected_cells = []
        coordinates = [(row_index, col_index)]
        while coordinates:
            copy_coordinates = coordinates.copy()
            for cell_coord in coordinates:
                cell_coord_row, cell_coord_col = cell_coord
                if self._cells[cell_coord_row][cell_coord_col] == self._fill:
                    copy_coordinates.remove(cell_coord)
                else:
                    copy_coordinates.remove(cell_coord)
                    connected_cells_coords = [(cell.x, cell.y) for cell in connected_cells]
                    neighbor_cells = self.get_neighbors(self._cells, cell_coord[1], cell_coord[0], (1, 1))
                    copy_coordinates.extend([(cell.x, cell.y) for cell in neighbor_cells if cell.modifier != self._fill
                                             and (cell.x, cell.y) not in connected_cells_coords])
                    copy_coordinates = list(set(copy_coordinates))
                if self._cells[cell_coord_row][cell_coord_col] not in connected_cells:
                    connected_cells.append(self._cells[cell_coord_row][cell_coord_col])
            coordinates = list(set(copy_coordinates)).copy()
        return connected_cells

    @staticmethod
    def get_neighbors(board: list, col_index: int, row_index: int, search_radius: typing.Tuple[int, int]):
        """** args **
        board  -  the board on which the search will be performed
        row_index  -  the row index of the element around which the search will take place
        col_index  -  the col index of the element around which the search will take place
        search_radius  -  tuple of numbers to which a search will be performed in both directions

        ** description **
        return a list of values, searched in search_radius on board"""

        ways = []
        for i in range(-search_radius[0], search_radius[0] + 1, 1):
            for j in range(-search_radius[0], search_radius[1] + 1, 1):
                if i == 0 and j == 0:
                    continue
                ways.append((i, j))
        return [board[row_index + dy][col_index + dx]
                for dx, dy in ways if check_neighbour(board, col_index + dx, row_index + dy)]

    def draw(self, screen: pygame.Surface) -> None:
        """** args **
        screen  -  the surface on which the map will be drawn
        rect  -  the rectangle in which the map should be inscribed

        ** description **
        draws a map"""

        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        for row_index in range(len(self._cells)):
            for col_index in range(len(self._cells[row_index])):
                cell_rect = pygame.Rect((self._draw_start[0] + col_index *
                                         (self._cell_width + self._horizontal_distance_between_cells),
                                         self._draw_start[1] + row_index *
                                         (self._cell_height + self._vertical_distance_between_cells),
                                         self._cell_width, self._cell_height))
                self._cells[row_index][col_index].draw(surface, cell_rect)
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def move(self, offset: typing.Tuple[int, int]) -> None:
        """** args **
        new_pos  -  new draw start position

        ** description **
        sets new draw start position"""
        self._draw_start = self._draw_start[0] + offset[0], self._draw_start[1] + offset[1]

    def get_cell(self, mouse_pos: typing.Tuple[int, int]) -> typing.Union[None, typing.Tuple[int, int]]:
        """** args **
        mouse_pos  -  mouse screen position

        ** description **
        returns the coordinates of the clicked cell"""

        cell = (mouse_pos[1] - self._draw_rect.y) // (self._cell_height + self._vertical_distance_between_cells), \
               (mouse_pos[0] - self._draw_rect.x) // (self._cell_width + self._horizontal_distance_between_cells)
        if 0 <= cell[1] < self._width and 0 <= cell[0] < self._height and \
                self._cells[cell[0]][cell[1]].modifier is not None:
            return cell
        return None

    @property
    def cells(self):
        return self._cells

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
