import pygame
from core.windows.window import Window

class SkinnedWindow(Window):
    def __init__(self, x, y, width, height, body_color=None, border_color=None, top_border_color=None, title="", title_color=(255, 255, 255), title_align="center", border_thickness_top=16, border_thickness_bottom=16, border_thickness_left=16, border_thickness_right=16):
        super().__init__(x, y, width, height)
        self.body_color = body_color or (0, 0, 0, 128)  # Default: semi-transparent black
        self.border_color = border_color or (255, 255, 255)  # Default: white
        self.top_border_color = top_border_color or self.border_color  # Default: same as border color
        self.title = title
        self.title_color = title_color
        self.title_align = title_align
        self.border_thickness_top = border_thickness_top
        self.border_thickness_bottom = border_thickness_bottom
        self.border_thickness_left = border_thickness_left
        self.border_thickness_right = border_thickness_right
        self.widgets = []
        self.close_button_rect = pygame.Rect(x + width - 20, y, 20, 20)  # Posiciona o botão de fechar no canto superior direito
        self.manager = None
        self.was_clicked = False  # Variável para rastrear o estado do clique no botão de fechar
        self.marked_for_removal = False  # Sinalizador para remoção
        self.visible = True  # Propriedade para controlar a visibilidade da janela

    def handle_event(self, event):
        super().handle_event(event)
        for widget in self.widgets:
            widget.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and not self.was_clicked:
            if self.close_button_rect.collidepoint(event.pos):
                self.widgets = []
                self.close()
                self.was_clicked = True  # Marca que o botão de fechar foi clicado
        elif event.type == pygame.MOUSEBUTTONUP:
            self.was_clicked = False  # Libera o estado de clique

    def close(self):
        # Método para fechar a janela
        self.marked_for_removal = True  # Marca a janela para remoção
        for widget in self.widgets:
            widget.attached_window = None
            self.manager.widget_manager.remove_widget(widget)  # Remova o widget imediatamente do widget_manager

    def render(self, screen):
        if not self.visible or self.marked_for_removal:
            return  # Não renderize se marcado para remoção ou não visível

        x, y, width, height = self.rect
        body_padding = 4

        if width <= self.border_thickness_left + self.border_thickness_right + body_padding or height <= self.border_thickness_top + self.border_thickness_bottom + body_padding:
            return  # Evita criar superfícies com dimensões inválidas

        body_surface = pygame.Surface(
            (
                width - self.border_thickness_left - self.border_thickness_right,
                height - self.border_thickness_top - self.border_thickness_bottom
            ),
            pygame.SRCALPHA
        )
        body_surface.fill(self.body_color)
        screen.blit(body_surface, (x + self.border_thickness_left, y + self.border_thickness_top))

        pygame.draw.rect(screen, self.top_border_color, (x, y, width, self.border_thickness_top))  # Top border
        pygame.draw.rect(screen, self.border_color, (x, y + height - self.border_thickness_bottom, width, self.border_thickness_bottom))  # Bottom border
        pygame.draw.rect(screen, self.border_color, (x, y + self.border_thickness_top, self.border_thickness_left, height - self.border_thickness_top - self.border_thickness_bottom))  # Left border
        pygame.draw.rect(screen, self.border_color, (x + width - self.border_thickness_right, y + self.border_thickness_top, self.border_thickness_right, height - self.border_thickness_top - self.border_thickness_bottom))  # Right border

        self.close_button_rect = pygame.Rect(x + width - 20, y, 20, 20)  # Atualiza a posição do botão de fechar
        font = pygame.font.Font(None, 28)  # Aumenta o tamanho da fonte para o "X"
        text = font.render("X", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.close_button_rect.center)
        screen.blit(text, text_rect)

        if self.title:
            title_font = pygame.font.Font(None, 24)
            title_surface = title_font.render(self.title, True, self.title_color)
            
            if self.title_align == "left":
                title_rect = title_surface.get_rect(midleft=(x + 10, y + self.border_thickness_top // 2))
            elif self.title_align == "right":
                title_rect = title_surface.get_rect(midright=(x + width - 30, y + self.border_thickness_top // 2))
            else:  # center
                title_rect = title_surface.get_rect(center=(x + width // 2, y + self.border_thickness_top // 2))
                
            screen.blit(title_surface, title_rect)

        for widget in self.widgets:
            widget.render(screen)

    def update(self):
        if self.marked_for_removal:
            return  # Não atualize se marcado para remoção

        super().update()
        for widget in self.widgets:
            widget.update()

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.attached_window = self
