import os
import pygame
import typing
import math
import random
from source.ui import Label, AcceptDialog
from source.data.sprites.primitives import PlanetIconSprite, BlueBackgroundSprite
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod
from source.store import Money


class PlanetChoose:
    def __init__(self, draw_rect: pygame.Rect, money: Money):
        self._draw_rect = draw_rect
        self._money = money
        self._open_planet_index: typing.Union[None, int] = None

        self._planet_buttons: typing.List[Label] = [Label(PlanetIconSprite().image, (50, 50),
                                                          text=str(i + 1), font_size=36, color=pygame.Color('black'))
                                                    for i in range(3)]
        self._planet_game_maps: typing.Dict[int, typing.Union[None, PlayerViewMap]] = \
            {i: None for i in range(len(self._planet_buttons))}
        self._planets_available: typing.Dict[int, bool] = {i: False for i in range(len(self._planet_buttons))}
        self._planets_available[0] = True

        self._exit_button = Label(BlueBackgroundSprite().image, (40, 30), text='Назад')
        self._buy_accept_dialog: typing.Union[None, AcceptDialog] = None
        self._not_enough_money_dialog: typing.Union[None, AcceptDialog] = None
        self.place_planet_buttons(100)

    def place_planet_buttons(self, radius: int):
        for index, place_button in enumerate(self._planet_buttons):
            angle = random.randint(0, 360)
            x, y = math.cos(angle), math.sin(angle)
            place_button.rect.center = (radius * (index + 1) * x + self._draw_rect.width // 2,
                                        radius * (index + 1) * y + self._draw_rect.height // 2)

    def save_maps(self, directory_name: str):
        with open(directory_name + '/available_maps.txt', mode='w', encoding='utf-8') as file:
            file.write(' '.join([str(int(i)) for i in self._planets_available.values()]))

        if not os.path.exists(directory_name + '/maps'):
            os.makedirs(directory_name + '/maps')

        for index, game_map in self._planet_game_maps.items():
            file_name = directory_name + f'/maps/map_{index}.txt'
            if game_map is None:
                open(file_name, mode='w').close()
            else:
                game_map.save_to_txt(file_name)

    def load_maps(self, directory_name: str):
        try:
            with open(directory_name + '/available_maps.txt', mode='r', encoding='utf-8') as file:
                data = file.read()
                self._planets_available = {index: bool(j) for index, j in enumerate(data.split())}
        except FileNotFoundError:
            pass

        filenames = next(os.walk(directory_name + '/maps'), (None, None, []))[2]
        for index, file_name in enumerate(filenames):
            if os.stat(directory_name + '/maps/' + file_name).st_size == 0:
                self._planet_game_maps[index] = None
            else:
                player_view_map = PlayerViewMap(self._draw_rect, None)
                player_view_map.load_from_txt(directory_name + '/maps/' + file_name)
                self._planet_game_maps[index] = player_view_map

    def draw(self, screen: pygame.Surface):
        for place_button in self._planet_buttons:
            pygame.draw.line(screen, pygame.Color('dark red'), self._draw_rect.center, place_button.rect.center)
            place_button.draw(screen, place_button.rect.topleft)

        self._exit_button.draw(screen, (self._draw_rect.topright[0] - self._exit_button.rect.width, 0))
        hub_label = Label(PlanetIconSprite().image, (25, 25))
        place = hub_label.image.get_rect(center=self._draw_rect.center)
        hub_label.draw(screen, place.topleft)

        if self._buy_accept_dialog is not None:
            self._buy_accept_dialog.draw(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))
        if self._not_enough_money_dialog is not None:
            self._not_enough_money_dialog.draw(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))

    def get_click(self, event: pygame.event.Event):
        self._confirm_purchase(event.pos)
        self._close_not_enough_money_dialog(event.pos)

    def _confirm_purchase(self, mouse_pos: typing.Tuple[int, int]):
        if self._buy_accept_dialog is None:
            return
        if self._buy_accept_dialog.accept_button.rect.collidepoint(mouse_pos):
            self._buy_accept_dialog = None
            if self._money.value < self._open_planet_index * 250:
                self._not_enough_money_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                                             (self._draw_rect.width // 2,
                                                              self._draw_rect.height // 2),
                                                             title='заработай больше!',
                                                             text='у вас не хватает денег,\n'
                                                                  'чтобы открыть эту планету', font_size=30,
                                                             info_font_size=24)
                return
            self._money.remove(self._open_planet_index * 250)
            self._planets_available[self._open_planet_index] = True
        elif self._buy_accept_dialog.reject_button.rect.collidepoint(mouse_pos):
            self._buy_accept_dialog = None

    def _close_not_enough_money_dialog(self, mouse_pos: typing.Tuple[int, int]):
        if self._not_enough_money_dialog is None:
            return
        if self._not_enough_money_dialog.accept_button.rect.collidepoint(mouse_pos) or\
                self._not_enough_money_dialog.reject_button.rect.collidepoint(mouse_pos):
            self._not_enough_money_dialog = None

    def get_planet(self, planet_index: int, map_size: typing.Tuple[int, int],
                   cell_dict: typing.Dict[CellModifierType, GenerateMod]) -> PlayerViewMap:
        self._open_planet_index = planet_index
        self._buy_planet(planet_index)
        if not self._planets_available[planet_index]:
            return None

        if self._planet_game_maps[planet_index] is None:
            game_map = PlayerViewMap(self._draw_rect, None)
            game_map.generate_map(map_size, cell_dict)
            self._planet_game_maps[planet_index] = game_map
        else:
            game_map = self._planet_game_maps[planet_index]
        return game_map

    def _buy_planet(self, planet_index: int):
        if not self._planets_available[planet_index]:
            self._buy_accept_dialog = AcceptDialog(BlueBackgroundSprite().image, (self._draw_rect.width // 2,
                                                                                  self._draw_rect.height // 2),
                                                   title='хотите открыть?',
                                                   text=f'открыть за {self._open_planet_index * 250}$?',
                                                   font_size=30, info_font_size=24)

    @property
    def draw_rect(self):
        return self._draw_rect

    @property
    def exit_button(self):
        return self._exit_button

    @property
    def planet_buttons(self):
        return self._planet_buttons
