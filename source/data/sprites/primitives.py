import pygame


class NoneCellSprite(pygame.sprite.Sprite):
    """sprite for NoneCell type cells"""
    def __init__(self):
        super(NoneCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect()


class EmptyCellSprite(pygame.sprite.Sprite):
    """sprite for EmptyCell type cells"""
    def __init__(self):
        super(EmptyCellSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color(162, 162, 208))
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
