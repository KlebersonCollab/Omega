import pygame
import pygame.locals as pl
from core.widgets.base_widget import BaseWidget

class TextInputWidget(BaseWidget):
    def __init__(self, x, y, width, height, font_path='resources/fonts/Roboto-Regular.ttf', font_size=24, text_color=(0, 0, 0), bg_color=(255, 255, 255), max_length=None, is_password=False, attached_window=None, callback=None):
        super().__init__(x, y, width, height, attached_window)
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.max_length = max_length
        self.is_password = is_password
        self.callback = callback
        self.text = ""
        self.cursor_visible = True
        self.cursor_counter = 0
        self.cursor_position = len(self.text)
        self.selected = False
        self.next_input = None  # Referência ao próximo campo de entrada de texto

        self.font = pygame.font.Font(font_path, font_size)
        self.update_absolute_position()

        # Para controlar a repetição de teclas
        self.key_repeat_delay = 500  # Delay inicial em milissegundos
        self.key_repeat_interval = 200  # Intervalo entre repetições em milissegundos
        self.last_keydown_time = 0
        self.last_key = None
        self.last_char = ''  # Último caractere digitado

    def handle_event(self, event):
        if not self.visible:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.absolute_rect.collidepoint(event.pos):
                self.selected = True
            else:
                self.selected = False

        if self.selected and event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            if event.key in [pl.K_BACKSPACE, pl.K_DELETE, pl.K_RETURN, pl.K_LEFT, pl.K_RIGHT, pl.K_v, pl.K_c, pl.K_TAB]:
                self.handle_keydown(event)
                self.last_keydown_time = current_time
                self.last_key = event.key
                self.last_char = event.unicode  # Armazena o último caractere digitado
            elif event.key != self.last_key or (current_time - self.last_keydown_time) > self.key_repeat_delay:
                self.last_keydown_time = current_time
                self.last_key = event.key
                self.last_char = event.unicode  # Armazena o último caractere digitado
                self.handle_keydown(event)

        if self.selected and event.type == pygame.KEYUP:
            self.last_key = None

    def handle_keydown(self, event):
        if event.key == pl.K_BACKSPACE:
            if self.cursor_position > 0:
                self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                self.cursor_position -= 1
        elif event.key == pl.K_DELETE:
            if self.cursor_position < len(self.text):
                self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
        elif event.key == pl.K_RETURN:
            if self.callback:
                self.callback(self.text)
        elif event.key == pl.K_TAB:
            if self.next_input:
                self.selected = False
                self.next_input.selected = True
        elif event.key == pl.K_LEFT:
            self.cursor_position = max(0, self.cursor_position - 1)
        elif event.key == pl.K_RIGHT:
            self.cursor_position = min(len(self.text), self.cursor_position + 1)
        elif event.key == pl.K_v and (event.mod & pl.KMOD_CTRL):
            clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')
            self.text = self.text[:self.cursor_position] + clipboard_text + self.text[self.cursor_position:]
            self.cursor_position += len(clipboard_text)
        elif event.key == pl.K_c and (event.mod & pl.KMOD_CTRL):
            pygame.scrap.put(pygame.SCRAP_TEXT, self.text.encode('utf-8'))
        else:
            if event.unicode and (self.max_length is None or len(self.text) < self.max_length):
                self.text = self.text[:self.cursor_position] + event.unicode.replace('\x00', '') + self.text[self.cursor_position:]
                self.cursor_position += 1

    def render(self, screen):
        if not self.visible:
            return

        self.update_absolute_position()
        
        pygame.draw.rect(screen, self.bg_color, self.absolute_rect)
        text_surface = self.font.render(self.get_display_text(), True, self.text_color)
        text_rect = text_surface.get_rect(topleft=(self.absolute_rect.x + 5, self.absolute_rect.y + (self.absolute_rect.height - self.font_size) // 2))
        screen.blit(text_surface, text_rect)

        if self.selected:
            self.cursor_counter += 1
            if self.cursor_counter >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_counter = 0
            if self.cursor_visible:
                cursor_surface = self.font.render("|", True, self.text_color)
                cursor_rect = cursor_surface.get_rect(topleft=(text_rect.left + self.font.size(self.get_display_text()[:self.cursor_position])[0] + 2, text_rect.y))
                screen.blit(cursor_surface, cursor_rect)

    def get_display_text(self):
        if self.is_password:
            return "*" * len(self.text)
        return self.text.replace('\x00', '')

    def update(self):
        super().update()
        if self.selected and self.last_key:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_keydown_time > self.key_repeat_interval:
                event = pygame.event.Event(pygame.KEYDOWN, key=self.last_key, unicode=self.last_char)
                self.handle_keydown(event)
                self.last_keydown_time = current_time

    def set_text(self, text):
        if self.max_length is None or len(text) <= self.max_length:
            self.text = text.replace('\x00', '')
            self.cursor_position = len(text)

    def get_text(self):
         return self.text.replace('\x00', '')
