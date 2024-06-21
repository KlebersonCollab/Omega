import pygame
from core.widgets.base_widget import BaseWidget

class LabelWidget(BaseWidget):
    def __init__(self, x, y, width, height, text, font_path='resources/fonts/Roboto-Regular.ttf', font_size=24, text_color=(0, 0, 0), bg_color=None, attached_window=None):
        super().__init__(x, y, width, height, attached_window)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(font_path, font_size)
        self.update_absolute_position()

    def render(self, screen):
        if not self.visible:
            return

        self.update_absolute_position()

        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, self.absolute_rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.absolute_rect.center)
        screen.blit(text_surface, text_rect)
