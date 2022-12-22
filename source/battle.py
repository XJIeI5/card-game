import pygame
import typing
from source.card import ActionAreaType
from source.in_battle_entity import InBattleEntity, HighlightType


class Battle:
    def __init__(self, draw_rect: pygame.rect.Rect, player_entities: list, enemy_entities: list):
        self._draw_rect = draw_rect

        self._player_entities = player_entities
        self._enemy_entities = enemy_entities

        self._move_order = {}
        self._current_acting_entity: typing.Union[None, InBattleEntity] = None

        self._current_cards = []
        self._picked_card = None

        self.init_move_order()
        self.next_action()

    def init_move_order(self) -> None:
        order = sorted(self._player_entities + self._enemy_entities, key=lambda x: x.initiative)[::-1]
        for i in range(len(order) - 1):
            self._move_order[order[i]] = order[i + 1]

    def get_first_entity(self):
        return sorted(self._player_entities + self._enemy_entities,
                                                 key=lambda x: x.initiative)[::-1][0]

    def next_action(self) -> None:
        self.reset_picked_card()
        if self._current_acting_entity is None:
            self._current_acting_entity = self.get_first_entity()
        else:
            # set the default highlight to the previous entity
            self._current_acting_entity.highlight_type = HighlightType.Default

            try:
                self._current_acting_entity = self._move_order[self._current_acting_entity]
            except KeyError:
                self._current_acting_entity = self.get_first_entity()

        if self._current_acting_entity.is_dead:
            self.next_action()
        # set the acting highlight to the current entity
        self._current_acting_entity.highlight_type = HighlightType.CurrentActingEntity

        if self._current_acting_entity in self._enemy_entities:
            self._current_acting_entity.act(self._player_entities)
            self.next_action()
            pygame.time.wait(100)

    def reset_picked_card(self) -> None:
        if self._picked_card:
            self._picked_card.picked = False
            self._picked_card = None

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))
        start_x, start_y = self._draw_rect.width // (len(self._player_entities) + 1), \
                           self._draw_rect.height // (len(self._player_entities) + 1)
        offset_x, offset_y = -25, start_y
        # player
        for i, entity in enumerate(self._player_entities):
            entity.rect.center = self._draw_rect.x + start_x + entity.rect.width // 4 * -i // 2, \
                                 self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)
        # enemy
        start_x, start_y = self._draw_rect.width // (len(self._enemy_entities) + 1), \
                           self._draw_rect.height // (len(self._enemy_entities) + 1)
        offset_x, offset_y = -25, start_y
        for i, entity in enumerate(self._enemy_entities):
            entity.rect.center = self._draw_rect.x + self._draw_rect.width - start_x - entity.rect.width / 4 * -i // 2, \
                                 self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)

        # cards
        if self._current_acting_entity in self._player_entities:
            self._current_cards = self._current_acting_entity.get_cards()
            for i, card in enumerate(self._current_acting_entity.get_cards()):
                start_pos = self._draw_rect.x + card.rect.width * i + card.rect.width // 2, \
                            self._draw_rect.height - card.rect.height / 2
                card.rect.center = start_pos
                if card.picked:
                    card.rect.center = self._draw_rect.center
                surface.blit(card.image, card.rect)

        # action order
        self.draw_action_order(surface)
        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def draw_action_order(self, surface: pygame.Surface) -> None:
        cell_size = 50
        current_entity = self._current_acting_entity
        for i in range(5):
            image = pygame.transform.scale(current_entity.icon, (cell_size, cell_size))
            if current_entity.is_dead:  # crossing out the dead entities
                pygame.draw.line(image, pygame.Color('red'), (0, 0), (cell_size, cell_size), 3)
                pygame.draw.line(image, pygame.Color('red'), (0, cell_size), (cell_size, 0), 3)

            pygame.draw.rect(surface, pygame.Color('green'),
                             (self._draw_rect.width - (cell_size * 5 - cell_size * i) - i - 2, 0,
                              self._draw_rect.width - (cell_size * 5 - cell_size * i) - i - 2 + cell_size,
                              cell_size + 2), 2)
            surface.blit(image, (self._draw_rect.width - (cell_size * 5 - cell_size * i) - i, 0))
            # getting next current_entity
            try:
                current_entity = self._move_order[current_entity]
            except KeyError:
                current_entity = self.get_first_entity()

    def get_click(self, mouse_pos: typing.Tuple[int, int]) -> None:
        self.pick_card(mouse_pos)
        if self._picked_card:
            if self._picked_card.action_area_type == ActionAreaType.SelfAction:
                if self._current_acting_entity.rect.collidepoint(mouse_pos):
                    self._picked_card.act(self._current_acting_entity)
                    self.next_action()
            elif self._picked_card.action_area_type == ActionAreaType.OneEnemy:
                for enemy in self._enemy_entities:
                    if enemy.rect.collidepoint(mouse_pos) and not enemy.is_dead:
                        self._picked_card.act(enemy)
                        self.next_action()
                        break

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
