import pygame


class NoneCellSprite(pygame.sprite.Sprite):
    """sprite for NoneCell type cells"""
    def __init__(self):
        super(NoneCellSprite, self).__init__()
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


class GrayBackgroundSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GrayBackgroundSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect()


class ScaledSprite(pygame.sprite.Sprite):
    def __init__(self, sprite: pygame.sprite.Sprite):
        super(ScaledSprite, self).__init__()
        self._image = sprite.image
        self.rect = self.image.get_rect()

    @property
    def image(self):
        return pygame.transform.scale(self._image, (70, 70))
