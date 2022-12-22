import pygame
import typing
import random
from source.in_battle_entity import InBattleEntity
from source import card_bundle


class BeetleSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(BeetleSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/cacodemon.png')
        self.rect = self.image.get_rect()


class Beetle(InBattleEntity):
    def __init__(self):
        cards = [card_bundle.RushAttack] * 3
        super(Beetle, self).__init__(BeetleSprite(), 'жук', 10, 15, 10, 10)
        self.extend_cards(cards)

    def act(self, player_entities: list[InBattleEntity]) -> None:
        card = random.choice(self._cards)
        player_entity = random.choice(player_entities)
        card.act(self, player_entity)
        print('YRY')
