import pygame
from enum import Enum
from source.in_battle_entity import InBattleEntity
from source import skills_bundle


class MedicSpeciality:
    SkillTree = {0: [skills_bundle.FirstAidSkill],
                 1: [skills_bundle.RapidHealingSkill, skills_bundle.DetoxificationSkill],
                 2: [skills_bundle.NeurotoxinSkill, skills_bundle.DetoxificationSkill]}


class TankSpeciality:
    SkillTree = {0: [skills_bundle.DurabilitySkill],
                 1: [skills_bundle.EarthquakeSkill, skills_bundle.StrengtheningSkill],
                 2: [skills_bundle.ForceFieldSkill, skills_bundle.MassiveImpactSkill]}


class EngineerSpeciality:
    SkillTree = {0: [skills_bundle.HackingSkill],
                 1: [skills_bundle.RechargeSkill, skills_bundle.AmyBombSkill],
                 2: [skills_bundle.OverloadSkill, skills_bundle.AccelerationSkill]}


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
    def __init__(self, sprite: pygame.sprite.Sprite, name: str, max_hp: int, max_shields: int,
                 attack: int, level: int, speciality: PlayerSpeciality, initiative: int):
        super(PlayerEntity, self).__init__(sprite, name, max_hp, max_shields, attack, level, initiative)

        self._speciality = speciality
        self._skills = {}
        for index, skills in self._speciality.value.SkillTree.items():
            for skill_class in skills:
                self._skills[index] = self._skills.get(index, []) + [skill_class()]
                # applying skill effects
                [i.apply_effect(self) for i in self._skills[index]]

    @property
    def speciality(self):
        return self._speciality

    @property
    def skills(self):
        return self._skills
