import pygame
from core.widgets.base_widget import BaseWidget

class RadioButtonWidget(BaseWidget):
    def __init__(self, x, y, size, selected_image_path='resources/widgets/radio_check.png', unselected_image_path='resources/widgets/radio_uncheck.png', attached_window=None, group=None, callback=None):
        super().__init__(x, y, size, size, attached_window)
        self.selected_image = pygame.image.load(selected_image_path).convert_alpha()
        self.unselected_image = pygame.image.load(unselected_image_path).convert_alpha()
        self.selected_image = pygame.transform.scale(self.selected_image, (size, size))
        self.unselected_image = pygame.transform.scale(self.unselected_image, (size, size))
        self.group = group
        self.callback = callback
        self.selected = False

        if self.group is not None:
            self.group.append(self)

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and not self.was_clicked:
            if self.absolute_rect.collidepoint(event.pos):
                if not self.attached_window or self.attached_window.manager.active_window == self.attached_window:
                    self.select()
                    self.was_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.was_clicked = False

    def select(self):
        if self.group is not None:
            for button in self.group:
                button.selected = False
        self.selected = True
        if self.callback:
            self.callback()

    def render(self, screen):
        if not self.visible:
            return
        self.update_absolute_position()
        if self.selected:
            screen.blit(self.selected_image, self.absolute_rect.topleft)
        else:
            screen.blit(self.unselected_image, self.absolute_rect.topleft)
