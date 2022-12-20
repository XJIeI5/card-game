import pygame
from source.card import Card


class InBattleEntity(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_hp: int, max_shields: int, initiative: int):
        super(InBattleEntity, self).__init__()
        self._image = sprite.image
        self._name = name
        self.rect = sprite.rect
        # characteristics
        self._initiative = initiative
        self._strength = 0
        self._dexterity = 0
        self._intelligence = 0

        self._equipment = []

        self._cards: list[Card] = []

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

    def extend_cards(self, cards: list[Card]):
        self._cards.extend(cards)

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
    def image(self):
        surface = pygame.Surface((self._image.get_size()[0] + 10, self._image.get_size()[1] + 10))

        surface.blit(self._image, (10, 10))

        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, 50, 10))
        pygame.draw.rect(surface, pygame.Color('red'), (0, 0, 50 * (self._hp / self._max_hp) // 1, 10))

        try:
            pygame.draw.rect(surface, pygame.Color('gray'), (-1, 10, 50, 10))
            pygame.draw.rect(surface, pygame.Color('blue'), (-1, 10, 50 * (self._shields / self._max_shields) // 1, 10))
        except ZeroDivisionError:
            pass

        return surface

    def __repr__(self):
        return f'{self.__class__.__name__} {self._name}'
