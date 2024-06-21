import pygame


class LoginScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def start(self):
        print("Login Scene Started")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Change to Initial Scene
            from game.scenes.initial_scene import InitialScene
            initial_scene = InitialScene(self.scene_manager)
            self.scene_manager.change_scene(initial_scene)
    
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill((0, 0, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Login Scene (Press ESC to go back)", True, (255, 255, 255))
        screen.blit(text, (200, 300))
    
    def destroy(self):
        print("Login Scene Destroyed")
