import typing
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
                 attack: int, level: int, initiative: int):
        super(InBattleEntity, self).__init__()
        self._image = sprite.image
        self._name = name
        self.rect = sprite.rect
        self._highlight_type = HighlightType.Default
        # characteristics
        self._level = level
        self._attack = attack
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
        self._is_poisoned = False

    def apply_damage(self, damage: int):
        remaining_damage = damage - self._shields
        if self._shields > 0:
            self._shields -= damage
        if remaining_damage > 0 and self._shields <= 0:
            self._hp -= remaining_damage
        if self._hp <= 0:
            self._is_dead = True
        if self._shields < 0:
            self._shields = 0
        if self._hp < 0:
            self._hp = 0

    def apply_shield(self, shield: int):
        self._shields += shield
        if self._shields > self._max_shields:
            self._shields = self._max_shields

    def apply_hp(self, hp: int):
        self._hp += hp
        if self._hp > self._max_hp:
            self._hp = self._max_hp

    def reduce_damage(self, coefficient: int):
        self._attack *= coefficient

    def extend_cards(self, cards_class: typing.List):
        """gets a list of classes inherited from Card, instances of which will be added to self._cards"""
        self._cards.extend([i() for i in cards_class])
        self.set_deck()

    def remove_cards(self, cards_class: typing.List):
        """remove instance of cards_class from self._cards"""
        to_remove = []
        for card in self._cards:
            if card.__class__ in cards_class:
                cards_class.remove(card.__class__)
                to_remove.append(card)
                if not cards_class:
                    break

        for card in to_remove:
            self._cards.remove(card)

    def set_deck(self):
        """init the good_stack and discard_stack"""
        self._good_stack = random.sample(self._cards, k=len(self._cards))
        self._discard_stack = []

    def place_cards_to_discard_stack(self):
        cards = self.get_cards()
        self._good_stack.remove(cards)
        self._discard_stack.extend(cards)

    def get_cards(self) -> typing.List[Card]:
        """return 6 cards from deck"""
        if len(self._good_stack) < 6:
            return self._good_stack[:len(self._good_stack)]
        return self._good_stack[:6]

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def initiative(self):
        return self._initiative

    @initiative.setter
    def initiative(self, value):
        self._initiative = value

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = value

    @property
    def dexterity(self):
        return self._dexterity

    @dexterity.setter
    def dexterity(self, value):
        self._dexterity = value

    @property
    def intelligence(self):
        return self._intelligence

    @intelligence.setter
    def intelligence(self, value):
        self._intelligence = value

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
        scaled_image = pygame.transform.scale(self._image, (70, 70))
        surface = pygame.Surface((scaled_image.get_size()[0] + 10, scaled_image.get_size()[1] + 50))
        pygame.draw.ellipse(surface, self._highlight_type.value,
                            (10, scaled_image.get_size()[1], scaled_image.get_size()[0], 30), 5)

        surface.blit(scaled_image, (10, 20))

        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, 50, 10))
        pygame.draw.rect(surface, pygame.Color('red'), (0, 0, 50 * (self._hp / self._max_hp) // 1, 10))

        hp = pygame.font.Font(None, 12).render(f'{self._hp}/{self._max_hp}', True, pygame.Color('black'))
        place = hp.get_rect(center=(25, 5))
        surface.blit(hp, place)

        try:
            pygame.draw.rect(surface, pygame.Color('gray'), (-1, 10, 50, 10))
            pygame.draw.rect(surface, pygame.Color('blue'), (-1, 10, 50 * (self._shields / self._max_shields) // 1, 10))

            shield = pygame.font.Font(None, 12).render(f'{self._shields}/{self._max_shields}', True,
                                                       pygame.Color('black'))
            place = shield.get_rect(center=(25, 15))
            surface.blit(shield, place)
        except ZeroDivisionError:
            pass

        return surface

    @property
    def icon(self):
        return self._image

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name

    @property
    def entity_type(self):
        return self.entity_type

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value):
        self._max_hp = value

    @property
    def shields(self):
        return self._shields

    @property
    def max_shields(self):
        return self._max_shields

    def __repr__(self):
        return f'{self.__class__.__name__} {self._name}'
