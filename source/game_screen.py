import pygame
import typing
from source.player_view_map import PlayerViewMap
from source.cell import CellModifierType
from source.generate_mod import GenerateMod, GenerateModType
from source.battle import Battle
from source.enemies import Beetle
from source.ui import Label, Alignment
from source.data.sprites.primitives import NextButtonSprite, PreviousButtonSprite, BlueBackgroundSprite


class GameScreen(pygame.Surface):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameScreen, self).__init__(size)

    def draw(self, screen: pygame.Surface):
        pass


class GameMapScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int]):
        super(GameMapScreen, self).__init__(size)

        self._player_view_map = PlayerViewMap(pygame.Rect(0, 0, *size), None)
        cell_dict = {CellModifierType.EmptyCell: GenerateMod(GenerateModType.Base, 1),
                     CellModifierType.EnemyCell: GenerateMod(GenerateModType.Probability, 1)}
        self._player_view_map.generate_map((50, 50), cell_dict)

        image = pygame.Surface((100, 100))
        image.fill(pygame.Color('blue'))
        self._palmtop_button = Label(image, (40, 30), text='КПК', font_size=16)

    def draw(self, screen: pygame.Surface):
        surface = pygame.Surface((screen.get_rect().width - self._palmtop_button.rect.width, screen.get_rect().height))
        self._player_view_map.draw(surface)
        screen.blit(surface, (0, 0))
        self._palmtop_button.draw(screen, (screen.get_rect().width - self._palmtop_button.rect.width, 0))

    @property
    def game_map(self):
        return self._player_view_map

    @property
    def palmtop_button(self):
        return self._palmtop_button


class BattleScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List):
        super(BattleScreen, self).__init__(size)

        self._player_entities = player_entities
        enemy_entities = [Beetle(1), Beetle(1), Beetle(1)]
        self._battle = Battle(pygame.Rect(0, 0, *size), player_entities, enemy_entities)

    def draw(self, screen: pygame.Surface):
        self._battle.draw(screen)

    @property
    def battle(self):
        return self._battle


class PalmtopUIScreen(GameScreen):
    def __init__(self, size: typing.Tuple[int, int], player_entities: typing.List):
        super(PalmtopUIScreen, self).__init__(size)

        self._player_entities = player_entities
        self._current_player_entity = player_entities[0]
        image = pygame.Surface((100, 100))
        image.fill(pygame.Color('blue'))
        self._exit_button = Label(image, (40, 30), text='карта', font_size=18)
        self._next_player_button = Label(NextButtonSprite().image, (30, 27))
        self._previous_player_button = Label(PreviousButtonSprite().image, (30, 27))
        self._character_name_label = Label(BlueBackgroundSprite().image, (200, 30),
                                           text=self._current_player_entity.name, font_size=24)

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

    def _draw_character_switcher(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        self._character_name_label.draw(screen, (position[0] - self._character_name_label.rect.width // 2, position[1]))
        self._previous_player_button.draw(screen, (position[0] - self._character_name_label.rect.width // 2 - indent -
                                                   self._previous_player_button.rect.width, position[1]))
        self._next_player_button.draw(screen, (position[0] + self._character_name_label.rect.width // 2 + indent,
                                               position[1]))

    def _draw_character_skill_tree(self, screen: pygame.Surface, position: typing.Tuple[int, int], indent=25):
        surface = pygame.Surface((screen.get_size()[0] // 2, screen.get_size()[1]))
        pygame.draw.rect(surface, pygame.Color('gray'), (0, 0, *surface.get_size()), 3)
        skill_tree: dict = self._current_player_entity.speciality.value.SkillTree
        cols = [indent, surface.get_size()[0] // 2]
        for list_index, skills in enumerate(skill_tree.values()):
            for skill_index, skill in enumerate(skills):
                label = Label(BlueBackgroundSprite().image, (surface.get_size()[0] // 2 - indent * 2, 30),
                              skill, font_size=20, alignment=Alignment.Left)
                label.draw(surface, (cols[skill_index], indent + indent * 2 * list_index))
        screen.blit(surface, (0, 0))

    def get_click(self, mouse_pos: typing.Tuple[int, int]):
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

    @property
    def exit_button(self):
        return self._exit_button
