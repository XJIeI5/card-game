import pygame
from enum import Enum
from source.ui import blit_text, Alignment


class CardType(Enum):
    Attack = pygame.Color('red')
    Defend = pygame.Color('blue')
    Weak = pygame.Color('green')
    Buff = pygame.Color('gray')


class ActionAreaType(Enum):
    SelfAction = 0
    OneEnemy = 1
    OneAlly = 2
    AllEnemies = 3
    AllAllies = 4


class Card(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, description: str, card_type: CardType,
                 action_area_type: ActionAreaType, action, sound: pygame.mixer.Sound):
        super(Card, self).__init__()
        self._width, self._height = 100, 200
        self._mini_image = pygame.transform.scale(sprite.image, (70, 70))
        self.rect = pygame.Rect((0, 0, self._width, self._height))

        self._name = name
        self._description = description
        self._card_type = card_type
        self._action_area_type = action_area_type
        self._action = action
        self._sound = sound
        self._picked = False

    def act(self, user, entity):
        self._action(user, entity)

    @property
    def image(self):
        surface = pygame.Surface((100, 200))
        start_pos = (0, 0)

        pygame.draw.rect(surface, pygame.Color(253, 244, 227), (*start_pos, self._width, self._height))
        pygame.draw.rect(surface, self._card_type.value, (*start_pos, self._width, self._height), 5)

        title = pygame.font.Font(None, 18).render(self._name, True, pygame.Color('black'))
        place = title.get_rect(center=(start_pos[0] + 50, start_pos[1] + 20))
        surface.blit(title, place)

        surface.blit(self._mini_image, (15, 40))

        blit_text(surface, pygame.Rect(5, self._mini_image.get_size()[1], *surface.get_size()),
                  self._description, 18, alignment=Alignment.Left)

        return surface

    @property
    def picked(self):
        return self._picked

    @picked.setter
    def picked(self, value):
        self._picked = value

    @property
    def action_area_type(self):
        return self._action_area_type

    @property
    def sound(self):
        return self._sound
     
    @property
    def card_type(self):
        return self._card_type

    def __str__(self):
        return self._name
