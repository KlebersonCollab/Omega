class WidgetManager:
    def __init__(self):
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)

    def handle_event(self, event):
        for widget in self.widgets:
            if widget.visible:
                widget.handle_event(event)

    def render(self, screen):
        for widget in self.widgets:
            if widget.visible:
                widget.render(screen)

    def update_widget_order(self, windows):
        ordered_widgets = []
        for window in windows:
            for widget in window.widgets:
                ordered_widgets.append(widget)
        independent_widgets = [widget for widget in self.widgets if widget.attached_window is None]
        self.widgets = independent_widgets + ordered_widgets
