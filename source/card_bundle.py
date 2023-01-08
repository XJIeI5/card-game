import pygame
import typing
from source.card import Card, CardType, ActionAreaType


class NoneSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(NoneSprite, self).__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect()


class RushAttack(Card):
    def __init__(self):
        super(RushAttack, self).__init__(NoneSprite(), 'Влететь!', 'Влетает во врага и наносит ему 10 урона',
                                         CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(10))


class FastPunch(Card):
    def __init__(self):
        super(FastPunch, self).__init__(NoneSprite(), 'быстрый удар', 'сносит врага\nна X хп', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(y.attack * 1))


class ShieldRestruct(Card):
    def __init__(self):
        super(ShieldRestruct, self).__init__(NoneSprite(), 'пересборка', 'подзарежает\nщит на 10', CardType.Defend,
                                             ActionAreaType.SelfAction, lambda y, x: x.apply_shield(10))
        
        
class FirstAid(Card):
    def __init__(self):
        super(FirstAid, self).__init__(NoneSprite(), 'первая помощь', 'лечит на 5', CardType.Buff,
                                       ActionAreaType.OneAlly, lambda y, x: x.apply_hp(5))


class FastShoot(Card):
    def __init__(self):
        super(FastShoot, self).__init__(NoneSprite(), 'беглый выстрел', 'стреляет на\n1.5X урона', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(int(y.attack * 1.5)))
