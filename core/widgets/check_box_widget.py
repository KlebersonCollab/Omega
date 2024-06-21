import pygame
from core.widgets.base_widget import BaseWidget

class CheckBoxWidget(BaseWidget):
    def __init__(self, x, y, size, checked_image_path='resources/widgets/checked.png', unchecked_image_path='resources/widgets/unchecked.png', attached_window=None, callback=None):
        super().__init__(x, y, size, size, attached_window)
        self.checked_image = pygame.image.load(checked_image_path).convert_alpha()
        self.unchecked_image = pygame.image.load(unchecked_image_path).convert_alpha()
        self.checked_image = pygame.transform.scale(self.checked_image, (size, size))
        self.unchecked_image = pygame.transform.scale(self.unchecked_image, (size, size))
        self.callback = callback
        self.checked = False
        self.was_clicked = False  # Variável para rastrear o estado do clique

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and not self.was_clicked:
            if self.absolute_rect.collidepoint(event.pos):
                if not self.attached_window or self.attached_window.manager.active_window == self.attached_window:
                    self.toggle()
                    self.was_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.was_clicked = False  # Libera o estado de clique

    def toggle(self):
        self.checked = not self.checked
        if self.callback:
            self.callback(self.checked)

    def render(self, screen):
        if not self.visible:
            return
        self.update_absolute_position()  # Atualiza a posição antes de renderizar
        if self.checked:
            screen.blit(self.checked_image, self.absolute_rect.topleft)
        else:
            screen.blit(self.unchecked_image, self.absolute_rect.topleft)
