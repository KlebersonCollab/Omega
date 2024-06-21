from core.widgets.button_widget import ButtonWidget
from core.widgets.check_box_widget import CheckBoxWidget
from core.widgets.label_widget import LabelWidget
from core.widgets.text_input_widget import TextInputWidget

class WindowLogin:
    def __init__(self, window_manager, widget_manager):
        self.window_manager = window_manager
        self.widget_manager = widget_manager

    def create_windows(self):
        login_window = self.window_manager.create_window(
            100, 100, 300, 250,
            body_color=(0, 0, 0, 70),
            title="Login",
        )
        return login_window

    def create_login_widgets(self, window, callback):
        LabelWidget(20, 30, 100, 30, "Username:", font_size=16, attached_window=window).register(self.widget_manager, window)
        username_input = TextInputWidget(120, 30, 160, 30, font_size=20, attached_window=window)
        username_input.register(self.widget_manager, window)

        LabelWidget(20, 80, 100, 30, "Password:", font_size=16, attached_window=window).register(self.widget_manager, window)
        password_input = TextInputWidget(120, 80, 160, 30, font_size=20, is_password=True, attached_window=window)
        password_input.register(self.widget_manager, window)

        #username_input.next_input = password_input  # Define o próximo campo de entrada para tabulação
        #password_input.next_input = username_input  # Define o próximo campo de entrada para tabulação (loop)

        show_password_check = CheckBoxWidget(120, 120, 20, attached_window=window, callback=lambda checked: self.toggle_password_visibility(checked, password_input))
        show_password_check.register(self.widget_manager, window)

        LabelWidget(100, 116, 200, 30, "Show Password", font_size=12, attached_window=window).register(self.widget_manager, window)

        login_button = ButtonWidget(80, 170, 140, 40, "Login", attached_window=window, callback=callback)
        login_button.register(self.widget_manager, window)
        
    def toggle_password_visibility(self, checked, password_input):
        password_input.is_password = not checked
