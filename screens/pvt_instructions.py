# screens/pvt_instructions.py

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 1) Import your translation helper
from utils.translation_handler import tr

def create_pvt_instructions_screen(stack):
    """Creates the PVT Instructions Screen, screen #4"""
    screen = QWidget()
    layout = QVBoxLayout()

    # Instructions
    # We retrieve the instructions from translations.json
    instructions = tr("pvt_instructions_text")

    label = QLabel(instructions)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(label)

    # Navigation Buttons
    nav_layout = QHBoxLayout()
    # back_button = QPushButton("Back")
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(3))
    # nav_layout.addWidget(back_button)

    # If you want this button localized, use tr("next_button"):
    next_button = QPushButton("Next")
    next_button.clicked.connect(lambda: stack.setCurrentIndex(5))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)
    return screen
