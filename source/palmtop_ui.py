import pygame
import typing
from source.ui import Label
from source.data.sprites.primitives import NextButtonSprite, PreviousButtonSprite, BlueBackgroundSprite,\
    GreenBackgroundSprite
from source.skill import Skill


class PalmtopUI:
    def __init__(self, draw_rect: pygame.Rect, player_entities: typing.List):

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
        self._accept_button: typing.Union[None, Label] = None

        self._picked_skill: typing.Union[None, Skill] = None

    def draw(self, screen: pygame.Surface):
        indent = 25

        self._draw_character_switcher(screen, (screen.get_rect().center[0] * 1.5 - indent, 10))
        # draw character
        screen.blit(pygame.transform.scale(self._current_player_entity.icon,
                                           (self._character_name_label.rect.width,
                                            self._character_name_label.rect.width)),
                    (self._character_name_label.offset[0], self._character_name_label.offset[1] +
                     self._character_name_label.rect.height + indent))

        self._draw_character_skill_tree(screen, (0, 0))

        self._exit_button.draw(screen, (screen.get_rect().width - self._exit_button.rect.width, 0))

        if self._picked_skill:
            self._draw_accept_dialog_box(screen, (self._draw_rect.width // 4, self._draw_rect.height // 4))

    def _draw_character_switcher(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        self._character_name_label.draw(screen, (position[0] - self._character_name_label.rect.width // 2, position[1]))
        self._previous_player_button.draw(screen, (position[0] - self._character_name_label.rect.width // 2 - indent -
                                                   self._previous_player_button.rect.width, position[1]))
        self._next_player_button.draw(screen, (position[0] + self._character_name_label.rect.width // 2 + indent,
                                               position[1]))

    def _draw_character_skill_tree(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        surface = pygame.Surface((screen.get_size()[0] // 2, screen.get_size()[1] // 3))
        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, *surface.get_size()), 3)
        skill_tree: dict = self._current_player_entity.skills
        cols = [indent, surface.get_size()[0] // 2]
        for list_index, skills in enumerate(skill_tree.values()):
            for skill_index, skill in enumerate(skills):
                draw_rect = pygame.Rect(cols[skill_index], indent + indent * list_index
                                        + skill.rect.height * list_index, surface.get_size()[0] // 2 - indent * 2, 30)
                skill.draw(surface, draw_rect)
        screen.blit(surface, position)

    def _draw_accept_dialog_box(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        sure_label = Label(BlueBackgroundSprite().image, (self._draw_rect.width // 2, 35),
                           text='Вы уверены?!', font_size=36)
        sure_label.draw(screen, (position[0], position[1]))

        info_label = Label(BlueBackgroundSprite().image, (self._draw_rect.width // 2, self._draw_rect.height // 2 - 60),
                           text=self._picked_skill.description[self._picked_skill.current_level], font_size=18)
        info_label.draw(screen, (position[0], position[1] + sure_label.rect.height))

        self._accept_button = Label(GreenBackgroundSprite().image, (self._draw_rect.width // 2, 30),
                                    text='подтвердить', font_size=20)
        self._accept_button.draw(screen, (position[0], position[1] + sure_label.rect.height + info_label.rect.height))

    def get_click(self, mouse_pos: typing.Tuple[int, int]):
        self._switch_character(mouse_pos)
        self._upgrade_skill(mouse_pos)

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

    def _upgrade_skill(self, mouse_pos: typing.Tuple[int, int]):
        if self._picked_skill is not None:
            if self._accept_button is not None and self._accept_button.rect.collidepoint(mouse_pos):
                self._picked_skill.level_up()
                self._picked_skill.apply_effect(self._current_player_entity)
                print(self._current_player_entity.cards)
            self._picked_skill = None
            return

        for skills in self._current_player_entity.skills.values():
            for skill in skills:
                if not skill.rect.collidepoint(mouse_pos):
                    continue
                self._picked_skill = skill
                if self._picked_skill.current_level == self._picked_skill.max_level:
                    self._picked_skill = None

    @property
    def exit_button(self):
        return self._exit_button
