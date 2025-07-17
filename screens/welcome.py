from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox
from PyQt6.QtCore import Qt
from utils.translation_handler import tr
from utils.translated_widgets import TranslatedLabel, TranslatedButton
from src.state import state_manager

def create_welcome_screen(stack):
    screen = QWidget()
    layout = QVBoxLayout()

    language_selector = QComboBox()
    language_selector.addItems(["English", "Français"])
    language_selector.setStyleSheet("font-size: 12px; padding: 5px; max-width: 100px;")
    language_selector.setFixedWidth(100)
    
    layout.addWidget(language_selector, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)


    layout.addStretch()  # <-- Add stretch below
    
    # Use a TranslatedLabel instead of QLabel
    welcome_label = TranslatedLabel("welcome_message")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    
    layout.addStretch()  # <-- Add stretch below

    

    # Use a TranslatedButton instead of QPushButton
    next_button = TranslatedButton("next_button")
    next_button.setStyleSheet("font-size: 16px; padding: 10px;")
    next_button.clicked.connect(lambda: stack.setCurrentIndex(1))
    layout.addWidget(next_button)

    def on_language_change():
        selected = language_selector.currentText()
        lang_code = "fr" if selected == "Français" else "en"
        state_manager.set_language(lang_code)
        # No manual setText calls needed—auto-refresh widgets pick it up

    language_selector.currentTextChanged.connect(on_language_change)

    screen.setLayout(layout)
    return screen
