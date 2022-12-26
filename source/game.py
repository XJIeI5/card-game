import pygame
import sys
import typing
from source.game_screen import GameMapScreen


class Game:
    def __init__(self, size: typing.Tuple[int, int]):
        pygame.init()
        self._window_size = self._window_width, self._window_height = size
        self._screen = pygame.display.set_mode(size)
        self._clock = pygame.time.Clock()
        self._screen.fill(pygame.Color('black'))
        self._fps = 60

        self._game_map_screen = GameMapScreen(size)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self._game_map_screen.game_map.move_player((-1, 0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self._game_map_screen.game_map.move_player((1, 0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self._game_map_screen.game_map.move_player((0, 1))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self._game_map_screen.game_map.move_player((0, -1))
            state = pygame.key.get_pressed()
            if state[pygame.K_w]:
                self._game_map_screen.game_map.move((0, 1))
            if state[pygame.K_s]:
                self._game_map_screen.game_map.move((0, -1))
            if state[pygame.K_a]:
                self._game_map_screen.game_map.move((1, 0))
            if state[pygame.K_d]:
                self._game_map_screen.game_map.move((-1, 0))
            self._screen.fill(pygame.Color('black'))
            self._game_map_screen.game_map.draw(self._screen)

            self._clock.tick(self._fps)
            pygame.display.flip()
