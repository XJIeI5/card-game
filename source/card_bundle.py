import pygame
from source.card import Card, CardType, ActionAreaType


class NoneSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(NoneSprite, self).__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect()


class RushAttack(Card):
    def __init__(self):
        super(RushAttack, self).__init__(NoneSprite(), 'Влететь!', 'Влетает во\nврага и\nнаносит\nему 15 урона',
                                         CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(15),
                                         pygame.mixer.Sound("data/sounds/punch.wav"))


class FastPunch(Card):
    def __init__(self):
        super(FastPunch, self).__init__(NoneSprite(), 'быстрый удар', 'сносит врага\nна атаку\nперсонажа', CardType.Attack,
                                        ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(y.attack * 1),
                                        pygame.mixer.Sound("data/sounds/punch.wav"))


class ShieldRestruct(Card):
    def __init__(self):
        super(ShieldRestruct, self).__init__(NoneSprite(), 'Пересборка', 'Подзаряжает\nщит на 10', CardType.Defend,
                                             ActionAreaType.SelfAction, lambda y, x: x.apply_shield(10),
                                             pygame.mixer.Sound("data/sounds/shield_restruct.wav"))


class ShieldIncrease(Card):
    def __init__(self):
        super(ShieldIncrease, self).__init__(NoneSprite(), 'Восполнение', 'Подзаряжает\nщит\nсоюзника\nна 10',
                                             CardType.Defend, ActionAreaType.OneAlly, lambda y, x: x.apply_shield(10))


class ShootAttack(Card):
    def __init__(self):
        super(ShootAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во\nврага и\nнаносит\nему 20 урона',
                                          CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(20),
                                          pygame.mixer.Sound("data/sounds/rifle-shot.wav"))


class ShootEMGAttack(Card):
    def __init__(self):
        super(ShootEMGAttack, self).__init__(NoneSprite(), 'Выстрел', 'Стреляет во\nврага и\nнаносит\nему 15 урона',
                                             CardType.Attack, ActionAreaType.OneEnemy, lambda y, x: x.apply_damage(15),
                                             pygame.mixer.Sound("data/sounds/emg-shot.wav"))


class HealSelf(Card):
    def __init__(self):
        super(HealSelf, self).__init__(NoneSprite(), 'Утяжка', 'Лечит\nсебя на\n10 очков\nздоровья', CardType.Defend,
                                       ActionAreaType.SelfAction, lambda y, x: x.apply_hp(10))


class HealChar(Card):
    def __init__(self):
        super(HealChar, self).__init__(NoneSprite(), 'Аптечка', 'Лечит\nвыбранного\n'
                                                                'персонажа на\n20 очков\nздоровья', CardType.Defend,
                                       ActionAreaType.OneAlly,
                                       lambda y, x: x.apply_hp(20), pygame.mixer.Sound("data/sounds/heal.wav"))


class HealAllChars(Card):
    def __init__(self):
        super(HealAllChars, self).__init__(NoneSprite(), 'Адреналин', 'Лечит\nвсех\nсоюзников\nна 10 очков\n'
                                                                      'здоровья', CardType.Defend,
                                           ActionAreaType.AllAllies,
                                           lambda y, x: x.apply_hp(10), pygame.mixer.Sound("data/sounds/heal.wav"))


class DamageReduce(Card):
    def __init__(self):
        super(DamageReduce, self).__init__(NoneSprite(), 'Взлом оружия', 'Взламывает\nоружие\nпротивников\n'
                                                                         'и уменьшает\nего урон\nна 10%',
                                           CardType.Weak, ActionAreaType.AllEnemies,
                                           lambda y, x: x.reduce_damage(0.9),
                                           pygame.mixer.Sound("data/sounds/shield_restruct.wav"))


class ShotgunAttack(Card):
    def __init__(self):
        super(ShotgunAttack, self).__init__(NoneSprite(), "Выстрел Дроби", "Стреляет и\nнаносит всем\nврагам 10\n"
                                                                                  "урона",
                                            CardType.Attack, ActionAreaType.AllEnemies,
                                            lambda y, x: x.apply_damage(10),
                                            pygame.mixer.Sound("data/sounds/shotgun-shot.wav"))


class EarthquakeAttack(Card):
    def __init__(self):
        super(EarthquakeAttack, self).__init__(NoneSprite(), 'Землетрясение', 'наносит всем\nврагам 5\nурона',
                                               CardType.Attack, ActionAreaType.AllEnemies,
                                               lambda y, x: x.apply_damage(5),
                                               pygame.mixer.Sound("data/sounds/punch.wav"))
