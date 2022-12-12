import pygame
import sys

from source.map import Map
from source.cell import CellType
from source.generate_mod import GenerateMod, GenerateModType
from source.triangulation import get_lines_from_triangulation


def main():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 60

    game_map = Map(50, 50, CellType.NoneCell)
    # game_map.load_from_txt('./source/data/map_test.txt', {' ': CellType.NoneCell, '#': CellType.EmptyCell})
    game_map.generate_map({CellType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                           CellType.CellWithNPC: GenerateMod(GenerateModType.Count, 3),
                           CellType.CellWithEnemy: GenerateMod(GenerateModType.Probability, 50)})
    map_pos = [0, 0]
    game_map.move((0, 0))
    game_map.draw(screen, pygame.Rect((50, 50, width - 100, height - 100)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        state = pygame.key.get_pressed()
        if state[pygame.K_w]:
            map_pos[1] += 1
        if state[pygame.K_s]:
            map_pos[1] -= 1
        if state[pygame.K_a]:
            map_pos[0] += 1
        if state[pygame.K_d]:
            map_pos[0] -= 1
        game_map.move(map_pos)
        # screen.fill(pygame.Color('black'))
        # game_map.draw(screen, pygame.Rect((50, 50, width - 100, height - 100)))
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
