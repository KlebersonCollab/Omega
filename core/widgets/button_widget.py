import pygame
from core.widgets.base_widget import BaseWidget

class ButtonWidget(BaseWidget):
    def __init__(self, x, y, width, height, text, button_image_path='resources/widgets/button.png', font_size=24, attached_window=None, callback=None):
        super().__init__(x, y, width, height, attached_window)
        self.text = text
        self.callback = callback
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.button_image = pygame.image.load(button_image_path).convert_alpha()
        self.button_image = pygame.transform.scale(self.button_image, (width, height))

        self.font = pygame.font.Font(None, font_size)

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and not self.was_clicked:
            if self.absolute_rect.collidepoint(event.pos):
                if not self.attached_window or self.attached_window.manager.active_window == self.attached_window:
                    if self.callback:
                        self.callback()
                    if not self.attached_window:
                        self.dragging = True
                        self.drag_offset_x = self.absolute_rect.x - event.pos[0]
                        self.drag_offset_y = self.absolute_rect.y - event.pos[1]
                    self.was_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.was_clicked = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and not self.attached_window:
                self.absolute_rect.x = event.pos[0] + self.drag_offset_x
                self.absolute_rect.y = event.pos[1] + self.drag_offset_y
                self.relative_rect.topleft = self.absolute_rect.topleft

    def render(self, screen):
        if not self.visible:
            return
        self.update_absolute_position()
        button_surface = self.button_image.copy()
        if self.was_clicked:
            button_surface.set_alpha(128)
        screen.blit(button_surface, self.absolute_rect.topleft)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.absolute_rect.center)
        screen.blit(text_surface, text_rect)
