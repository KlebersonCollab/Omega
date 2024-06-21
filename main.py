import pygame

from core.scenes.scene_manager import SceneManager
from game.scenes.initial_scene import InitialScene




def main():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Omega Engine")
    
    clock = pygame.time.Clock()
    scene_manager = SceneManager()
    
    initial_scene = InitialScene(scene_manager)
    scene_manager.change_scene(initial_scene)
    pygame.scrap.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    running = False
            scene_manager.handle_event(event)
        
        scene_manager.update()
        scene_manager.render(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
