import pygame
import sys

from source.game_map import GameMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType


def main():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 1

    game_map = GameMap(pygame.Rect((50, 50, width - 100, height - 100)), None)
    # game_map.load_from_txt('./source/data/map_test.txt', {' ': None, '#': CellModifierType.EmptyCell})
    cell_dict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                 CellModifierType.EnemyCell: GenerateMod(GenerateModType.Count, 1)}
    game_map.generate_map((50, 50), cell_dict)
    # print(*game_map.cells, sep='\n', end='\n\n')
    map_pos = [0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # player_on_map.set_path(game_map.get_cell(event.pos))
                pass
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
        # game_map.move_entities()
        # print(*game_map.cells, sep='\n', end='\n\n')
        screen.fill(pygame.Color('black'))
        game_map.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
