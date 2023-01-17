from source.data.sprites import primitives
from source.item import Item, ItemType, Equipment, EquipmentType
from source import card_bundle


class ShellItem(Item):
    def __init__(self):
        super(ShellItem, self).__init__(primitives.ShellSprite(), 'панцирь', 'кусок панциря', 64,
                                        ItemType.Collectable, 25)


class GooItem(Item):
    def __init__(self):
        super(GooItem, self).__init__(primitives.GooSprite(), 'жижа', 'склязкая жижа', 2,
                                      ItemType.Collectable, 30)


class HoverSpikeItem(Equipment):
    def __init__(self):
        super(HoverSpikeItem, self).__init__(primitives.HoverSpikeSprite(), 'шип летуна',
                                             'шип летуна\nможет ранить врагов', EquipmentType.SecondaryWeapon,
                                             price=75, cards=[card_bundle.RushAttack], characteristics={'attack': 3})


class HealingSerumItem(Item):
    def __init__(self):
        super(HealingSerumItem, self).__init__(primitives.HealingSerumSprite(), 'сыворотка лечения',
                                               'вылечит легкую травму', 10, ItemType.Consumable, 75,
                                               action=lambda x: x.apply_hp(10))


class SmallPistolItem(Equipment):
    def __init__(self):
        super(SmallPistolItem, self).__init__(primitives.PistolSprite(), 'маленький пистолет',
                                              'может проделать дырок во враге', EquipmentType.MainWeapon, price=70,
                                              cards=[card_bundle.ShootEMGAttack, card_bundle.ShootEMGAttack],
                                              characteristics={'attack': 5})


class ShotgunItem(Equipment):
    def __init__(self):
        super(ShotgunItem, self).__init__(primitives.ShotgunSprite(), 'дробовик', 'из-за разброса задевает всех врагов',
                                          EquipmentType.MainWeapon, price=150, cards=[card_bundle.ShotgunAttack],
                                          characteristics={'attack': 5})
