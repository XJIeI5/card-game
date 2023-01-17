import pygame
import typing
import os
import sys
from source.ui import Label, ContextMenu
from source.data.sprites.primitives import PlanetChooseSprite, StoreSprite, BlueBackgroundSprite


class GearSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GearSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/gear.png')
        self.rect = self.image.get_rect()


class Hub:
    def __init__(self, draw_rect: pygame.Rect):
        self._draw_rect = draw_rect
        self._is_save = False

        self._planet_choose_button = Label(PlanetChooseSprite().image, (200, 200))
        self._store_button = Label(StoreSprite().image, (200, 200))
        self._settings_button = Label(GearSprite().image, (50, 50))

        self._settings_menu: typing.Union[None, ContextMenu] = None
        self._save_button = Label(BlueBackgroundSprite().image, (0, 0), text='сохранить', font_size=30)
        self._load_button = Label(BlueBackgroundSprite().image, (0, 0), text='загрузить', font_size=30)
        self._quit_button = Label(BlueBackgroundSprite().image, (0, 0), text='выйти', font_size=30)

        self._file_choose_menu: typing.Union[None, ContextMenu] = None
        self._file_0_button = Label(BlueBackgroundSprite().image, (0, 0), text='файл 0  -  Нет', font_size=30)
        self._file_1_button = Label(BlueBackgroundSprite().image, (0, 0), text='файл 1  -  Нет', font_size=30)
        self._file_2_button = Label(BlueBackgroundSprite().image, (0, 0), text='файл 2  -  Нет', font_size=30)
        self.init_file_button()

    def init_file_button(self):
        if os.path.exists('./source/data/save/save_0'):
            self._file_0_button.set_text('файл 0  -  Есть')
        if os.path.exists('./source/data/save/save_1'):
            self._file_1_button.set_text('файл 1  -  Есть')
        if os.path.exists('./source/data/save/save_2'):
            self._file_2_button.set_text('файл 2  -  Есть')

    def draw(self, screen: pygame.Surface):
        place = self._planet_choose_button.image.get_rect(center=self._draw_rect.center)
        self._planet_choose_button.draw(screen, place.topleft)
        self._store_button.draw(screen, (0, place.y - 40))
        place = self._settings_button.image.get_rect(topright=self._draw_rect.topright)
        self._settings_button.draw(screen, place.topleft)

        if self._settings_menu is not None:
            self._settings_menu.draw(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))
        if self._file_choose_menu is not None:
            self._file_choose_menu.draw(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))

    def get_click(self, event: pygame.event.Event):
        self._open_settings(event.pos)
        self._act_settings_action(event.pos)

    def _open_settings(self, mouse_pos: typing.Tuple[int, int]):
        if not self._settings_button.rect.collidepoint(mouse_pos):
            return
        if self._file_choose_menu is not None:
            self._file_choose_menu = None
            return

        if self._settings_menu is None:
            self._settings_menu = ContextMenu(BlueBackgroundSprite().image, (self._draw_rect.width // 2, 100),
                                              [self._save_button, self._load_button, self._quit_button])
        else:
            self._settings_menu = None
            self._file_choose_menu = None

    def _act_settings_action(self, mouse_pos: typing.Tuple[int, int]):
        if self._settings_menu is None:
            return
        if self._save_button.rect.collidepoint(mouse_pos):
            self._file_choose_menu = ContextMenu(BlueBackgroundSprite().image, (self._draw_rect.width // 2, 100),
                                                 [self._file_0_button, self._file_1_button, self._file_2_button])
            self._settings_menu = None
            self._is_save = True
        if self._load_button.rect.collidepoint(mouse_pos):
            self._file_choose_menu = ContextMenu(BlueBackgroundSprite().image, (self._draw_rect.width // 2, 100),
                                                 [self._file_0_button, self._file_1_button, self._file_2_button])
            self._settings_menu = None
            self._is_save = False
        if self._quit_button.rect.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()

    @property
    def draw_rect(self):
        return self._draw_rect

    @property
    def planet_choose_button(self):
        return self._planet_choose_button

    @property
    def store_button(self):
        return self._store_button

    @property
    def settings_button(self):
        return self._settings_button

    @property
    def setting_menu(self):
        return self._settings_menu

    @property
    def file_choose_menu(self):
        return self._file_choose_menu

    @property
    def file_0_button(self):
        return self._file_0_button

    @property
    def file_1_button(self):
        return self._file_1_button

    @property
    def file_2_button(self):
        return self._file_2_button

    @property
    def is_save(self):
        return self._is_save
