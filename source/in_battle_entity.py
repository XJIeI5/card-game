from enum import Enum
import pygame
import random
from source.card import Card


class HighlightType(Enum):
    Default = pygame.Color('yellow')
    CurrentActingEntity = pygame.Color('white')
    CanBeChosen = pygame.Color('blue')


class InBattleEntity(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_hp: int, max_shields: int,
                 initiative: int):
        super(InBattleEntity, self).__init__()
        self._image = sprite.image
        self._name = name
        self.rect = sprite.rect
        self._highlight_type = HighlightType.Default
        # characteristics
        self._initiative = initiative
        self._strength = 0
        self._dexterity = 0
        self._intelligence = 0

        self._equipment = []

        self._cards: list[Card] = []   # a list of all cards in general
        self._good_stack: list[Card] = []   # a stack of cards to be placed in the hand
        self._discard_stack: list[Card] = []  # a stack of cards that were in the hand

        self._max_hp = max_hp
        self._hp = max_hp
        self._max_shields = max_shields
        self._shields = max_shields
        self._is_dead = False

    def apply_damage(self, damage: int):
        remaining_damage = damage - self._shields
        self._shields -= damage
        self._hp -= remaining_damage
        if self._hp <= 0:
            self._is_dead = True

    def apply_shield(self, shield: int):
        self._shields += shield

    def extend_cards(self, cards: list):
        """gets a list of classes inherited from Card, instances of which will be added to self._cards"""
        self._cards.extend([i() for i in cards])
        self.set_deck()

    def set_deck(self):
        """init the good_stack and discard_stack"""
        self._good_stack = random.sample(self._cards, k=len(self._cards))
        self._discard_stack = []

    def place_cards_to_discard_stack(self):
        cards = self.get_cards()
        self._good_stack.remove(cards)
        self._discard_stack.extend(cards)

    def get_cards(self) -> list[Card]:
        """return 6 cards from deck"""
        if len(self._good_stack) < 6:
            return self._good_stack[:len(self._good_stack)]
        return self._good_stack[:6]

    @property
    def initiative(self):
        return self._initiative

    @property
    def strength(self):
        return self._strength

    @property
    def dexterity(self):
        return self._dexterity

    @property
    def intelligence(self):
        return self._intelligence

    @property
    def cards(self):
        return self._cards

    @property
    def is_dead(self):
        return self._is_dead

    @property
    def highlight_type(self):
        return self._highlight_type

    @highlight_type.setter
    def highlight_type(self, value):
        self._highlight_type = value

    @property
    def image(self):
        surface = pygame.Surface((self._image.get_size()[0] + 10, self._image.get_size()[1] + 40))
        pygame.draw.ellipse(surface, self._highlight_type.value,
                            (10, self._image.get_size()[1], self._image.get_size()[0], 30), 5)

        surface.blit(self._image, (10, 10))

        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, 50, 10))
        pygame.draw.rect(surface, pygame.Color('red'), (0, 0, 50 * (self._hp / self._max_hp) // 1, 10))

        try:
            pygame.draw.rect(surface, pygame.Color('gray'), (-1, 10, 50, 10))
            pygame.draw.rect(surface, pygame.Color('blue'), (-1, 10, 50 * (self._shields / self._max_shields) // 1, 10))
        except ZeroDivisionError:
            pass

        return surface

    @property
    def icon(self):
        return self._image

    def __repr__(self):
        return f'{self.__class__.__name__} {self._name}'
