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
        self._planet_game_maps = {i: None for i in range(len(self._planet_buttons))}

        self._exit_button = Label(BlueBackgroundSprite().image, (40, 30), text='Назад')
        self.place_planet_buttons(100)

    def place_planet_buttons(self, radius: int):
        for index, place_button in enumerate(self._planet_buttons):
            place_button.rect.center = (radius * (index + 1) * math.cos(random.randint(0, 360))
                                        + self._draw_rect.width // 2,
                                        radius * (index + 1) * math.sin(random.randint(0, 360))
                                        + self._draw_rect.height // 2)

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
