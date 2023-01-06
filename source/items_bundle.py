from source.data.sprites.primitives import BlueBackgroundSprite, GreenBackgroundSprite, RedBackgroundSprite
from source.item import Item, ItemType
from source import card_bundle


class RockItem(Item):
    def __init__(self):
        super(RockItem, self).__init__(BlueBackgroundSprite(), 'камень', 64, ItemType.Collectable)


class GlassItem(Item):
    def __init__(self):
        super(GlassItem, self).__init__(GreenBackgroundSprite(), 'стекло', 2, ItemType.Collectable)


class HealingSerumItem(Item):
    def __init__(self):
        super(HealingSerumItem, self).__init__(RedBackgroundSprite(), 'сыворотка лечения', 10, ItemType.Consumable,
                                               action=lambda x: x.apply_hp(10))


class SmallPistolItem(Item):
    def __init__(self):
        super(SmallPistolItem, self).__init__(GreenBackgroundSprite(), 'маленький пистолет', 1,
                                              ItemType.Equipment.value.MainWeapon,
                                              action=lambda x: x.extend_cards([card_bundle.FastShoot] * 2),
                                              undo_action=lambda x: x.remove_cards([card_bundle.FastShoot] * 2))
