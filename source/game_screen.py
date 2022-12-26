import pygame
import typing
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType


class GameScreen(pygame.Surface):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameScreen, self).__init__(size)

    def draw(self, screen: pygame.Surface):
        pass


class GameMapScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameMapScreen, self).__init__(size)

        self._player_view_map = PlayerViewMap(pygame.rect.Rect(0, 0, *size), None)
        cell_dict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                     CellModifierType.EnemyCell: GenerateMod(GenerateModType.Probability, 1)}
        self._player_view_map.generate_map((50, 50), cell_dict)

    def draw(self, screen: pygame.Surface):
        self._player_view_map.draw(screen)

    @property
    def game_map(self):
        return self._player_view_map
