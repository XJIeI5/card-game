import pygame
import typing
from source.inventory import Inventory
from source.ui import ContextMenu, AcceptDialog, Label
from source.item import Item, ItemType
from source.data.sprites.primitives import BlueBackgroundSprite, GrayBackgroundSprite, GreenBackgroundSprite
from source import items_bundle


class Money:
    def __init__(self, value: int):
        self._value = value

    def append(self, count: int):
        self._value += count

    def remove(self, count: int):
        self._value -= count

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class ItemMenageMenu(ContextMenu):
    def __init__(self, is_seller_item: bool):
        self._buy_button = Label(BlueBackgroundSprite().image, (0, 0), text='купить', font_size=20) if is_seller_item \
            else None
        self._sell_button = None if is_seller_item \
            else Label(BlueBackgroundSprite().image, (0, 0), text='продать', font_size=20)
        self._info_button = Label(BlueBackgroundSprite().image, (0, 0), text='инфо', font_size=20)

        super(ItemMenageMenu, self).__init__(GrayBackgroundSprite().image, (90, 30),
                                             [self._buy_button, self._sell_button, self._info_button])

    @property
    def info_button(self):
        return self._info_button

    @property
    def buy_button(self):
        return self._buy_button

    @property
    def sell_button(self):
        return self._sell_button


