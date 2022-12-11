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


class CellWithEnemySprite(pygame.sprite.Sprite):
    """sprite for CellWithEnemy type cells"""
    def __init__(self):
        super(CellWithEnemySprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color((255, 36, 0)))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, pygame.Color((176, 0, 0)),
                           (self.rect.width // 2 - 10, self.rect.height // 2 - 10), 200)


class CellWithNPCSprite(pygame.sprite.Sprite):
    """sprite for CellWithNPC type cells"""
    def __init__(self):
        super(CellWithNPCSprite, self).__init__()
        self.image = pygame.Surface((500, 500))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect()
