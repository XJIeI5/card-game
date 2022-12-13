import typing
from source.pathfinding import dijkstra
from source.map import Map


class PlayerOnMap:
    """Represents the player on the map"""

    def __init__(self, start_pos: typing.Tuple[int, int], game_map: Map):
        self._position: tuple = start_pos
        self._game_map: Map = game_map
        self._path = []

    def set_path(self, end_point: typing.Tuple[int, int]) -> None:
        """** args **
        end_point  -  the point at which the player should come

        ** description **
        sets player path (indexes of points that the player must pass through to reach the end_point)"""

        graph = {}
        for array_index, array in enumerate(self._game_map.cells):
            for element_index, element in enumerate(array):
                neighbors = [(i, (i.y, i.x)) for i in
                             self._game_map.get_neighbors(self._game_map.cells, array_index, element_index, (1, 1))]
                graph[(array_index, element_index)] = graph.get((array_index, element_index), []) + neighbors
        visited = dijkstra(self._position, end_point, graph)
        return self.restore_path(visited, end_point)

    @staticmethod
    def restore_path(visited: dict[typing.Tuple[int, int], typing.Union[None, typing.Tuple[int, int]]],
                     end_point: typing.Tuple[int, int])\
            -> list[typing.Tuple[int, int]]:
        """** args **
        visited  -  dictionary of all visited cells and their preceding cells
        end_point  -  the point at which the player should come

        ** description **
        from all the visited cells restores the path to the end_point"""

        path, path_segment = [], end_point
        while path_segment and path_segment in visited:
            path.append(path_segment)
            path_segment = visited[path_segment]
        return path[::-1]
