# add code that updates the screen with the instructions
#screens/pvt_instructions.py
# add code that updates the screen with the instructions
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_pvt_instructions_screen(stack):
    """Creates the PVT Instructions Screen, screen #4"""
    screen = QWidget()
    layout = QVBoxLayout()
    # Instructions
    instructions = """
    In this section, you will complete a reaction time task. 
    
    When the counter appears on the screen, press the SPACEBAR as quickly as possible.
    
    Press the Next button to begin the task.
    """
    label = QLabel(instructions)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(label)


    # Navigation Buttons
    nav_layout = QHBoxLayout()
    # back_button = QPushButton("Back")
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(3))
    # nav_layout.addWidget(back_button)
    next_button = QPushButton("Next")
    next_button.clicked.connect(lambda: stack.setCurrentIndex(5))
    nav_layout.addWidget(next_button)
    layout.addLayout(nav_layout)
    screen.setLayout(layout)
    return screen
