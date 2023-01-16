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
        super(RushAttack, self).__init__(NoneSprite(), 'Влететь!', 'Влетает во\n врага и\nнаносит\nему 15 урона',
                                         CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(15))


class FastPunch(Card):
    def __init__(self):
        super(FastPunch, self).__init__(NoneSprite(), 'быстрый удар', 'сносит врага\nна X хп', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(y.attack * 1))


class ShieldRestruct(Card):
    def __init__(self):
        super(ShieldRestruct, self).__init__(NoneSprite(), 'Пересборка', 'Подзаряжает\nщит на 10', CardType.Defend,
                                             ActionAreaType.SelfAction, lambda y, x: x.apply_shield(10))


class ShootAttack(Card):
    def __init__(self):
        super(ShootAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во\n врага и\nнаносит\nему 20 урона',
                                          CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(20))


class ShootEMGAttack(Card):
    def __init__(self):
        super(ShootEMGAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во\nврага и\nнаносит\nему 15 урона',
                                             CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(15))


class HealSelf(Card):
    def __init__(self):
        super(HealSelf, self).__init__(NoneSprite(), 'Утяжка', 'Лечит\nсебя на\n10 очков\nздоровья', CardType.Defend,
                                       ActionAreaType.SelfAction, lambda y, x: x.apply_hp(10))


class HealChar(Card):
    def __init__(self):
        super(HealChar, self).__init__(NoneSprite(), 'Аптечка', 'Лечит\nвыбранного\n'
                                                                'персонажа на\n20 очков\nздоровья', CardType.Defend,
                                       ActionAreaType.OneAlly,
                                       lambda y, x: x.apply_hp(20))


class HealAllChars(Card):
    def __init__(self):
        super(HealAllChars, self).__init__(NoneSprite(), 'Адреналин', 'Лечит\n всех персонажей\nна 10 очков\n'
                                                                      'здоровья', CardType.Defend,
                                           ActionAreaType.AllAllies,
                                           lambda y, x: x.apply_hp(10))


class DamageReduce(Card):
    def __init__(self):
        super(DamageReduce, self).__init__(NoneSprite(), 'Взлом оружия', 'Взламывает\nоружие\nпротивников\n'
                                                                         'и уменьшает\nвходящий урон\nна 10%',
                                           CardType.Weak, ActionAreaType.AllEnemies,
                                           lambda y, x: x.reduce_damage(0.9))


class ShotgunAttack(Card):
    def __init__(self):
        super(ShotgunAttack, self).__init__(NoneSprite(), "Выстрел из дробовика", "Стреляет и\nнаносит всем\nврагам 10\n"
                                                                                  "урона",
                                            CardType.Attack, ActionAreaType.AllEnemies,
                                            lambda y, x: x.apply_damage(10))
