from source.data.sprites.primitives import BlueBackgroundSprite, GreenBackgroundSprite, RedBackgroundSprite
from source.item import Item, ItemType, Equipment, EquipmentType
from source import card_bundle


class RockItem(Item):
    def __init__(self):
        super(RockItem, self).__init__(BlueBackgroundSprite(), 'камень', 'кусок камня', 64, ItemType.Collectable, 200)


class GlassItem(Item):
    def __init__(self):
        super(GlassItem, self).__init__(GreenBackgroundSprite(), 'стекло', 'кусок стекла', 2, ItemType.Collectable, 100)


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
