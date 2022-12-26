import pygame
import typing
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType
from source.battle import Battle
from source.enemies import Beetle


class GameScreen(pygame.Surface):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameScreen, self).__init__(size)

    def draw(self, screen: pygame.Surface):
        pass


class GameMapScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameMapScreen, self).__init__(size)

        self._player_view_map = PlayerViewMap(pygame.Rect(0, 0, *size), None)
        cell_dict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                     CellModifierType.EnemyCell: GenerateMod(GenerateModType.Probability, 1)}
        self._player_view_map.generate_map((50, 50), cell_dict)

    def draw(self, screen: pygame.Surface):
        self._player_view_map.draw(screen)

    @property
    def game_map(self):
        return self._player_view_map


class BattleScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List):
        super(BattleScreen, self).__init__(size)

        self._player_entities = player_entities
        enemy_entities = [Beetle(), Beetle(), Beetle()]
        self._battle = Battle(pygame.Rect(0, 0, *size), player_entities, enemy_entities)

    def draw(self, screen: pygame.Surface):
        self._battle.draw(screen)

    @property
    def battle(self):
        return self._battle
