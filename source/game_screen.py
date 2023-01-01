import pygame
import typing
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType
from source.battle import Battle
from source.enemies import Beetle
from source.ui import Label, Alignment
from source.inventory import Inventory
from source.palmtop_ui import PalmtopUI


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

        image = pygame.Surface((100, 100))
        image.fill(pygame.Color('blue'))
        self._palmtop_button = Label(image, (40, 30), text='КПК', font_size=16)

    def draw(self, screen: pygame.Surface):
        surface = pygame.Surface((screen.get_rect().width - self._palmtop_button.rect.width, screen.get_rect().height))
        self._player_view_map.draw(surface)
        screen.blit(surface, (0, 0))
        self._palmtop_button.draw(screen, (screen.get_rect().width - self._palmtop_button.rect.width, 0))

    @property
    def game_map(self):
        return self._player_view_map

    @property
    def palmtop_button(self):
        return self._palmtop_button


class BattleScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List):
        super(BattleScreen, self).__init__(size)

        self._player_entities = player_entities
        enemy_entities = [Beetle(1), Beetle(1), Beetle(1)]
        self._battle = Battle(pygame.Rect(0, 0, *size), player_entities, enemy_entities)

    def draw(self, screen: pygame.Surface):
        self._battle.draw(screen)

    @property
    def battle(self):
        return self._battle


class PalmtopUIScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List, inventory: Inventory):
        super(PalmtopUIScreen, self).__init__(size)

        self._palmtop_ui = PalmtopUI(pygame.Rect(0, 0, *size), player_entities, inventory)

    def draw(self, screen: pygame.Surface):
        self._palmtop_ui.draw(screen)

    def get_click(self, mouse_pos: typing.Tuple[int, int]):
        self._palmtop_ui.get_click(mouse_pos)

    @property
    def exit_button(self):
        return self._palmtop_ui.exit_button
