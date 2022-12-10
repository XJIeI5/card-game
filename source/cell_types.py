from enum import Enum

import pygame


class CellType(Enum):
    NoneCell = pygame.Color('black')  # background color
    EmptyCell = pygame.Color(162, 162, 208)
    CellWithEnemy = pygame.Color('red')
    CellWithNPC = pygame.Color(106, 90, 205)
