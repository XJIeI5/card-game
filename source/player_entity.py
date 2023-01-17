import pygame
import typing
import json
import os
from enum import Enum
from source.in_battle_entity import InBattleEntity
from source import skills_bundle
from source.inventory import Inventory
from source.data.sprites.primitives import ScaledSprite, FirstCharacterSprite, SecondCharacterSprite,\
    ThirdCharacterSprite
from source import items_bundle


class MedicSpeciality:
    SkillTree = {0: [skills_bundle.FirstAidSkill],
                 1: [skills_bundle.SteelSkinSkill]}


class TankSpeciality:
    SkillTree = {0: [skills_bundle.DurabilitySkill],
                 1: [skills_bundle.EarthquakeSkill]}


class EngineerSpeciality:
    SkillTree = {0: [skills_bundle.HackingSkill],
                 1: [skills_bundle.RechargeSkill]}


class ShooterSpeciality:
    SkillTree = {0: [skills_bundle.AccurateFireSkill],
                 1: [skills_bundle.AimingSkill, skills_bundle.RunawayShootingSkill],
                 2: [skills_bundle.SieveSkill, skills_bundle.PenetrationSkill]}


class PlayerSpeciality(Enum):
    Medic = MedicSpeciality
    Tank = TankSpeciality
    Engineer = EngineerSpeciality
    Shooter = ShooterSpeciality


class PlayerEntity(InBattleEntity):
    def __init__(self, index: int, name: str, max_hp: int, max_shields: int,
                 attack: int, level: int, speciality: PlayerSpeciality, initiative: int):

        self._index = index
        if index == 0:
            sprite = ScaledSprite(FirstCharacterSprite())
        elif index == 1:
            sprite = ScaledSprite(SecondCharacterSprite())
        else:
            sprite = ScaledSprite(ThirdCharacterSprite())

        super(PlayerEntity, self).__init__(sprite, name, max_hp, max_shields, attack, level, initiative)

        self._speciality = speciality
        self._skills = {}
        self._upgrade_points = 0
        self._exp = 0
        self._exp_amount_to_raise_level = [0, 5, 10, 20, 40, 60, 100]
        self._main_weapon: Inventory = Inventory(pygame.Rect(0, 0, 0, 0), 1, 1, 1)
        self._secondary_weapon: Inventory = Inventory(pygame.Rect(0, 0, 0, 0), 1, 1, 1)

        self.apply_skills()

    def apply_skills(self):
        for index, skills in self._speciality.value.SkillTree.items():
            for skill_class in skills:
                self._skills[index] = self._skills.get(index, []) + [skill_class()]
                # applying skill effects
                [i.apply_effect(self) for i in self._skills[index]]

    def save_to_json(self, directory_name: str):
        if not os.path.exists(directory_name + '/characters'):
            os.makedirs(directory_name + '/characters')
        print(self._skills)
        data = {
            'name': self._name,
            'index': self._index,
            'level': self._level,
            'exp': self._exp,
            'upgrade_points': self._upgrade_points,
            'attack': self._attack,
            'initiative': self._initiative,
            'strength': self._strength,
            'dexterity': self._dexterity,
            'intelligence': self._intelligence,
            'max_hp': self._max_hp,
            'hp': self._hp,
            'max_shields': self._max_shields,
            'shields': self._shields,
            'is_dead': self._is_dead,
            'main_weapon': self._main_weapon.items[0].__class__.__name__ if self._main_weapon.items else None,
            'secondary_weapon': self._secondary_weapon.items[0].__class__.__name__ if
            self._secondary_weapon.items else None,
            'speciality': self._speciality.value.__name__,
            'skills': {i: {skill.__class__.__name__: skill.current_level for skill in j}
                       for i, j in self._skills.items()}
        }
        with open(directory_name + f'/characters/character_{self._index}.json', mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, directory_name: str):
        file_name = directory_name + f'/characters/character_{self._index}.json'
        with open(file_name, mode='r', encoding='utf-8') as file:
            data = json.load(file)

        self._name = data['name']
        self._level = data['level']
        self._exp = data['exp']
        self._upgrade_points = data['upgrade_points']
        self._attack = data['attack']
        self._initiative = data['initiative']
        self._strength = data['strength']
        self._dexterity = data['dexterity']
        self._intelligence = data['intelligence']
        self._max_hp = data['max_hp']
        self._hp = data['hp']
        self._max_shields = data['max_shields']
        self._shields = data['shields']
        self._is_dead = data['is_dead']
        self._main_weapon = Inventory(pygame.Rect(0, 0, 0, 0), 1, 1, 1)
        if data['main_weapon']:
            self._main_weapon.extend_items({getattr(items_bundle, data['main_weapon']): 1})
        self._secondary_weapon = Inventory(pygame.Rect(0, 0, 0, 0), 1, 1, 1)
        if data['secondary_weapon']:
            self._secondary_weapon.extend_items({getattr(items_bundle, data['secondary_weapon']): 1})
        self._speciality = PlayerSpeciality.Medic if data['speciality'] == 'MedicSpeciality' else\
            PlayerSpeciality.Tank if data['speciality'] == 'TankSpeciality' else\
                PlayerSpeciality.Engineer if data['speciality'] == 'EngineerSpeciality' else\
                    PlayerSpeciality.Shooter
        for index, skills in data['skills'].items():
            line = []
            for skill_name in skills:
                skill = getattr(skills_bundle, skill_name)()
                [skill.level_up() for _ in range(skill.current_level)]
                line.append(skill)
            self._skills[index] = line

    def get_exp(self, exp_amount):
        self._exp += exp_amount
        if self._exp >= self._exp_amount_to_raise_level[self._level]:
            self._exp = self._exp - self._exp_amount_to_raise_level[self._level]
            self._level += 1
            self._upgrade_points += 1

    @property
    def speciality(self):
        return self._speciality

    @property
    def skills(self):
        return self._skills

    @property
    def upgrade_points(self):
        return self._upgrade_points

    @upgrade_points.setter
    def upgrade_points(self, value):
        self._upgrade_points = value

    @property
    def exp(self):
        return self._exp

    @property
    def exp_amount_to_raise_level(self):
        return self._exp_amount_to_raise_level

    @property
    def main_weapon(self):
        return self._main_weapon

    @property
    def secondary_weapon(self):
        return self._secondary_weapon
