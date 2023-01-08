from source.skill import Skill
from source.card_bundle import FirstAid


class FirstAidSkill(Skill):
    def __init__(self):
        level_effects = [lambda y: y.extend_cards([FirstAid]),
                         lambda y: y.extend_cards([FirstAid]),
                         lambda y: setattr(y, 'attack', y.attack + 10)]
        description = {1: 'добавляет карту Первая помощь\n(лечит 5 здоровья)',
                       2: 'добавляет карту Первая помощь\n(лечит 5 здоровья)',
                       3: 'повышает урон на 10'}
        super(FirstAidSkill, self).__init__('первая помощь', 3, level_effects, description, current_level=1)


class RapidHealingSkill(Skill):
    def __init__(self):
        level_effects = []
        super(RapidHealingSkill, self).__init__('быстрое заживление', 0, level_effects, {})


class DetoxificationSkill(Skill):
    def __init__(self):
        level_effects = []
        super(DetoxificationSkill, self).__init__('детоксикация', 0, level_effects, {})


class NeurotoxinSkill(Skill):
    def __init__(self):
        level_effects = []
        super(NeurotoxinSkill, self).__init__('нейротоксин', 0, level_effects, {})


class NanoFirstAid(Skill):
    def __init__(self):
        level_effects = []
        super(NanoFirstAid, self).__init__('нано аптечка', 0, level_effects, {})


class DurabilitySkill(Skill):
    def __init__(self):
        level_effects = []
        super(DurabilitySkill, self).__init__('стойкость', 0, level_effects, {})


class EarthquakeSkill(Skill):
    def __init__(self):
        level_effects = []
        super(EarthquakeSkill, self).__init__('землетрясение', 0, level_effects, {})


class StrengtheningSkill(Skill):
    def __init__(self):
        level_effects = []
        super(StrengtheningSkill, self).__init__('укрепление', 0, level_effects, {})


class ForceFieldSkill(Skill):
    def __init__(self):
        level_effects = []
        super(ForceFieldSkill, self).__init__('силовое поле', 0, level_effects, {})


class MassiveImpactSkill(Skill):
    def __init__(self):
        level_effects = []
        super(MassiveImpactSkill, self).__init__('массивный удар', 0, level_effects, {})


class HackingSkill(Skill):
    def __init__(self):
        level_effects = []
        super(HackingSkill, self).__init__('взлом', 0, level_effects, {})


class RechargeSkill(Skill):
    def __init__(self):
        level_effects = []
        super(RechargeSkill, self).__init__('подпитка', 0, level_effects, {})


class AmyBombSkill(Skill):
    def __init__(self):
        level_effects = []
        super(AmyBombSkill, self).__init__('эми-бомба', 0, level_effects, {})


class OverloadSkill(Skill):
    def __init__(self):
        level_effects = []
        super(OverloadSkill, self).__init__('перегрузка', 0, level_effects, {})


class AccelerationSkill(Skill):
    def __init__(self):
        level_effects = []
        super(AccelerationSkill, self).__init__('разгон', 0, level_effects, {})


class AccurateFireSkill(Skill):
    def __init__(self):
        level_effects = []
        super(AccurateFireSkill, self).__init__('меткий огонь', 0, level_effects, {})


class AimingSkill(Skill):
    def __init__(self):
        level_effects = []
        super(AimingSkill, self).__init__('наводка', 0, level_effects, {})


class RunawayShootingSkill(Skill):
    def __init__(self):
        level_effects = []
        super(RunawayShootingSkill, self).__init__('беглая стрельба', 0, level_effects, {})


class SieveSkill(Skill):
    def __init__(self):
        level_effects = []
        super(SieveSkill, self).__init__('решето', 0, level_effects, {})


class PenetrationSkill(Skill):
    def __init__(self):
        level_effects = []
        super(PenetrationSkill, self).__init__('прострел', 0, level_effects, {})
