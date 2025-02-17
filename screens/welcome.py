from PyQt6.QtWidgets import ( QWidget, QLabel,
    QVBoxLayout, QPushButton,

)


import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def create_welcome_screen(stack):
    """Creates the Welcome Screen, screen #0 """
    screen = QWidget()
    layout = QVBoxLayout()

    label = QLabel("Hello, thank you for taking part in this test!")
    label.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(label)

    next_button = QPushButton("Next")
    next_button.setStyleSheet("font-size: 18px; padding: 10px;")
    next_button.resize(20,10)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(1))  # Move to demographic form
    layout.addWidget(next_button)
    

    screen.setLayout(layout)
    return screen

