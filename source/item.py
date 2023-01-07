import pygame
import typing
from enum import Enum
from source.card import Card


class EquipmentType(Enum):
    MainWeapon = 0
    SecondaryWeapon = 1


class ItemType(Enum):
    Collectable = 0
    Consumable = 1
    Equipment = 2


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_stack: int, item_type: ItemType,
                 current_stack: int = 0, action=None, undo_action=None):
        super(Item, self).__init__()
        self.image = sprite.image
        self.rect = self.image.get_rect()
        self._name = name
        self._max_stack = max_stack
        self._current_stack = current_stack
        self._item_type = item_type
        self._action = action
        self._undo_action = undo_action
        self._is_full = False

    def add(self, value) -> int:
        self._current_stack += value
        if self._current_stack >= self._max_stack:
            self._is_full = True
            result = self._current_stack - self._max_stack
            self._current_stack = self._max_stack
            return result
        return 0

    def reduce(self, value) -> int:
        self._current_stack -= value
        if self._current_stack != self._max_stack:
            self._is_full = False
        if self._current_stack < 0:
            result = abs(self._current_stack)
            self._current_stack = 0
            return result
        return 0

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self.rect.x, self.rect.y = position
        screen.blit(self.image, self.rect)

        if self._current_stack == 1:
            return
        stack_text = pygame.font.Font(None, 18).render(str(self._current_stack), True, pygame.Color('white'))
        place = stack_text.get_rect(bottomright=self.rect.bottomright)
        screen.blit(stack_text, place)

    def scale(self, new_size: typing.Tuple[int, int]):
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()

    @property
    def name(self):
        return self._name

    @property
    def max_stack(self):
        return self._max_stack

    @property
    def current_stack(self):
        return self._current_stack

    @property
    def is_full(self):
        return self._is_full

    @property
    def item_type(self):
        return self._item_type

    @property
    def action(self):
        return self._action

    @property
    def undo_action(self):
        return self._undo_action

    def __repr__(self):
        return f'{self.__class__.__name__} x{self._current_stack}'


class Equipment(Item):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, equipment_type: EquipmentType,
                 cards: typing.List[Card.__class__], characteristics: typing.Dict[str, int], current_stack: int = 0):
        super(Equipment, self).__init__(sprite, name, 1, ItemType.Equipment, current_stack)
        self._equipment_type = equipment_type
        self._cards = cards
        self._characteristics = characteristics

    @property
    def action(self):
        actions = [lambda x: x.extend_cards([self._cards])]
        for key, value in self._characteristics:
            actions.append(lambda x: setattr(x, key, getattr(x, key) + value))
        return lambda x: [action(x) for action in actions]

    @property
    def undo_action(self):
        actions = [lambda x: x.remove_cards([self._cards])]
        for key, value in self._characteristics:
            actions.append(lambda x: setattr(x, key, getattr(x, key) - value))
        return lambda x: [action(x) for action in actions]

    @property
    def cards(self):
        return self._cards

    @property
    def characteristics(self):
        return self._characteristics

    @property
    def equipment_type(self):
        return self._equipment_type
