import pygame
import sys

from source.in_battle_entity import InBattleEntity
from source.battle import Battle
from source.card import Card, CardType, ActionAreaType
from source.enemies import Beetle


class Test(pygame.sprite.Sprite):
    def __init__(self):
        super(Test, self).__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color((162, 162, 208)))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color('gray'), self.rect, 5)


class FastPunch(Card):
    def __init__(self):
        super(FastPunch, self).__init__(Test(), 'быстрый удар', 'сносит врага на 1x хп', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(y.attack * 1))


class ShieldRestruct(Card):
    def __init__(self):
        super(ShieldRestruct, self).__init__(Test(), 'пересборка', 'подзарежает щит на 10', CardType.Defend,
                                             ActionAreaType.SelfAction, lambda y, x: x.apply_shield(10))


cards = [FastPunch, ShieldRestruct]


def main():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 60

    first_ent = InBattleEntity(Test(), 'abba', 50, 10, 10, 10)
    first_ent.extend_cards(cards)
    second_ent = InBattleEntity(Test(), 'beeb', 30, 50, 10, 20)
    second_ent.extend_cards(cards)
    third_ent = InBattleEntity(Test(), 'cac', 80, 0, 10, 60)
    third_ent.extend_cards(cards * 4)
    player_ent = [first_ent, second_ent, third_ent]

    entities = [Beetle(), Beetle(), Beetle()]

    battle = Battle(pygame.Rect((0, 0, width - 0, height - 0)), player_ent, entities)
    print(battle._move_order)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                battle.get_click(event.pos)
        screen.fill(pygame.Color('black'))
        battle.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
