import pygame
import typing
from enum import Enum
from source.data.sprites.primitives import GreenBackgroundSprite, RedBackgroundSprite, GrayBackgroundSprite


class Alignment(Enum):
    Center = 0
    Left = 1
    Right = 2


class Label(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], text: str = '', font_size: int = 12,
                 alignment=Alignment.Center):
        super(Label, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self._text = text
        self._font_size = font_size
        self._alignment = alignment

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self.rect.x, self.rect.y = position
        screen.blit(self.image, position)
        text = pygame.font.Font(None, self._font_size).render(self._text, True, pygame.Color('white'))
        if self._alignment == Alignment.Center:
            place = text.get_rect(center=self.rect.center)
        elif self._alignment == Alignment.Left:
            place = text.get_rect(topleft=self.rect.topleft)
            place.x += 5
        else:
            place = text.get_rect(topright=self.rect.topright)
            place.x -= 5
        screen.blit(text, (place.x, self.rect.center[1] - self.rect.height // 4))

    def set_text(self, new_text: str):
        self._text = new_text

    def set_font_size(self, new_font_size: int):
        self._font_size = new_font_size


class AcceptDialog(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], title: str = '', text: str = '',
                 font_size: int = 12, info_font_size: int = 12, alignment: Alignment = Alignment.Center):
        super(AcceptDialog, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self._title = title
        self._text = text
        self._font_size = font_size
        self._info_font_size = info_font_size
        self._alignment = alignment

        self._accept_button = Label(GreenBackgroundSprite().image, (self.rect.width // 2, self.rect.height // 10),
                                    text='OK', font_size=self._font_size)
        self._reject_button = Label(RedBackgroundSprite().image, (self.rect.width // 2, self.rect.height // 10),
                                    text='не ОК', font_size=self._font_size)

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        print(self.rect.height)
        self.rect.x, self.rect.y = position

        title_label = Label(GrayBackgroundSprite().image, (self.rect.width, self.rect.height // 10),
                            text=self._title, font_size=self._font_size)
        title_label.draw(screen, self.rect.topleft)

        info_label = Label(self.image, (self.rect.width, self.rect.height - self.rect.height // 5),
                           text=self._text, font_size=self._info_font_size)
        info_label.draw(screen, (self.rect.x, self.rect.y + title_label.rect.height))

        self._accept_button.draw(screen, (self.rect.width,
                                          self.rect.y + self.rect.height - self._accept_button.rect.height))
        self._reject_button.draw(screen, (self.rect.width // 2,
                                          self.rect.y + self.rect.height - self._reject_button.rect.height))

    def set_text(self, new_text: str):
        self._text = new_text

    def set_font_size(self, new_font_size: int):
        self._font_size = new_font_size

    @property
    def accept_button(self):
        return self._accept_button

    @property
    def reject_button(self):
        return self._reject_button


class ContextMenu(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], actions: typing.List[Label]):
        super(ContextMenu, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self._actions = [i for i in actions if i is not None]
        self._indent = 3

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self.rect.x, self.rect.y = position
        action_height = self.rect.height // len(self._actions)

        for index, action in enumerate(self._actions):
            action.rect = pygame.Rect(0, 0, self.rect.width, action_height)
            action.image = pygame.transform.scale(self.image, (self.rect.width, action_height))
            action.draw(screen, (self.rect.x, self.rect.y + (self._indent + action_height) * index))
            print(index, ':', self.rect.x, self.rect.y + (self._indent + action_height) * index)
