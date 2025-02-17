from PyQt6.QtWidgets import (
    QWidget, QLabel,  
    QVBoxLayout, QPushButton
)
import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def create_ending_screen(stack):
    """Creates the Ending Screen, screen #8 """
    screen = QWidget()
    layout = QVBoxLayout()

    label = QLabel("Thank you for participating in this study!")
    label.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(label)

    exit_button = QPushButton("Exit")
    exit_button.setStyleSheet("font-size: 18px; padding: 10px;")
    exit_button.clicked.connect(lambda: sys.exit())  # Exit application
    layout.addWidget(exit_button)

    screen.setLayout(layout)
    return screen

