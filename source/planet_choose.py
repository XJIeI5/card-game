import os
import pygame
import typing
import math
import random
from source.ui import Label
from source.data.sprites.primitives import PlanetIconSprite, BlueBackgroundSprite
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod


class PlanetChoose:
    def __init__(self, draw_rect: pygame.Rect):
        self._draw_rect = draw_rect
        self._planet_buttons: typing.List[Label] = [Label(PlanetIconSprite().image, (50, 50),
                                                          text=str(i + 1), font_size=36, color=pygame.Color('black'))
                                                    for i in range(3)]
        self._planet_game_maps: typing.Dict[int, typing.Union[None, PlayerViewMap]] =\
            {i: None for i in range(len(self._planet_buttons))}

        self._exit_button = Label(BlueBackgroundSprite().image, (40, 30), text='Назад')
        self.place_planet_buttons(100)

    def place_planet_buttons(self, radius: int):
        for index, place_button in enumerate(self._planet_buttons):
            angle = random.randint(0, 360)
            x, y = math.cos(angle), math.sin(angle)
            place_button.rect.center = (radius * (index + 1) * x + self._draw_rect.width // 2,
                                        radius * (index + 1) * y + self._draw_rect.height // 2)

    def save_maps(self, directory_name: str):
        if not os.path.exists(directory_name + '/maps'):
            os.makedirs(directory_name + '/maps')

        for index, game_map in self._planet_game_maps.items():
            file_name = directory_name + f'/maps/map_{index}.txt'
            if game_map is None:
                open(file_name, mode='w').close()
            else:
                game_map.save_to_txt(file_name)

    def load_maps(self, directory_name: str):
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

    def get_planet(self, planet_index: int, map_size: typing.Tuple[int, int],
                   cell_dict: typing.Dict[CellModifierType, GenerateMod]) -> PlayerViewMap:
        if self._planet_game_maps[planet_index] is None:
            game_map = PlayerViewMap(self._draw_rect, None)
            game_map.generate_map(map_size, cell_dict)
            self._planet_game_maps[planet_index] = game_map
        else:
            game_map = self._planet_game_maps[planet_index]
        return game_map

    @property
    def draw_rect(self):
        return self._draw_rect

    @property
    def exit_button(self):
        return self._exit_button

    @property
    def planet_buttons(self):
        return self._planet_buttons