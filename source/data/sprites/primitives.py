import pygame


class NoneSprite(pygame.sprite.Sprite):
    """sprite for NoneCell type cells"""
    def __init__(self):
        super(NoneSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.rect = self.image.get_rect()


class EmptyCellSprite(pygame.sprite.Sprite):
    """sprite for EmptyCell type cells"""
    def __init__(self):
        super(EmptyCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((162, 162, 208)))
        self.rect = self.image.get_rect()


class EnemyCellSprite(pygame.sprite.Sprite):
    """sprite for CellWithEnemy type cells"""
    def __init__(self):
        super(EnemyCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((255, 36, 0)))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color((176, 0, 0)),
                         (self.rect.x + 25, self.rect.y + 25, self.rect.width - 100, self.rect.height - 100))


class PlayerCellSprite(pygame.sprite.Sprite):
    """sprite for CellWithEnemy type cells"""
    def __init__(self):
        super(PlayerCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((34, 139, 34)))
        self.rect = self.image.get_rect()


class NPCCellSprite(pygame.sprite.Sprite):
    """sprite for CellWithNPC type cells"""
    def __init__(self):
        super(NPCCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect()


class StartCellSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(StartCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color(197, 208, 230))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color('black'),
                         (self.rect.x + 25, self.rect.y + 25, self.rect.width - 100, self.rect.height - 100))


class NextButtonSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(NextButtonSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.rect = self.image.get_rect()
        pygame.draw.polygon(self.image, pygame.Color((162, 162, 208)),
                            [(0, 0),
                             (0, self.rect.height),
                             (self.rect.width, self.rect.height // 2)])


class PreviousButtonSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PreviousButtonSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.rect = self.image.get_rect()
        pygame.draw.polygon(self.image, pygame.Color((162, 162, 208)),
                            [(self.rect.width, 0),
                             (self.rect.width, self.rect.height),
                             (0, self.rect.height // 2)])


class BlueBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(BlueBackgroundSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((162, 162, 208)))
        self.rect = self.image.get_rect()


class GreenBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GreenBackgroundSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((34, 139, 34)))
        self.rect = self.image.get_rect()


class RedBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(RedBackgroundSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()


class GrayBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GrayBackgroundSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect()


class PlanetIconSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PlanetIconSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, pygame.Color('red'), self.rect.center, self.rect.width // 2)


class ScaledSprite(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite):
        super(ScaledSprite, self).__init__()
        self._image = sprite.image
        self.rect = self.image.get_rect()

    @property
    def image(self):
        return pygame.transform.scale(self._image, (70, 70))


class BeetleSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(BeetleSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/beetle.png')
        self.rect = self.image.get_rect()


class HoverSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(HoverSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/hover.png')
        self.rect = self.image.get_rect()


class FirstCharacterSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(FirstCharacterSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/first_character.png')
        self.rect = self.image.get_rect()


class SecondCharacterSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(SecondCharacterSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/second_character.png')
        self.rect = self.image.get_rect()


class ThirdCharacterSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(ThirdCharacterSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/third_character.png')
        self.rect = self.image.get_rect()


class ShotgunSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(ShotgunSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/shotgun.png')
        self.rect = self.image.get_rect()


class PistolSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PistolSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/pistol.png')
        self.rect = self.image.get_rect()


class HealingSerumSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(HealingSerumSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/healing_serum.png')
        self.rect = self.image.get_rect()


class HoverSpikeSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(HoverSpikeSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/hover_spike.png')
        self.rect = self.image.get_rect()


class GooSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GooSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/goo.png')
        self.rect = self.image.get_rect()


class ShellSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(ShellSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/shell.png')
        self.rect = self.image.get_rect()


class PlanetChooseSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(PlanetChooseSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/planet_choose.png')
        self.rect = self.image.get_rect()


class StoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(StoreSprite, self).__init__()
        self.image = pygame.image.load('./source/data/sprites/store.png')
        self.rect = self.image.get_rect()
