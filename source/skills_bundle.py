from source.skill import Skill
from source.card_bundle import HealChar, ShieldIncrease, ShieldRestruct, EarthquakeAttack, DamageReduce


class FirstAidSkill(Skill):
    def __init__(self):
        level_effects = [lambda y: y.extend_cards([HealChar]),
                         lambda y: y.extend_cards([HealChar]),
                         lambda y: setattr(y, 'attack', y.attack + 10)]
        description = {1: 'добавляет карту Первая помощь\n(лечит 5 здоровья)',
                       2: 'добавляет карту Первая помощь\n(лечит 5 здоровья)',
                       3: 'повышает урон на 10'}
        super(FirstAidSkill, self).__init__('первая помощь', 3, level_effects, description, current_level=1)


class SteelSkinSkill(Skill):
    def __init__(self):
        level_effects = [lambda y: setattr(y, 'max_hp', y.max_hp + 5),
                         lambda y: setattr(y, 'max_hp', y.max_hp + 5),
                         lambda y: setattr(y, 'max_hp', y.max_hp + 10)]
        description = {0: 'увеличивает максимальное здоровье на 5',
                       1: 'увеличивает максимальное здоровье на 5',
                       2: 'увеличивает максимальное здоровье на 10'}
        super(SteelSkinSkill, self).__init__('стальная кожа', 3, level_effects, description, current_level=0)


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
        level_effects = [lambda y: y.extend_cards([ShieldIncrease]),
                         lambda y: y.extend_cards([ShieldIncrease])]
        description = {0: 'дает карту, которая восполняет щит союзника на 10',
                       1: 'дает карту, которая восполняет щит союзника на 10'}
        super(DurabilitySkill, self).__init__('стойкость', 2, level_effects, description, current_level=0)


class EarthquakeSkill(Skill):
    def __init__(self):
        level_effects = [lambda y: y.extend_cards([EarthquakeAttack]),
                         lambda y: y.extend_cards([EarthquakeAttack])]
        description = {0: 'дает карту, которая наносит всем врагам 5 урона',
                       1: 'дает карту, которая наносит всем врагам 5 урона'}
        super(EarthquakeSkill, self).__init__('землетрясение', 2, level_effects, description, current_level=0)


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
        level_effects = [lambda y: y.extend_cards([DamageReduce]),
                         lambda y: y.extend_cards([DamageReduce])]
        description = {0: 'дает карту, которая уменьшает урон вражеской атаки',
                       1: 'дает карту, которая уменьшает урон вражеской атаки'}
        super(HackingSkill, self).__init__('взлом', 2, level_effects, description, current_level=0)


class RechargeSkill(Skill):
    def __init__(self):
        level_effects = [lambda y: y.extend_cards([ShieldRestruct]),
                         lambda y: y.extend_cards([ShieldIncrease])]
        description = {0: 'дает карту, которая восполняет щит на 10',
                       1: 'дает карту, которая восполняет щит на 10'}
        super(RechargeSkill, self).__init__('подпитка', 2, level_effects, description, current_level=0)


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
