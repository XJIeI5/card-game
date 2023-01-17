import pygame
import typing
import random
from source.player_entity import PlayerEntity
from source.in_battle_entity import InBattleEntity
from source import card_bundle
from source import items_bundle
from source.card import CardType
from source.data.sprites.primitives import ScaledSprite, BeetleSprite, HoverSprite
from source.enemy import Enemy


class Beetle(Enemy):
    def __init__(self, level: int):
        cards = [card_bundle.RushAttack] * 3
        super(Beetle, self).__init__(ScaledSprite(BeetleSprite()), 'жук', 10, 15, 10, level, 10,
                                     [items_bundle.ShellItem])
        self.extend_cards(cards)

    def act(self, player_entities: typing.List[InBattleEntity]) -> None:
        card = random.choice(self._cards)
        player_entities = [i for i in player_entities if not i.is_dead]
        if len(player_entities) <= 0:
            return
        if len(player_entities) > 1:
            player_entity = random.choice(player_entities)
        else:
            player_entity = player_entities[0]
        card.act(self, player_entity)
        print('hurted', player_entity, 'by 10')


class Hover(Enemy):
    def __init__(self, level: int):
        cards = [card_bundle.HealSelf, card_bundle.RushAttack, card_bundle.RushAttack]
        super(Hover, self).__init__(ScaledSprite(HoverSprite()), 'летун', 25, 5, 8, level, 5,
                                    [items_bundle.GooItem, items_bundle.HoverSpikeItem])
        self.extend_cards(cards)

    def act(self, player_entities: typing.List[PlayerEntity]):
        cards_to_act = self._cards
        if self._hp >= self._max_hp * 0.8:
            cards_to_act = [i for i in cards_to_act if i.card_type != CardType.Defend]
        card = random.choice(cards_to_act)
        player_entities = [i for i in player_entities if not i.is_dead]
        if len(player_entities) <= 0:
            return
        player_entity = sorted(player_entities, key=lambda x: x.hp)[0]
        card.act(self, player_entity)
