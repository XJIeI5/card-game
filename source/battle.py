import pygame
import typing


class Battle:
    def __init__(self, draw_rect: pygame.rect.Rect, player_entities: list, enemy_entities: list):
        self._draw_rect = draw_rect

        self._player_entities = player_entities
        self._enemy_entities = enemy_entities

        self._move_order = {}
        self._current_acting_entity = None

        self._current_cards = []
        self._picked_card = None

        self.init_move_order()
        self.init_turn()

    def init_move_order(self) -> None:
        order = sorted(self._player_entities + self._enemy_entities, key=lambda x: x.initiative)[::-1]
        for i in range(len(order) - 1):
            self._move_order[order[i]] = order[i + 1]

    def init_turn(self) -> None:
        if self._current_acting_entity is None:
            self._current_acting_entity = sorted(self._player_entities + self._enemy_entities,
                                                 key=lambda x: x.initiative)[::-1][0]
        else:
            self._current_acting_entity = self._move_order[self._current_acting_entity]

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        start_x, start_y = self._draw_rect.width // (len(self._player_entities) + 1),\
                           self._draw_rect.height // (len(self._player_entities) + 1)
        offset_x, offset_y = -25, start_y
        # player
        for i, entity in enumerate(self._player_entities):
            entity.rect.center = self._draw_rect.x + start_x + entity.rect.width // 4 * -i // 2,\
                                 self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)
        # enemy
        start_x, start_y = self._draw_rect.width // (len(self._enemy_entities) + 1),\
                           self._draw_rect.height // (len(self._enemy_entities) + 1)
        offset_x, offset_y = -25, start_y
        for i, entity in enumerate(self._enemy_entities):
            entity.rect.center = self._draw_rect.x + self._draw_rect.width - start_x - entity.rect.width / 4 * -i // 2,\
                                    self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)

        # cards
        if self._current_acting_entity in self._player_entities:
            self._current_cards = self._current_acting_entity.cards
            for i, card in enumerate(self._current_acting_entity.cards):
                start_pos = self._draw_rect.x + card.rect.width * i + card.rect.width // 2,\
                            self._draw_rect.height - card.rect.height / 2
                card.rect.center = start_pos
                if card.picked:
                    card.rect.center = self._draw_rect.center
                surface.blit(card.image, card.rect)
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def pick_card(self, mouse_pos: typing.Tuple[int, int]) -> None:
        for card in self._current_cards:
            if card.rect.collidepoint(mouse_pos):
                card.picked = not card.picked
                if self._picked_card and card.picked:
                    card.picked = False
                    return
                if self._picked_card and not card.picked:
                    self._picked_card = None
                    return
                self._picked_card = card
