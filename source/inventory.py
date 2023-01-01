import pygame
import typing
from source.data.sprites.primitives import BlueBackgroundSprite, GrayBackgroundSprite
from source.ui import Label
from source.item import Item


class Inventory:
    def __init__(self, draw_rect: pygame.rect.Rect, rows: int, columns: int, max_pages: int):
        self._draw_rect = draw_rect
        self._rows = rows
        self._columns = columns
        self._max_pages = max_pages
        self._current_page = 0

        self._items: typing.List[Item] = []
        self._is_full = False

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

    def draw(self, screen: pygame.Surface):
        indent = 3
        start, end = (self._rows * self._columns) * self._current_page,\
                     (self._rows * self._columns) + (self._rows * self._columns) * self._current_page
        items_to_draw = self._items[start:end]
        items_to_draw.extend([None for _ in range(self._rows * self._columns - len(items_to_draw))])
        for row in range(self._rows):
            for column in range(self._columns):
                if items_to_draw[column + row * self._rows] is None:
                    empty_label = Label(GrayBackgroundSprite().image, (Item.ItemSize, Item.ItemSize))
                    empty_label.draw(screen, (self._draw_rect.x + column * (Item.ItemSize + indent),
                                              self._draw_rect.y + row * (Item.ItemSize + indent)))
                    continue
                items_to_draw[column + row * self._rows].draw(screen,
                                                              (self._draw_rect.x + column * (Item.ItemSize + indent),
                                                               self._draw_rect.y + row * (Item.ItemSize + indent)))

    @property
    def draw_rect(self):
        return self._draw_rect

    @draw_rect.setter
    def draw_rect(self, value):
        self._draw_rect = value