class Store:
    def __init__(self, draw_rect: pygame.Rect, rows: int, columns: int, pages: int, money: Money):
        self._draw_rect = draw_rect
        self._indent = 25
        self._money = money

        self._buy_label = Label(GreenBackgroundSprite().image, (self._draw_rect.width // 2 - self._indent, 30),
                                text='КУПИТЬ', font_size=36)
        self._seller_inventory = Inventory(pygame.Rect(0,
                                                       self._draw_rect.height - draw_rect.height // 2,
                                                       draw_rect.width // 2 - self._indent,
                                                       draw_rect.height // 2 - self._indent),
                                           rows, columns, pages)
        self._seller_inventory.extend_items({items_bundle.HealingSerumItem: 15, items_bundle.SmallPistolItem: 3})
        self._sell_label = Label(GreenBackgroundSprite().image, (self._draw_rect.width // 2 - self._indent, 30),
                                 text='ПРОДАТЬ', font_size=36)
        self._player_inventory = Inventory(pygame.Rect(self._seller_inventory.draw_rect.width + self._indent * 2,
                                                       self._draw_rect.height - draw_rect.height // 2,
                                                       draw_rect.width // 2 - self._indent,
                                                       draw_rect.height // 2 - self._indent),
                                           rows, columns, pages)
        self._exit_button = Label(GrayBackgroundSprite().image, (40, 30), text='выйти', font_size=18)

        self._info_dialog: typing.Union[None, AcceptDialog] = None
        self._accept_dialog: typing.Union[None, AcceptDialog] = None

        self._acting_item: typing.Union[None, Item] = None
        self._buying_item: typing.Union[None, Item] = None
        self._selling_item: typing.Union[None, Item] = None
        self._acting_item_menu: typing.Union[None, ItemMenageMenu] = None
        self._context_menu_pos: typing.Tuple[int, int] = (0, 0)

    def draw(self, screen: pygame.Surface):
        self._draw_inventory(screen)
        self._draw_top_panel(screen)

        if self._acting_item is not None:
            self._acting_item_menu.draw(screen, self._context_menu_pos)

        if self._info_dialog is not None:
            self._info_dialog.draw(screen, (self._draw_rect.width // 4,
                                            self._draw_rect.height // 4 - self._info_dialog.rect.height // 4))

        if self._accept_dialog is not None:
            self._accept_dialog.draw(screen, (self._draw_rect.width // 4,
                                              self._draw_rect.height // 4 - self._accept_dialog.rect.height // 4))

    def _draw_inventory(self, screen: pygame.Surface):
        self._seller_inventory.draw(screen)
        self._buy_label.draw(screen, (0,
                                      self._seller_inventory.draw_rect.height - self._indent))
        self._player_inventory.draw(screen)
        self._sell_label.draw(screen, (self._seller_inventory.draw_rect.width + self._indent * 2,
                                       self._player_inventory.draw_rect.height - self._indent))

    def _draw_top_panel(self, screen: pygame.Surface):
        Label(BlueBackgroundSprite().image, (self._draw_rect.width, 30)).draw(screen, (0, 0))
        Label(GrayBackgroundSprite().image, (self._draw_rect.width // 4, 30),
              text=f'{self._money.value}$', font_size=30).draw(screen, (0, 0))
        self._exit_button.draw(screen, (self._draw_rect.width - self._exit_button.rect.width, 0))

    def get_click(self, event: pygame.event.Event):
        if not self._seller_inventory.draw_rect.collidepoint(event.pos) and \
                not self._player_inventory.draw_rect.collidepoint(event.pos):
            self._acting_item = None
        self._act_with_seller_items(event.pos)
        self._act_with_player_items(event.pos)
        self._seller_inventory.get_click(event)
        self._player_inventory.get_click(event)
        self._set_item_info_menu(event.pos)
        self._buy_item(event.pos)
        self._sell_item(event.pos)

    def _act_with_seller_items(self, mouse_pos: typing.Tuple[int, int]):
        if self._acting_item is not None:
            result = self._process_action_clicks(mouse_pos)
            if result:
                self._acting_item = None
                self._acting_item_menu = None
                return
        item_pos = self._seller_inventory.get_cell(mouse_pos)
        if item_pos is None or item_pos[1] + item_pos[0] * self._seller_inventory.columns >= \
                len(self._seller_inventory.items):
            return
        self._acting_item = self._seller_inventory.items[item_pos[1] + item_pos[0] * self._seller_inventory.columns]
        self._acting_item_menu = ItemMenageMenu(is_seller_item=True)
        self._context_menu_pos = mouse_pos

    def _act_with_player_items(self, mouse_pos: typing.Tuple[int, int]):
        if self._acting_item is not None:
            result = self._process_action_clicks(mouse_pos)
            if result:
                self._acting_item = None
                self._acting_item_menu = None
                return
        item_pos = self._player_inventory.get_cell(mouse_pos)
        if item_pos is None or item_pos[1] + item_pos[0] * self._player_inventory.columns >= \
                len(self._player_inventory.items):
            return
        self._acting_item = self._player_inventory.items[item_pos[1] + item_pos[0] * self._player_inventory.columns]
        self._acting_item_menu = ItemMenageMenu(is_seller_item=False)
        self._context_menu_pos = mouse_pos

    def _process_action_clicks(self, mouse_pos: typing.Tuple[int, int]) -> bool:
        if self._acting_item_menu.info_button.rect.collidepoint(mouse_pos):
            self._info_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                             (self._draw_rect.width // 2, self._draw_rect.height // 1.5),
                                             'информация', self._acting_item.description, font_size=28,
                                             info_font_size=24)
            return True
        if self._acting_item_menu.buy_button and self._acting_item_menu.buy_button.rect.collidepoint(mouse_pos):
            self._buying_item = self._acting_item
            self._accept_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                               (self._draw_rect.width // 2, self._draw_rect.height // 2),
                                               title='вы уверены?!',
                                               text=f'вы точно хотите купить это за {self._acting_item.price}?',
                                               font_size=28, info_font_size=28)
            return True
        if self._acting_item_menu.sell_button and self._acting_item_menu.sell_button.rect.collidepoint(mouse_pos):
            self._selling_item = self._acting_item
            self._accept_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                               (self._draw_rect.width // 2, self._draw_rect.height // 2),
                                               title='вы уверены?!',
                                               text=f'вы точно хотите продать это за'
                                                    f' {int(self._selling_item.price * 0.9)}?',
                                               font_size=28, info_font_size=28)
            return True

        return False

    def _set_item_info_menu(self, mouse_pos: typing.Tuple[int, int]):
        if self._info_dialog and \
                (self._info_dialog.accept_button.rect.collidepoint(mouse_pos) or
                 self._info_dialog.reject_button.rect.collidepoint(mouse_pos)):
            self._info_dialog = None
            return

    def _buy_item(self, mouse_pos: typing.Tuple[int, int]):
        if self._buying_item is None or self._accept_dialog is None:
            return

        if self._accept_dialog.reject_button.rect.collidepoint(mouse_pos):
            self._buying_item = None
            self._accept_dialog = None
            return

        if self._accept_dialog.accept_button.rect.collidepoint(mouse_pos):
            price = self._buying_item.price
            if price > self._money.value:
                self._accept_dialog = None
                self._buying_item = None
                self._info_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                                 (self._draw_rect.width // 2, self._draw_rect.height // 1.5),
                                                 'информация', 'у вас недосаточно денег!', font_size=28,
                                                 info_font_size=24)
                return
            self._seller_inventory.remove_item(self._buying_item, 1)
            self._player_inventory.extend_items({self._buying_item.__class__: 1})
            self._money.remove(price)
            self._accept_dialog = None
            self._buying_item = None

    def _sell_item(self, mouse_pos: typing.Tuple[int, int]):
        if self._selling_item is None or self._accept_dialog is None:
            return

        if self._accept_dialog.reject_button.rect.collidepoint(mouse_pos):
            self._selling_item = None
            self._accept_dialog = None
            return

        if self._accept_dialog.accept_button.rect.collidepoint(mouse_pos):
            self._player_inventory.remove_item(self._selling_item, 1)
            self._seller_inventory.extend_items({self._selling_item.__class__: 1})
            self._money.append(int(self._selling_item.price * 0.9))
            self._accept_dialog = None
            self._selling_item = None

    @property
    def draw_rect(self):
        return self._draw_rect

    @property
    def exit_button(self):
        return self._exit_button
