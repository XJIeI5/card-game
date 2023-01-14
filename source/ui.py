import pygame
import typing
from enum import Enum
from source.data.sprites.primitives import GreenBackgroundSprite, RedBackgroundSprite, GrayBackgroundSprite


class Alignment(Enum):
    Center = 0
    Left = 1
    Right = 2


def blit_text(screen: pygame.Surface, draw_rect: pygame.Rect, text: str, font_size: int,
              color: pygame.Color = pygame.Color('black'), alignment: Alignment = Alignment.Center):
    lines = text.split('\n')
    font = pygame.font.Font(None, font_size)
    line_height = font.size('A')[1]
    for index, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        if alignment == Alignment.Center:
            place = text_surface.get_rect(center=draw_rect.center)
        elif alignment == Alignment.Left:
            place = text_surface.get_rect(topleft=draw_rect.topleft)
            place.x += 5
        else:
            place = text_surface.get_rect(topright=draw_rect.topright)
            place.x -= 5
        screen.blit(text_surface, (place.x, draw_rect.center[1] - draw_rect.height // 4 +
                                   line_height * index))  # (place.x, screen.get_rect().center[1] - screen.get_rect().height // 4)))


class Label(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], text: str = '', font_size: int = 12,
                 alignment=Alignment.Center, color: pygame.Color = pygame.Color('white')):
        super(Label, self).__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self._text = text
        self._font_size = font_size
        self._alignment = alignment
        self._color = color

    def draw(self, screen: pygame.Surface, position: typing.Tuple[int, int]):
        self.rect.x, self.rect.y = position
        screen.blit(self.image, position)
        blit_text(screen, self.rect, self._text, self._font_size, color=self._color,
                  alignment=self._alignment)

    def set_text(self, new_text: str):
        self._text = new_text

    def set_font_size(self, new_font_size: int):
        self._font_size = new_font_size

    def set_image(self, new_image: pygame.Surface):
        self.image = pygame.transform.scale(new_image, self.rect.size)

    def set_color(self, new_color: pygame.Color):
        self._color = new_color


class AcceptDialog(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, size: typing.Tuple[int, int], title: str = '', text: str = '',
                 font_size: int = 12, info_font_size: int = 12, alignment: Alignment = Alignment.Center,
                 images=None):
        super(AcceptDialog, self).__init__()
        if images is None:
            images = []
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self._title = title
        self._text = text
        self._font_size = font_size
        self._info_font_size = info_font_size
        self._alignment = alignment
        self._images: typing.List[pygame.Surface] = images
        self._images_indent = 10

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
                           text=self._text, font_size=self._info_font_size, alignment=self._alignment)
        info_label.draw(screen, (self.rect.x, self.rect.y + title_label.rect.height))

        if self._images:
            image_size = self.rect.width // len(self._images) - self._images_indent, info_label.rect.height // 2
            for index, image in enumerate(self._images):
                image_width, image_height = image.get_size()
                image = pygame.transform.scale(image, (image_size[0] if image_width > image_size[0] else image_width,
                                                       image_size[1] if image_height > image_size[1] else image_height))
                screen.blit(image,
                            (self._images_indent // 2 + position[0] + (image_size[0] + self._images_indent) * index,
                             info_label.rect.center[1]))

        # buttons
        self._accept_button.draw(screen,
                                 (self.rect.x + self.rect.width // 2,
                                  self.rect.y + self.rect.height - self._accept_button.rect.height))
        self._reject_button.draw(screen,
                                 (self.rect.x,
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

        for index, action in enumerate(self._actions):
            action.rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            action.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            action.draw(screen, (self.rect.x, self.rect.y + (self._indent + self.rect.height) * index))
