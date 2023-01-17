import pygame
import typing
from source.card import ActionAreaType
from source.in_battle_entity import InBattleEntity, HighlightType
from source.player_entity import PlayerEntity
from card_bundle import RushAttack
from source.ui import AcceptDialog
from source.data.sprites.primitives import GrayBackgroundSprite
from source.inventory import Inventory


class Battle:
    def __init__(self, draw_rect: pygame.rect.Rect, player_entities: list, enemy_entities: list, inventory: Inventory):
        self._draw_rect = draw_rect

        self._player_entities = player_entities
        self._enemy_entities = enemy_entities
        self._inventory = inventory

        self._move_order = {}
        self._current_acting_entity: typing.Union[None, InBattleEntity] = None

        self._current_cards = []
        self._picked_card = None

        self._is_win = False
        self._private_is_win = False
        self._is_lose = False

        self._loot_show_dialog: typing.Union[None, AcceptDialog] = None

        self.apply_equipment_effects()
        self.init_move_order()
        self.next_action()

    def apply_equipment_effects(self):
        for character in self._player_entities:
            if character.main_weapon.items:
                character.main_weapon.items[0].action(character)
            if character.secondary_weapon.items:
                character.secondary_weapon.items[0].action(character)

    def init_move_order(self) -> None:
        order = sorted(self._player_entities + self._enemy_entities, key=lambda x: x.initiative)[::-1]
        for i in range(len(order) - 1):
            self._move_order[order[i]] = order[i + 1]

    def get_first_entity(self):
        return sorted(self._player_entities + self._enemy_entities,
                      key=lambda x: x.initiative)[::-1][0]

    def next_action(self) -> None:
        if all([i.is_dead for i in self._player_entities]):
            self.lose_battle()
            return

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
            self.play_card_sound(RushAttack.sound)
            self.next_action()
            pygame.time.wait(100)

    def reset_picked_card(self) -> None:
        if self._picked_card:
            self._picked_card.picked = False
            self._picked_card = None

    def draw(self, screen: pygame.Surface) -> None:
        surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height))

        self.draw_player(surface)
        self.draw_enemies(surface)
        self.draw_cards(surface)
        self.draw_action_order(surface)
        if self._loot_show_dialog is not None:
            self._loot_show_dialog.draw(surface, (self._draw_rect.width // 4, self._draw_rect.height // 4))

        screen.blit(surface, (self._draw_rect.x, self._draw_rect.y))

    def draw_player(self, surface: pygame.Surface) -> None:
        start_x, start_y = self._draw_rect.width // (len(self._player_entities) + 1), \
                           self._draw_rect.height // (len(self._player_entities) + 1)
        offset_x, offset_y = -25, (self._draw_rect.height - 200) // (len(self._player_entities) + 1)
        for i, entity in enumerate(self._player_entities):
            entity.rect.center = self._draw_rect.x + start_x + entity.rect.width // 4 * -i // 2, \
                                 self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)

    def draw_enemies(self, surface: pygame.Surface) -> None:
        start_x, start_y = self._draw_rect.width // 4, \
                           self._draw_rect.height // (len(self._enemy_entities) + 1)
        offset_x, offset_y = -25, (self._draw_rect.height - 200) // (len(self._enemy_entities) + 1)
        for i, entity in enumerate(self._enemy_entities):
            entity.rect.center = self._draw_rect.x + self._draw_rect.width - start_x - entity.rect.width / 4 * -i // 2,\
                                 self._draw_rect.y + start_y + offset_y * i
            surface.blit(entity.image, entity.rect)

    def draw_cards(self, surface: pygame.Surface) -> None:
        if self._current_acting_entity in self._player_entities:
            self._current_cards = self._current_acting_entity.get_cards()
            for i, card in enumerate(self._current_acting_entity.get_cards()):
                start_pos = self._draw_rect.x + card.rect.width * i + card.rect.width // 2, \
                            self._draw_rect.height - card.rect.height / 2
                card.rect.center = start_pos
                if card.picked:
                    card.rect.center = self._draw_rect.center
                surface.blit(card.image, card.rect)

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
        self.pick_up_loot(mouse_pos)
        if self._picked_card:
            self.play_card_sound(self._picked_card.sound)
            # Self
            if self._picked_card.action_area_type == ActionAreaType.SelfAction:
                if self._current_acting_entity.rect.collidepoint(mouse_pos):
                    self._picked_card.act(self._current_acting_entity, self._current_acting_entity)
                    self.next_action()
            # OneEnemy
            elif self._picked_card.action_area_type == ActionAreaType.OneEnemy:
                for enemy in self._enemy_entities:
                    if enemy.rect.collidepoint(mouse_pos) and not enemy.is_dead:
                        self._picked_card.act(self._current_acting_entity, enemy)
                        # gain exp to character
                        if enemy.is_dead and isinstance(self._current_acting_entity, PlayerEntity):
                            self._current_acting_entity.get_exp(enemy.level)
                        self.next_action()
                        break
            # OneAlly
            elif self._picked_card.action_area_type == ActionAreaType.OneAlly:
                for ally in self._player_entities:
                    if ally.rect.collidepoint(mouse_pos) and not ally.is_dead:
                        self._picked_card.act(self._current_acting_entity, ally)
                        self.next_action()
                        break
            # AllEnemies
            elif self._picked_card.action_area_type == ActionAreaType.AllEnemies:
                for enemy in self._enemy_entities:
                    if enemy.rect.collidepoint(mouse_pos) and not enemy.is_dead:
                        for act_enemy in self._enemy_entities:
                            self._picked_card.act(self._current_acting_entity, act_enemy)
                            # gain exp to character
                            if enemy.is_dead and isinstance(self._current_acting_entity, PlayerEntity):
                                self._current_acting_entity.get_exp(enemy.level)
                        self.next_action()
                        break
            # AllAllies
            elif self._picked_card.action_area_type == ActionAreaType.AllAllies:
                for ally in self._player_entities:
                    if ally.rect.collidepoint(mouse_pos) and not ally.is_dead:
                        for act_ally in self._player_entities:
                            self._picked_card.act(self._current_acting_entity, act_ally)
                        self.next_action()
                        break
            if all([i.is_dead for i in self._enemy_entities]):
                self.win_battle()

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

    def pick_up_loot(self, mouse_pos: typing.Tuple[int, int]):
        if self._loot_show_dialog is not None and\
            (self._loot_show_dialog.accept_button.rect.collidepoint(mouse_pos) or
             self._loot_show_dialog.reject_button.rect.collidepoint(mouse_pos)):
            self._is_win = self._private_is_win
            self._loot_show_dialog = None

    def win_battle(self):
        self._undo_equipment_effects()
        self._private_is_win = True
        loot = [i.get_loot() for i in self._enemy_entities]
        images = [i().image for i in loot]
        self._loot_show_dialog = AcceptDialog(GrayBackgroundSprite().image, (self._draw_rect.width // 2,
                                                                             self._draw_rect.height // 2),
                                              'лут с врагов!', 'вы нашли:', font_size=30, info_font_size=24,
                                              images=images)
        new_items = {}
        for item_class in loot:
            new_items[item_class] = new_items.get(item_class, 0) + 1
        self._inventory.extend_items(new_items)

    def lose_battle(self):
        self._is_lose = True

    def _undo_equipment_effects(self):
        for character in self._player_entities:
            if character.main_weapon.items:
                character.main_weapon.items[0].undo_action(character)
            if character.secondary_weapon.items:
                character.secondary_weapon.items[0].undo_action(character)

    @property
    def is_win(self):
        return self._is_win

    @property
    def is_lose(self):
        return self._is_lose

    def play_card_sound(self, sound):
        sound.play()
