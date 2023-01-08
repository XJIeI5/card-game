import pygame
import typing
from source.ui import Label, AcceptDialog, ContextMenu, Alignment
from source.data.sprites.primitives import NextButtonSprite, PreviousButtonSprite, BlueBackgroundSprite, \
    GrayBackgroundSprite
from source.skill import Skill
from source.inventory import Inventory
from source.item import Item, ItemType, Equipment, EquipmentType


class ItemMenageMenu(ContextMenu):
    def __init__(self, item: Item):
        self._throw_button = Label(BlueBackgroundSprite().image, (0, 0), text='выкинуть', font_size=20)
        self._use_button = None if item.item_type != ItemType.Consumable else\
            Label(BlueBackgroundSprite().image, (0, 0), text='использовать', font_size=20)
        self._equip_button = None if item.item_type != ItemType.Equipment else\
            Label(BlueBackgroundSprite().image, (0, 0), text='экипировать', font_size=20)

        super(ItemMenageMenu, self).__init__(GrayBackgroundSprite().image, (90, 30),
                                             [self._throw_button, self._use_button, self._equip_button])

    @property
    def use_button(self):
        return self._use_button

    @property
    def equip_button(self):
        return self._equip_button

    @property
    def throw_button(self):
        return self._throw_button


class PalmtopUI:
    def __init__(self, draw_rect: pygame.Rect, player_entities: typing.List, inventory: Inventory):

        self._draw_rect = draw_rect
        self._drawing_screen: typing.Union[None, pygame.Surface] = None

        self._player_entities = player_entities
        self._current_player_entity = player_entities[0]

        image = pygame.Surface((100, 100))
        image.fill(pygame.Color('blue'))
        self._exit_button = Label(image, (40, 30), text='карта', font_size=18)
        self._next_player_button = Label(NextButtonSprite().image, (30, 27))
        self._previous_player_button = Label(PreviousButtonSprite().image, (30, 27))
        self._character_name_label = Label(BlueBackgroundSprite().image, (200, 30),
                                           text=self._current_player_entity.name, font_size=24)
        self._character_icon_label = Label(self._current_player_entity.icon,
                                           (self._character_name_label.rect.width,
                                            self._character_name_label.rect.width))
        self._accept_skill_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                                 (self._draw_rect.width // 2, self._draw_rect.height // 2),
                                                 title='Вы уверены?!', font_size=28, info_font_size=28)
        self._info_dialog: typing.Union[None, AcceptDialog] = None

        self._picked_skill: typing.Union[None, Skill] = None
        self._inventory = inventory

        self._acting_item: typing.Union[None, Item] = None
        self._acting_item_menu: typing.Union[None, ItemMenageMenu] = None
        self._context_menu_pos: typing.Tuple[int, int] = (0, 0)

    def draw(self, screen: pygame.Surface):
        indent = 25

        self._draw_character_switcher(screen, (self._draw_rect.center[0] * 1.5 - indent, 0))
        # draw character
        self._character_icon_label.draw(screen, (self._character_name_label.rect.x, self._character_name_label.rect.y +
                                                 self._character_name_label.rect.height + indent))

        self._draw_character_skill_tree(screen, (0, 0))

        self._exit_button.draw(screen, (self._draw_rect.width - self._exit_button.rect.width, 0))

        self._draw_inventory(screen, (0, self._draw_rect.height // 2 - 5))
        self._draw_character_equipment(screen, (self._draw_rect.width // 2 + indent, self._draw_rect.height // 2 - 5))

        self._draw_exp_progress_bar(screen,
                                    (self._character_name_label.rect.x,
                                     self._character_name_label.rect.width + self._character_name_label.rect.height +
                                     indent + 5))

        if self._picked_skill:
            self._draw_accept_dialog_box(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))

        if self._acting_item is not None:
            self._acting_item_menu.draw(screen, self._context_menu_pos)

        if self._info_dialog is not None:
            self._info_dialog.draw(screen, (self._draw_rect.width // 4,
                                            self._draw_rect.height // 4 - self._accept_skill_dialog.rect.height // 4))

    def _draw_character_switcher(self, screen: pygame.Surface, center: typing.Tuple[int, int], indent=25):
        self._character_name_label.draw(screen, (center[0] - self._character_name_label.rect.width // 2, center[1]))
        self._previous_player_button.draw(screen, (center[0] - self._character_name_label.rect.width // 2 - indent -
                                                   self._previous_player_button.rect.width, center[1]))
        self._next_player_button.draw(screen, (center[0] + self._character_name_label.rect.width // 2 + indent,
                                               center[1]))

    def _draw_character_skill_tree(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        surface = pygame.Surface((screen.get_size()[0] // 2, screen.get_size()[1] // 3 - 30))
        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, *surface.get_size()), 3)
        skill_tree: dict = self._current_player_entity.skills
        cols = [indent, surface.get_size()[0] // 2]
        for list_index, skills in enumerate(skill_tree.values()):
            for skill_index, skill in enumerate(skills):
                draw_rect = pygame.Rect(cols[skill_index], indent + indent * list_index
                                        + skill.rect.height * list_index, surface.get_size()[0] // 2 - indent * 2, 30)
                skill.draw(surface, draw_rect)
        screen.blit(surface, position)

        # upgrade points
        upgrade_points = pygame.font.Font(None, 36).render(
            f'осталось {self._current_player_entity.upgrade_points} улучшений', True, pygame.Color('white'))
        screen.blit(upgrade_points, (position[0] + 5, position[1] + surface.get_size()[1] + 10))

    def _draw_accept_dialog_box(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self._accept_skill_dialog.set_text(self._picked_skill.description[self._picked_skill.current_level + 1])
        self._accept_skill_dialog.draw(screen, position)

    def _draw_exp_progress_bar(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        pygame.draw.rect(screen, pygame.Color('gray'), (position[0], position[1],
                                                        self._character_name_label.rect.width, 10))
        one_piece = self._character_name_label.rect.width // \
                    self._current_player_entity.exp_amount_to_raise_level[self._current_player_entity.level]
        pygame.draw.rect(screen, pygame.Color('green'), (*position,
                                                         one_piece * self._current_player_entity.exp, 10))

        text = f'{self._current_player_entity.exp} / ' \
               f'{self._current_player_entity.exp_amount_to_raise_level[self._current_player_entity.level]}'
        exp_text = pygame.font.Font(None, 16).render(text, True, pygame.Color('black'))
        place = pygame.Rect((*position, self._character_name_label.rect.width, 1)).center
        screen.blit(exp_text, place)

    def _draw_inventory(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self._inventory.draw_rect = pygame.Rect(*position, *self._inventory.draw_rect.size)
        self._inventory.draw(screen)

    def _draw_character_equipment(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        width, height = screen.get_size()
        size = width // 2 - indent * 2 - self._exit_button.rect.width
        self._current_player_entity.main_weapon.draw_rect = pygame.Rect(*position, size // 2, size // 2)
        self._current_player_entity.main_weapon.draw(screen)
        self._current_player_entity.secondary_weapon.draw_rect = pygame.Rect(position[0] + size // 2, position[1],
                                                                             size // 2, size // 2)
        self._current_player_entity.secondary_weapon.draw(screen)

    def get_click(self, event: pygame.event.Event):
        if not self._inventory.draw_rect.collidepoint(event.pos):
            self._acting_item = None
        self._switch_character(event.pos)
        self._upgrade_skill(event.pos)
        self._inventory.get_click(event)
        self._act_with_items(event.pos)
        self._set_equipment_info_menu(event.pos)
        self._set_player_entity_info_menu(event.pos)

    def _switch_character(self, mouse_pos: typing.Tuple[int, int]):
        if self._next_player_button.rect.collidepoint(mouse_pos):
            current_player_entity_index = [index for index, i in enumerate(self._player_entities)
                                           if i == self._current_player_entity][0]
            self._current_player_entity = self._player_entities[current_player_entity_index + 1] if \
                current_player_entity_index + 1 < len(self._player_entities) \
                else self._player_entities[0]

            self._character_name_label.set_text(self._current_player_entity.name)

        if self._previous_player_button.rect.collidepoint(mouse_pos):
            current_player_entity_index = [index for index, i in enumerate(self._player_entities)
                                           if i == self._current_player_entity][0]
            self._current_player_entity = self._player_entities[current_player_entity_index - 1] if \
                current_player_entity_index - 1 >= 0 \
                else self._player_entities[-1]

            self._character_name_label.set_text(self._current_player_entity.name)
        self._character_icon_label.set_image(self._current_player_entity.icon)

    def _upgrade_skill(self, mouse_pos: typing.Tuple[int, int]):
        if self._picked_skill is not None:
            if self._accept_skill_dialog.accept_button.rect.collidepoint(mouse_pos):
                self._picked_skill.level_up()
                self._picked_skill.apply_effect(self._current_player_entity)
                self._current_player_entity.upgrade_points -= 1
                print('cards:', self._current_player_entity.cards, 'attack:', self._current_player_entity.attack)
                self._picked_skill = None
            elif self._accept_skill_dialog.reject_button.rect.collidepoint(mouse_pos):
                self._picked_skill = None
            return

        for skills in self._current_player_entity.skills.values():
            for skill in skills:
                if not skill.rect.collidepoint(mouse_pos):
                    continue
                self._picked_skill = skill
                if self._picked_skill.current_level == self._picked_skill.max_level:
                    self._picked_skill = None
                if self._current_player_entity.upgrade_points <= 0:
                    self._picked_skill = None

    def _act_with_items(self, mouse_pos: typing.Tuple[int, int]):
        if self._acting_item is not None:
            result = self._process_action_clicks(mouse_pos)
            if result:
                self._acting_item = None
                self._acting_item_menu = None
                return
        item_pos = self._inventory.get_cell(mouse_pos)
        if item_pos is None or item_pos[1] + item_pos[0] * self._inventory.columns >= len(self._inventory.items):
            return
        self._acting_item = self._inventory.items[item_pos[1] + item_pos[0] * self._inventory.columns]
        self._acting_item_menu = ItemMenageMenu(self._acting_item)
        self._context_menu_pos = mouse_pos

    def _process_action_clicks(self, mouse_pos: typing.Tuple[int, int]) -> bool:
        if self._acting_item_menu.throw_button.rect.collidepoint(mouse_pos):
            self._inventory.items.remove(self._acting_item)
            return True
        if self._acting_item.item_type == ItemType.Consumable and \
                self._acting_item_menu.use_button.rect.collidepoint(mouse_pos):
            self._acting_item.action(self._current_player_entity)
            self._inventory.remove_item(self._acting_item, 1)
            return True
        if self._acting_item.item_type == ItemType.Equipment and \
                self._acting_item_menu.equip_button.rect.collidepoint(mouse_pos):
            leading_weapon = self._current_player_entity.main_weapon \
                if isinstance(self._acting_item,
                              Equipment) and self._acting_item.equipment_type == EquipmentType.MainWeapon \
                else self._current_player_entity.secondary_weapon
            old_weapon = leading_weapon.items.copy()
            leading_weapon.extend_items({self._acting_item.__class__: 1})
            self._inventory.extend_items({i.__class__: 1 for i in old_weapon})
            self._inventory.remove_item(self._acting_item, 1)
            return True

        return False

    def _set_equipment_info_menu(self, mouse_pos: typing.Tuple[int, int]):
        if self._info_dialog and\
            (self._info_dialog.accept_button.rect.collidepoint(mouse_pos) or
             self._info_dialog.reject_button.rect.collidepoint(mouse_pos)):
            self._info_dialog = None
            return
        self._set_main_weapon_info_menu(mouse_pos)
        self._set_secondary_weapon_info_menu(mouse_pos)

    def _set_main_weapon_info_menu(self, mouse_pos: typing.Tuple[int, int]):
        if self._current_player_entity.main_weapon.draw_rect.collidepoint(mouse_pos):
            if not self._current_player_entity.main_weapon.items:
                return
            weapon = self._current_player_entity.main_weapon.items[0]
            images = [card_class().image for card_class in weapon.cards]
            description = weapon.name + '\n' + "\n".join([f"{i} - {j}" for i, j in weapon.characteristics.items()])
            self._info_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                             (self._draw_rect.width // 2, self._draw_rect.height // 1.5),
                                             'информация', description, font_size=28, info_font_size=24,
                                             images=images)

    def _set_secondary_weapon_info_menu(self, mouse_pos: typing.Tuple[int, int]):
        if self._current_player_entity.secondary_weapon.draw_rect.collidepoint(mouse_pos):
            if not self._current_player_entity.secondary_weapon.items:
                return
            weapon = self._current_player_entity.secondary_weapon.items[0]
            images = [card_class().image for card_class in weapon.cards]
            description = weapon.name + '\n' + "\n".join([f"{i} - {j}" for i, j in weapon.characteristics.items()])
            self._info_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                             (self._draw_rect.width // 2, self._draw_rect.height // 1.5),
                                             'информация', description, font_size=28, info_font_size=24,
                                             images=images)

    def _set_player_entity_info_menu(self, mouse_pos: typing.Tuple[int, int]):
        if self._character_icon_label.rect.collidepoint(mouse_pos):
            images = [card.image for card in self._current_player_entity.cards]
            description = f'level    -  {self._current_player_entity.level}\n' \
                          f'attack -  {self._current_player_entity.attack}\n' \
                          f'hp        -  {self._current_player_entity.hp} / {self._current_player_entity.max_hp}'
            self._info_dialog = AcceptDialog(BlueBackgroundSprite().image,
                                             (self._draw_rect.width // 2, self._draw_rect.height // 1.5),
                                             'информация', description, images=images, font_size=28, info_font_size=24,
                                             alignment=Alignment.Left)

    @property
    def exit_button(self):
        return self._exit_button
