import pygame
import typing
import random
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType
from source.battle import Battle
from source.enemies_bundle import Beetle, Hover
from source.ui import Label, Alignment
from source.inventory import Inventory
from source.palmtop_ui import PalmtopUI
from source.planet_choose import PlanetChoose
from source.hub import Hub
from source.data.sprites.primitives import BlueBackgroundSprite, NoneSprite
from source.store import Store, Money


class GameScreen(pygame.Surface):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameScreen, self).__init__(size)
        self._size = size

    def draw(self, screen: pygame.Surface):
        pass


class GameMapScreen(GameScreen):
    CellDict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                CellModifierType.EnemyCell: GenerateMod(GenerateModType.Probability, 1)}
    MapSize = (50, 50)

    def __init__(self, size: typing.Tuple[int, int], game_map: PlayerViewMap):
        super(GameMapScreen, self).__init__(size)

        self._player_view_map = game_map

        self._palmtop_button = Label(BlueBackgroundSprite().image, (40, 30), text='КПК', font_size=16)
        self._is_draw_hub_button = False
        self._hub_button = Label(BlueBackgroundSprite().image, (80, 30), text='Вернуться', font_size=16)

    def draw(self, screen: pygame.Surface):
        surface = pygame.Surface((screen.get_rect().width - self._palmtop_button.rect.width, screen.get_rect().height))
        self._player_view_map.draw(surface)
        screen.blit(surface, (0, 0))
        self._palmtop_button.draw(screen, (screen.get_rect().width - self._palmtop_button.rect.width, 0))
        if self._is_draw_hub_button:
            place = self._hub_button.image.get_rect(center=(screen.get_rect().center[0], self._hub_button.rect.height))
            self._hub_button.draw(screen, place.topleft)

    @property
    def game_map(self):
        return self._player_view_map

    @property
    def palmtop_button(self):
        return self._palmtop_button

    @property
    def hub_button(self):
        return self._hub_button

    @property
    def is_draw_hub_button(self):
        return self._is_draw_hub_button

    @is_draw_hub_button.setter
    def is_draw_hub_button(self, value):
        self._is_draw_hub_button = value


class BattleScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List, inventory: Inventory,
                 planet_index: int):
        super(BattleScreen, self).__init__(size)

        self._player_entities = player_entities
        if planet_index == 0:
            enemy_entities = [Beetle(1) for _ in range(random.randint(1, 2))]
        else:
            enemy_entities = [Hover(2) for _ in range(random.randint(1, 3))]
        self._battle = Battle(pygame.Rect(0, 0, *size), player_entities, enemy_entities, inventory)

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

    @property
    def palmtop_ui(self):
        return self._palmtop_ui

    @property
    def exit_button(self):
        return self._palmtop_ui.exit_button


class PlanetChooseScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], money: Money):
        super(PlanetChooseScreen, self).__init__(size)

        self._planet_choose = PlanetChoose(pygame.Rect(0, 0, *size), money)
        self._planet_choose.load_maps('./source/data/save')

    def draw(self, screen: pygame.Surface):
        self._planet_choose.draw(screen)

    @property
    def planet_choose(self):
        return self._planet_choose

    @property
    def exit_button(self):
        return self._planet_choose.exit_button


class HubScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int]):
        super(HubScreen, self).__init__(size)

        self._hub = Hub(pygame.Rect(0, 0, *size))

    def draw(self, screen: pygame.Surface):
        self._hub.draw(screen)

    @property
    def hub(self):
        return self._hub


class StoreScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], money: Money, inventory: Inventory):
        super(StoreScreen, self).__init__(size)

        print(inventory.items)
        self._store = Store(pygame.rect.Rect(0, 0, *size), 5, 5, 2, money, inventory)

    def draw(self, screen: pygame.Surface):
        self._store.draw(screen)

    @property
    def store(self):
        return self._store

    @property
    def exit_button(self):
        return self._store.exit_button


class HomeScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int]):
        super(HomeScreen, self).__init__(size)

    def draw(self, screen: pygame.Surface):
        label = Label(NoneSprite().image, (self._size[0] // 2, 50), text='нажмите на любую кнопку', font_size=36)
        label.draw(screen, (self._size[0] // 4, self._size[1] - label.rect.height))
