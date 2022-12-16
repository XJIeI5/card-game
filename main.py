import pygame
import sys

from source.game_map import GameMap
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType


def main():
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('black'))
    fps = 100

    game_map = PlayerViewMap(pygame.Rect((50, 50, width - 100, height - 100)), None)
    # game_map.load_from_txt('./source/data/map_test.txt', {' ': None, '#': CellModifierType.EmptyCell})
    cell_dict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                 CellModifierType.EnemyCell: GenerateMod(GenerateModType.Count, 1)}
    game_map.generate_map((50, 50), cell_dict)
    # print(game_map._player_position)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                game_map.move_player((-1, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                game_map.move_player((1, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                game_map.move_player((0, 1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_map.move_player((0, -1))
        state = pygame.key.get_pressed()
        if state[pygame.K_w]:
            game_map.move((0, 1))
        if state[pygame.K_s]:
            game_map.move((0, -1))
        if state[pygame.K_a]:
            game_map.move((1, 0))
        if state[pygame.K_d]:
            game_map.move((-1, 0))
        screen.fill(pygame.Color('black'))
        game_map.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
