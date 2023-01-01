from source.data.sprites.primitives import BlueBackgroundSprite, GreenBackgroundSprite
from source.item import Item


class RockItem(Item):
    def __init__(self):
        super(RockItem, self).__init__(BlueBackgroundSprite(), 'камень', 64)


class GlassItem(Item):
    def __init__(self):
        super(GlassItem, self).__init__(GreenBackgroundSprite(), 'стекло', 2)
