import pygame
import sys

from source.game import Game


def main():
    game = Game((800, 800))
    game.run()


if __name__ == '__main__':
    main()
