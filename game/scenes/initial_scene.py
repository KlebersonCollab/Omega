import pygame
from core.widgets.widget_manager import WidgetManager
from core.windows.window_manager import WindowManager
from game.scenes.login_scene import LoginScene
from game.windows.window_login import WindowLogin

class InitialScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.widget_manager = WidgetManager()
        self.window_manager = WindowManager(self.widget_manager)

        factory = WindowLogin(self.window_manager, self.widget_manager)
        self.login_window = factory.create_windows()
        factory.create_login_widgets(self.login_window, self.handle_login)

    def start(self):
        print("Initial Scene Started")

    def handle_login(self):
        print("Login button clicked")
        # Navegar para a LoginScene
        login_scene = LoginScene(self.scene_manager)
        self.scene_manager.change_scene(login_scene)

    def handle_event(self, event):
        self.window_manager.handle_event(event)
        self.widget_manager.handle_event(event)

    def update(self):
        self.window_manager.update()

    def render(self, screen):
        screen.fill((255, 255, 255))
        self.window_manager.render(screen)

    def destroy(self):
        print("Initial Scene Destroyed")
