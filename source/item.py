import pygame
import typing


class Item(pygame.sprite.Sprite):
    ItemSize = 40

    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_stack: int, current_stack: int = 0):
        super(Item, self).__init__()
        self.image = pygame.transform.scale(sprite.image, (Item.ItemSize, Item.ItemSize))
        self.rect = pygame.Rect(*sprite.rect.topleft, Item.ItemSize, Item.ItemSize)
        self._name = name
        self._max_stack = max_stack
        self._current_stack = current_stack
        self._is_full = False

    def add(self, value) -> int:
        self._current_stack += value
        if self._current_stack >= self._max_stack:
            self._is_full = True
            result = self._current_stack - self._max_stack
            self._current_stack = self._max_stack
            return result
        return 0

    def reduce(self, value):
        if self._current_stack - value < 0:
            raise ValueError('item stack can not be less than zero')
        self._current_stack -= value
        if self._is_full:
            self._is_full = False

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self.rect.x, self.rect.y = position
        screen.blit(self.image, self.rect)

        if self._current_stack == 1:
            return
        stack_text = pygame.font.Font(None, 18).render(str(self._current_stack), True, pygame.Color('white'))
        place = stack_text.get_rect(bottomright=self.rect.bottomright)
        screen.blit(stack_text, place)

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

    def __repr__(self):
        return f'{self.__class__.__name__} x{self._current_stack}'