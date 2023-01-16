from source.data.sprites.primitives import BlueBackgroundSprite, GreenBackgroundSprite, RedBackgroundSprite
from source.item import Item, ItemType, Equipment, EquipmentType
from source import card_bundle


class ShellItem(Item):
    def __init__(self):
        super(ShellItem, self).__init__(BlueBackgroundSprite(), 'панцирь', 'кусок панциря', 64, ItemType.Collectable,
                                        25)


class GooItem(Item):
    def __init__(self):
        super(GooItem, self).__init__(GreenBackgroundSprite(), 'жижа', 'склязкая жижа', 2, ItemType.Collectable, 30)


class HoverSpikeItem(Equipment):
    def __init__(self):
        super(HoverSpikeItem, self).__init__(GreenBackgroundSprite(), 'шип летуна', 'шип летуна\nможет ранить врагов',
                                             EquipmentType.MainWeapon, price=75, cards=[card_bundle.RushAttack],
                                             characteristics={'attack': 3})


class HealingSerumItem(Item):
    def __init__(self):
        super(HealingSerumItem, self).__init__(RedBackgroundSprite(), 'сыворотка лечения', 'вылечит легкую травму',
                                               10, ItemType.Consumable, 75,
                                               action=lambda x: x.apply_hp(10))


class SmallPistolItem(Equipment):
    def __init__(self):
        super(SmallPistolItem, self).__init__(GreenBackgroundSprite(), 'маленький пистолет',
                                              'может проделать дырок во враге', EquipmentType.MainWeapon, price=250,
                                              cards=[card_bundle.ShootEMGAttack, card_bundle.ShootEMGAttack],
                                              characteristics={'attack': 5})
