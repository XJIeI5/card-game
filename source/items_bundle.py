from source.data.sprites.primitives import BlueBackgroundSprite, GreenBackgroundSprite, RedBackgroundSprite
from source.item import Item, ItemType, Equipment, EquipmentType
from source import card_bundle


class RockItem(Item):
    def __init__(self):
        super(RockItem, self).__init__(BlueBackgroundSprite(), 'камень', 'кусок камня', 64, ItemType.Collectable)


class GlassItem(Item):
    def __init__(self):
        super(GlassItem, self).__init__(GreenBackgroundSprite(), 'стекло', 'кусок стекла', 2, ItemType.Collectable)


class HealingSerumItem(Item):
    def __init__(self):
        super(HealingSerumItem, self).__init__(RedBackgroundSprite(), 'сыворотка лечения', 'вылечит легкую травму',
                                               10, ItemType.Consumable,
                                               action=lambda x: x.apply_hp(10))


class SmallPistolItem(Equipment):
    def __init__(self):
        super(SmallPistolItem, self).__init__(GreenBackgroundSprite(), 'маленький пистолет',
                                              'может проделать дырок во враге', EquipmentType.MainWeapon,
                                              cards=[card_bundle.FastShoot, card_bundle.FastShoot],
                                              characteristics={'attack': 5})
