import pygame
import sys

from source.map import Map
from source.cell_types import CellType


def main():
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 100

    game_map = Map()
    game_map.load_from_txt('./source/data/map_test.txt', {' ': CellType.NoneCell, '#': CellType.EmptyCell})
    game_map.move((0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(pygame.Color('black'))
        game_map.draw(screen, pygame.Rect((10, 10, width, height)))
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
