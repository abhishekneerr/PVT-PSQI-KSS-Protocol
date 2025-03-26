# screens/pvt_instructions.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
import logging

from utils.translation_handler import tr
from utils.translated_widgets import (
    TranslatedLabel, TranslatedButton
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_pvt_instructions_screen(stack):
    """Creates the PVT Instructions Screen, screen #4"""
    screen = QWidget()
    layout = QVBoxLayout()

    # Instructions Label (auto-refreshing)
    instructions_label = TranslatedLabel("pvt_instructions_text")
    instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    instructions_label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(instructions_label)

    # Navigation Buttons
    nav_layout = QHBoxLayout()

    # If you want this button localized, e.g. "next_button":
    next_button = TranslatedButton("next_button")
    next_button.clicked.connect(lambda: stack.setCurrentIndex(5))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)
    return screen
