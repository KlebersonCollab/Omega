import pygame
from core.windows.skinned_window import SkinnedWindow

class WindowManager:
    def __init__(self, widget_manager):
        self.windows = []
        self.active_window = None
        self.widget_manager = widget_manager

    def add_window(self, window):
        self.windows.append(window)
        self.update_widget_order()

    def remove_window(self, window):
        if window in self.windows:
            for widget in window.widgets:
                self.widget_manager.remove_widget(widget)
            self.windows.remove(window)
            self.update_widget_order()

    def create_window(self, x, y, width, height, body_color=(0, 0, 0, 128), border_color=(60,91,115), top_border_color=(60,91,115), title="", title_color=(255, 255, 255), title_align="center", border_thickness_top=20, border_thickness_bottom=4, border_thickness_left=4, border_thickness_right=4):
        window = SkinnedWindow(x, y, width, height, body_color, border_color, top_border_color, title, title_color, title_align, border_thickness_top, border_thickness_bottom, border_thickness_left, border_thickness_right)
        self.add_window(window)
        window.manager = self  # Set the manager for the window
        return window

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for window in reversed(self.windows):
                if window.visible and window.rect.collidepoint(event.pos):
                    self.set_active_window(window)
                    window.start_drag(event.pos)
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            if self.active_window:
                self.active_window.stop_drag()

        if event.type == pygame.MOUSEMOTION:
            if self.active_window:
                self.active_window.drag(event.pos)

        # Verificar e remover janelas fechadas
        for window in self.windows:
            if window.rect.width == 0 and window.rect.height == 0:
                self.remove_window(window)
                
        if self.active_window:
            self.active_window.handle_event(event)

    def update(self):
        for window in self.windows:
            window.update()

    def render(self, screen):
        for window in self.windows:
            if window.visible:
                window.render(screen)
                for widget in window.widgets:
                    widget.render(screen)
        for widget in self.widget_manager.widgets:
            if widget.attached_window is None:
                widget.render(screen)

    def set_active_window(self, window):
        if self.active_window != window:
            self.active_window = window
            self.windows.remove(window)
            self.windows.append(window)  # move window to top
            self.update_widget_order()

    def update_widget_order(self):
        self.widget_manager.update_widget_order(self.windows)

    def show_window(self, window):
        if window not in self.windows:
            self.add_window(window)
        window.visible = True
        for widget in window.widgets:
            widget.set_visibility(True)

    def hide_window(self, window):
        if window in self.windows:
            window.visible = False
            for widget in window.widgets:
                widget.set_visibility(False)
            self.update_active_window()

    def toggle_window_visibility(self, window):
        if window.visible:
            self.hide_window(window)
        else:
            self.show_window(window)

    def update_active_window(self):
        # Atualiza a janela ativa para a próxima janela visível
        for window in reversed(self.windows):
            if window.visible:
                self.set_active_window(window)
                break
        else:
            self.active_window = None
