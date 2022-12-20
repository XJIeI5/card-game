import pygame
import sys

from source.in_battle_entity import InBattleEntity
from source.battle import Battle
from source.card import Card, CardType


class Test(pygame.sprite.Sprite):
    def __init__(self):
        super(Test, self).__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color((162, 162, 208)))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color('gray'), self.rect, 5)


cards = [Card(Test(), 'fast punch', 'beat enemy on 10 hp', CardType.Attack, lambda x: x.apply_damage(10)),
         Card(Test(), 'shield restruct', 'restore 10 shields', CardType.Defend, lambda x: x.apply_shield(10))]


def main():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 60

    first_ent = InBattleEntity(Test(), 'abba', 50, 10, 10)
    second_ent = InBattleEntity(Test(), 'beeb', 30, 50, 20)
    third_ent = InBattleEntity(Test(), 'cac', 80, 0, 60)
    third_ent.extend_cards(cards)
    player_ent = [first_ent, second_ent, third_ent]
    entities = [InBattleEntity(Test(), 'juk', 10, 10, 10), InBattleEntity(Test(), 'kuk', 20, 20, 20), InBattleEntity(Test(), 'ruk', 30, 30, 30)]
    battle = Battle(pygame.Rect((0, 0, width - 0, height - 0)), player_ent, entities + [InBattleEntity(Test(), 'chuk', 50, 50, 50)])
    print(battle._move_order)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                battle.pick_card(event.pos)
        screen.fill(pygame.Color('black'))
        battle.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
