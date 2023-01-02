import pygame
import typing
from source.data.sprites.primitives import PreviousButtonSprite, NextButtonSprite, BlueBackgroundSprite, \
    GrayBackgroundSprite
from source.ui import Label
from source.item import Item


class Inventory:
    def __init__(self, draw_rect: pygame.rect.Rect, rows: int, columns: int, max_pages: int):
        self._draw_rect = draw_rect
        self._rows = rows
        self._columns = columns
        self._indent = 3
        self._max_pages = max_pages
        self._current_page = 1

        self._items: typing.List[Item] = []
        self._is_full = False

        self._previous_page_button = Label(PreviousButtonSprite().image, (20, 25))
        self._next_page_button = Label(NextButtonSprite().image, (20, 25))
        self._current_page_label = Label(BlueBackgroundSprite().image, (50, 25),
                                         text=str(self._current_page),  font_size=30)

        self._item_size = (self._draw_rect.width // self._columns - self._indent,
                           self._draw_rect.height // self._rows - ((self._current_page_label.rect.height + self._indent)
                                                                   * int(self._max_pages != 1))
                           // self._rows - self._indent)

    def extend_items(self, new_items: typing.Dict[Item.__class__, int]):
        for item in self._items:
            if item.is_full:
                continue
            if new_items.get(item.__class__, None) is None:
                continue
            self._extend_to_item(item, new_items[item.__class__])
            new_items.pop(item.__class__)

        for item_class, count in new_items.items():
            self._append_to_item(item_class(), count)

    def _extend_to_item(self, item: Item, count: int):
        remains = item.add(count)

        while remains and not self._is_full:
            sprite = pygame.sprite.Sprite()
            sprite.image, sprite.rect = item.image, item.rect
            new_item = item.__class__()
            self._items.append(new_item)
            remains = new_item.add(remains)
            if len(self._items) >= (self._rows * self._columns) * self._max_pages:
                self._is_full = True

    def _append_to_item(self, item: Item, count: int):
        self._items.append(item)
        self._extend_to_item(item, count)

    def remove_item(self, item_class: Item.__class__, count: int):
        items = [i for i in self._items if isinstance(i, item_class)]
        if not items:
            raise ValueError(item_class + ' not in list')
        if sum([i.current_stack for i in items]) < count:
            raise ValueError('too much value to delete')

        while count != 0:
            count = items[-1].reduce(count)
            if not items[-1].current_stack:
                self._items.remove(items[-1])
                items = items[:-1]

    def draw(self, screen: pygame.Surface):
        start, end = (self._rows * self._columns) * (self._current_page - 1),\
                     (self._rows * self._columns) + (self._rows * self._columns) * (self._current_page - 1)
        items_to_draw = self._items[start:end]
        items_to_draw.extend([None for _ in range(self._rows * self._columns - len(items_to_draw))])
        for row in range(self._rows):
            for column in range(self._columns):
                if items_to_draw[column + row * self._columns] is None:
                    empty_label = Label(GrayBackgroundSprite().image, self._item_size)
                    empty_label.draw(screen, (self._draw_rect.x + column * (self._item_size[0] + self._indent),
                                              self._draw_rect.y + row * (self._item_size[1] + self._indent)))
                    continue
                item = items_to_draw[column + row * self._columns]
                item.scale(self._item_size)
                item.draw(screen, (self._draw_rect.x + column * (self._item_size[0] + self._indent),
                                   self._draw_rect.y + row * (self._item_size[1] + self._indent)))

        if self._max_pages != 1:
            self._draw_ui(screen)

    def _draw_ui(self, screen: pygame.Surface, indent: int = 3):
        draw_y = self._draw_rect.y + self._rows * (self._item_size[1] + indent)

        self._current_page_label.draw(screen, (self._draw_rect.width // 2 - self._current_page_label.rect.width // 2,
                                               draw_y))
        self._previous_page_button.draw(screen, (self._draw_rect.width // 2 - self._current_page_label.rect.width // 2 -
                                                 self._previous_page_button.rect.width * 1.5,
                                                 draw_y))
        self._next_page_button.draw(screen, (self._draw_rect.width // 2 + self._current_page_label.rect.width // 2 +
                                             self._next_page_button.rect.width // 2,
                                             draw_y))

    def get_click(self, mouse_pos: typing.Tuple[int, int]):
        self._switch_page(mouse_pos)

    def _switch_page(self, mouse_pos: typing.Tuple[int, int]):
        if self._next_page_button.rect.collidepoint(mouse_pos):
            self._current_page += 1 if self._current_page < self._max_pages else 0
            self._current_page_label.set_text(str(self._current_page))

        if self._previous_page_button.rect.collidepoint(mouse_pos):
            self._current_page -= 1 if self._current_page > 1 else 0
            self._current_page_label.set_text(str(self._current_page))

    @property
    def draw_rect(self):
        return self._draw_rect

    @draw_rect.setter
    def draw_rect(self, value):
        self._draw_rect = value
        self._item_size = (self._draw_rect.width // self._columns - self._indent,
                           self._draw_rect.height // self._rows - ((self._current_page_label.rect.height + self._indent)
                                                                   * int(self._max_pages != 1))
                           // self._rows - self._indent)
