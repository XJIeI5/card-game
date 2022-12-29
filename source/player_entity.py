import pygame
from enum import Enum
from source.in_battle_entity import InBattleEntity


class MedicSpeciality:
    SkillTree = {0: ['первая помощь'], 1: ['быстрое заживление', 'детоксикация'], 2: ['нейротоксин', 'наноаптечка']}


class TankSpeciality:
    SkillTree = {0: ['стойкость'], 1: ['землетрясение', 'укрепление'], 2: ['силовое поле', 'массивный удар']}


class EngineerSpeciality:
    SkillTree = {0: ['взлом'], 1: ['подпитка', 'эми-бомба'], 2: ['перегрузка', 'разгон']}


class ShooterSpeciality:
    SkillTree = {0: ['меткий огонь'], 1: ['наводка', 'беглая стрельба'], 2: ['решето', 'прострел']}


class PlayerSpeciality(Enum):
    Medic = MedicSpeciality
    Tank = TankSpeciality
    Engineer = EngineerSpeciality
    Shooter = ShooterSpeciality


class PlayerEntity(InBattleEntity):
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_hp: int, max_shields: int,
                 attack: int, level: int, speciality: PlayerSpeciality, initiative: int):
        super(PlayerEntity, self).__init__(sprite, name, max_hp, max_shields, attack, level, initiative)

        self._speciality = speciality

    def test(self):
        print(self._speciality.value.SkillTree)

    @property
    def speciality(self):
        return self._speciality
