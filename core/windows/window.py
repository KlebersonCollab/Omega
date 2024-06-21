import pygame

class Window:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False  # Adiciona a propriedade dragging
        self.drag_offset = (0, 0)  # Adiciona a propriedade drag_offset
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
    def start_drag(self, mouse_pos):
        self.dragging = True
        self.drag_offset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])
    
    def stop_drag(self):
        self.dragging = False
        
    def drag(self, mouse_pos):
        if self.dragging:
            self.rect.x = mouse_pos[0] + self.drag_offset[0]
            self.rect.y = mouse_pos[1] + self.drag_offset[1]
