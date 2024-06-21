class SceneManager:
    def __init__(self):
        self.scene = None
    
    def change_scene(self, scene):
        if self.scene is not None:
            self.scene.destroy()
        self.scene = scene
        self.scene.start()
    
    def handle_event(self, event):
        if self.scene is not None:
            self.scene.handle_event(event)
    
    def update(self):
        if self.scene is not None:
            self.scene.update()
    
    def render(self, screen):
        if self.scene is not None:
            self.scene.render(screen)
