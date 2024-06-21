import pygame

class BaseWidget:
    def __init__(self, x, y, width, height, attached_window=None):
        self.relative_rect = pygame.Rect(x, y, width, height)
        self.absolute_rect = pygame.Rect(x, y, width, height)
        self.attached_window = attached_window
        self.visible = True
        self.was_clicked = False

        self.update_absolute_position()

    def set_visibility(self, visible):
        self.visible = visible

    def handle_event(self, event):
        pass

    def render(self, screen):
        pass

    def update(self):
        if self.visible:
            self.update_absolute_position()

    def update_absolute_position(self):
        if self.attached_window and self.attached_window.rect.width > 0 and self.attached_window.rect.height > 0:
            self.absolute_rect.topleft = (
                self.attached_window.rect.x + self.relative_rect.x,
                self.attached_window.rect.y + self.relative_rect.y
            )
        else:
            self.absolute_rect.topleft = self.relative_rect.topleft

    def register(self, widget_manager, attached_window):
        widget_manager.add_widget(self)
        attached_window.add_widget(self)