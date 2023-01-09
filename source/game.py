import pygame
import sys
import typing
from enum import Enum
from source.game_screen import GameMapScreen, BattleScreen, PalmtopUIScreen, PlanetChooseScreen, HubScreen
from source.player_entity import PlayerEntity, PlayerSpeciality
from source.cell import Cell, CellModifierType
from source.card_bundle import FastPunch, ShieldRestruct
from source.data.sprites.primitives import PlayerCellSprite, ScaledSprite
from source.inventory import Inventory
from source.items_bundle import RockItem, GlassItem, HealingSerumItem, SmallPistolItem


class GameState(Enum):
    GameMap = 0
    Battle = 1
    Palmtop = 2
    PlanetChoose = 3
    Hub = 4


class TestSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TestSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect()


class Game:
    def __init__(self, size: typing.Tuple[int, int]):
        pygame.init()
        self._window_size = self._window_width, self._window_height = size
        self._screen = pygame.display.set_mode(size)
        self._clock = pygame.time.Clock()
        self._screen.fill(pygame.Color('black'))
        self._fps = 60
        self._state = GameState.Hub
        cards = [ShieldRestruct, FastPunch]
        self._player_entities = [PlayerEntity(ScaledSprite(TestSprite()), 'A person', 50, 25, 10, 1,
                                              PlayerSpeciality.Medic, 1),
                                 PlayerEntity(ScaledSprite(PlayerCellSprite()), 'B person', 50, 25, 10, 1,
                                              PlayerSpeciality.Tank, 1),
                                 PlayerEntity(ScaledSprite(TestSprite()), 'C person', 50, 25, 10, 1,
                                              PlayerSpeciality.Engineer, 1)]
        [i.extend_cards(cards) for i in self._player_entities]
        self._inventory = Inventory(pygame.Rect(0, 0,
                                                self._window_width // 2, self._window_height // 2), 5, 5, 2)
        [self._inventory.extend_items({SmallPistolItem: 1, RockItem: 2, HealingSerumItem: 2}) for _ in range(3)]

        self._game_map_screen: typing.Union[None, GameMapScreen] = None
        self._battle_screen: typing.Union[None, BattleScreen] = None
        self._palmtop_screen: typing.Union[None, PalmtopUIScreen] = None
        self._planet_choose_screen = PlanetChooseScreen(size)
        self._hub_screen = HubScreen(size)

    def run(self) -> None:
        while True:
            if self._state == GameState.GameMap:
                self.game_map_view()
            elif self._state == GameState.Battle:
                self.battle_view()
            elif self._state == GameState.Palmtop:
                self.palmtop_view()
            elif self._state == GameState.PlanetChoose:
                self.planet_choose_view()
            elif self._state == GameState.Hub:
                self.hub_view()

            self._clock.tick(self._fps)
            pygame.display.flip()

    def game_map_view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self._game_map_screen.game_map.move_player((-1, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self._game_map_screen.game_map.move_player((1, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self._game_map_screen.game_map.move_player((0, 1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self._game_map_screen.game_map.move_player((0, -1))

            # state changing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._game_map_screen.palmtop_button.rect.collidepoint(event.pos):
                    self._state = GameState.Palmtop
                    self._palmtop_screen = PalmtopUIScreen(self._window_size, self._player_entities, self._inventory)

                if self._game_map_screen.hub_button.rect.collidepoint(event.pos):
                    self._state = GameState.Hub

        if self._game_map_screen.game_map.player_position in\
                [[cell.x, cell.y] for cell in self._game_map_screen.game_map.start_cells]:
            self._game_map_screen.is_draw_hub_button = True
        else:
            self._game_map_screen.is_draw_hub_button = False

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_w]:
            self._game_map_screen.game_map.move((0, 1))
        if key_state[pygame.K_s]:
            self._game_map_screen.game_map.move((0, -1))
        if key_state[pygame.K_a]:
            self._game_map_screen.game_map.move((1, 0))
        if key_state[pygame.K_d]:
            self._game_map_screen.game_map.move((-1, 0))
        self._screen.fill(pygame.Color('black'))
        self._game_map_screen.draw(self._screen)

        # state changing
        player_position = self._game_map_screen.game_map.player_position
        if self._game_map_screen.game_map.cells[player_position[1]][player_position[0]].modifier == \
                CellModifierType.EnemyCell:
            self._state = GameState.Battle
            self._battle_screen = BattleScreen(self._window_size, self._player_entities)
            print('BATTLE')

    def battle_view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._battle_screen.battle.get_click(event.pos)
        self._screen.fill(pygame.Color('black'))
        self._battle_screen.draw(self._screen)

        # state changing
        if self._battle_screen.battle.is_win:
            self._state = GameState.GameMap
            player_position = self._game_map_screen.game_map.player_position
            self._game_map_screen.game_map.cells[player_position[1]][player_position[0]] = \
                Cell(player_position[1], player_position[0], CellModifierType.EmptyCell)

    def palmtop_view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # state changing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._palmtop_screen.exit_button.rect.collidepoint(event.pos):
                    self._state = GameState.GameMap
                self._palmtop_screen.palmtop_ui.get_click(event)

        self._screen.fill(pygame.Color('black'))
        self._palmtop_screen.draw(self._screen)

    def planet_choose_view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # state changing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._planet_choose_screen.exit_button.rect.collidepoint(event.pos):
                    self._state = GameState.Hub
                for index, button in enumerate(self._planet_choose_screen.planet_choose.planet_buttons):
                    if button.rect.collidepoint(event.pos):
                        game_map = self._planet_choose_screen.planet_choose.\
                            get_planet(index, GameMapScreen.MapSize, GameMapScreen.CellDict)
                        self._state = GameState.GameMap
                        self._game_map_screen = GameMapScreen(self._window_size, game_map)

        self._screen.fill(pygame.Color('black'))
        self._planet_choose_screen.draw(self._screen)

    def hub_view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # state changing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._hub_screen.hub.planet_choose_button.rect.collidepoint(event.pos):
                    self._state = GameState.PlanetChoose

        self._screen.fill(pygame.Color('black'))
        self._hub_screen.draw(self._screen)
