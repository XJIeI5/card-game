import pygame
import random
import typing
from source.in_battle_entity import InBattleEntity
from source.item import Item
from source.player_entity import PlayerEntity


class Enemy(InBattleEntity):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_hp: int, max_shields: int,
                 attack: int, level: int, initiative: int, loot: typing.List[Item]):
        super(Enemy, self).__init__(sprite, name, max_hp, max_shields, attack, level, initiative)
        self._loot = loot

    def get_loot(self) -> Item:
        return random.choice(self._loot)

    def act(self, player_player_entities: typing.List[PlayerEntity]):
        pass
