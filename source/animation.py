import pygame
from abc import ABC

class Animator:
    translate_speed = 5.0

class Animateble(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect) -> None:
        super().__init__()
        self.rect: pygame.Rect = rect

    def translate_steps(self, pos: tuple[int, int]) -> int:
        distance = pygame.Vector2(*self.rect.center).distance_to(pos)
        return int(distance / Animator.translate_speed)

    def translate(self, pos: tuple[int, int]):
        direction = pygame.Vector2(pos[0] - self.rect.center[0], pos[1] - self.rect.center[1])
        try:
            promotion = direction.normalize() * Animator.translate_speed
        except ValueError:
            return
        new_pos = promotion + pygame.Vector2(*self.rect.center)
        self.rect.center = new_pos.xy

