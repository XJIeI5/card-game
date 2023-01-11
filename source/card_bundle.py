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
        super(FastPunch, self).__init__(NoneSprite(), 'Быстрый удар', 'Сносит врагу X хп', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(y.attack * 1))


class ShieldRestruct(Card):
    def __init__(self):
        super(ShieldRestruct, self).__init__(NoneSprite(), 'Пересборка', 'Подзаряжает щит на 10', CardType.Defend,
                                             ActionAreaType.SelfAction, lambda y, x: x.apply_shield(10))


class ShootAttack(Card):
    def __init__(self):
        super(ShootAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во врага и наносит ему 20 урона',
                                          CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(20))


class ShootEMGAttack(Card):
    def __init__(self):
        super(ShootEMGAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во врага и наносит ему 15 урона',
                                             CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(15))


class HealChar(Card):
    def __init__(self):
        super(HealChar, self).__init__(NoneSprite(), 'Аптечка', 'Восстанавливает выбранному персонажу'
                                       ' 20 очков здоровья', CardType.Defend, ActionAreaType.OneAlly,
                                       lambda y, x: x.apply_hp(20))


class HealAllChars(Card):
    def __init__(self):
        super(HealAllChars, self).__init__(NoneSprite(), 'Адреналин', 'Восстанавливает всем персонажам'
                                           ' 10 очков здоровья', CardType.Defend, ActionAreaType.AllAllies,
                                           lambda y, x: [x[i].apply_hp(10) for i in x])


class DamageReduce(Card):
    def __init__(self):
        super(DamageReduce, self).__init__(NoneSprite(), 'Взлом оружия', 'Взламывает оружие противников и уменьшает'
                                           ' входящий урон на 10%', CardType.Weak, ActionAreaType.AllEnemies,
                                           lambda y, x: [i.reduce_damage(0.9) for i in x])


class ShotgunAttack(Card):
    def __init__(self):
        super(ShotgunAttack, self).__init__(NoneSprite(), "Выстрел из дробовика", "Стреляет и наносит всем врагам"
                                            " 10 урона", CardType.Attack, ActionAreaType.AllEnemies, lambda y, x:
                                            [i.apply_damage(10) for i in x])