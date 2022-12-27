import pygame
import typing
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType
from source.battle import Battle
from source.enemies import Beetle
from source.ui import Button


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

        image = pygame.Surface((20, 20))
        image.fill(pygame.Color('blue'))
        self._palmtop_button = Button(image, (20, 20))

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
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List):
        super(PalmtopUIScreen, self).__init__(size)

        self._player_entities = player_entities
        image = pygame.Surface((20, 20))
        image.fill(pygame.Color('blue'))
        self._exit_button = Button(image, (20, 20))

    def draw(self, screen: pygame.Surface):
        indent = 25
        icon_size = (screen.get_size()[0] - indent * len(self._player_entities)) // len(self._player_entities)
        for index, player_entity in enumerate(self._player_entities):
            screen.blit(pygame.transform.scale(player_entity.icon, (icon_size, icon_size)),
                        ((icon_size + indent) * index, 0))
        self._exit_button.draw(screen, (screen.get_rect().width - self._exit_button.rect.width, 0))

    @property
    def exit_button(self):
        return self._exit_button
