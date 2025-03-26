from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
)
import sys
import csv
import os
import logging

from utils.translation_handler import tr
from utils.translated_widgets import TranslatedLabel, TranslatedButton
from src.state import state_manager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from utils.data_handler import save_to_csv


def create_ending_screen(stack):
    """Creates the Ending Screen, screen #8"""
    screen = QWidget()
    layout = QVBoxLayout()

    # Thank you message
    thank_you_label = TranslatedLabel("ending_thankyou")
    thank_you_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(thank_you_label)

    # Feedback prompt
    feedback_prompt = TranslatedLabel("ending_feedback_prompt")
    feedback_prompt.setStyleSheet("font-size: 18px;")
    layout.addWidget(feedback_prompt)

    # Feedback textbox
    feedback_textbox = QTextEdit()
    feedback_textbox.setMaximumHeight(200)
    layout.addWidget(feedback_textbox)

    # Buttons (Submit + Exit)
    button_layout = QHBoxLayout()

    submit_button = TranslatedButton("ending_submit_feedback")
    submit_button.setStyleSheet("font-size: 16px; padding: 10px;")

    def handle_submit_feedback():
        participant_id = state_manager.get_participant_id()
        feedback = feedback_textbox.toPlainText().strip()

        if not feedback:
            return  # Don't save empty feedback

        # Save feedback to CSV
        save_to_csv(participant_id, "feedback", {"feedback": feedback})

        # Optionally clear box or disable it
        feedback_textbox.setPlainText("")
        submit_button.setText(tr("ending_thank_you_feedback"))


    submit_button.clicked.connect(handle_submit_feedback)
    button_layout.addWidget(submit_button)

    exit_button = TranslatedButton("ending_exit_button")
    exit_button.setStyleSheet("font-size: 16px; padding: 10px;")
    exit_button.clicked.connect(lambda: sys.exit())
    button_layout.addWidget(exit_button)

    layout.addLayout(button_layout)

    screen.setLayout(layout)
    return screen



# -  - - - - - - - - old code

# from PyQt6.QtWidgets import (
#     QWidget, QLabel,  
#     QVBoxLayout, QPushButton
# )
# import sys
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# def create_ending_screen(stack):
#     """Creates the Ending Screen, screen #8 """
#     screen = QWidget()
#     layout = QVBoxLayout()

#     label = QLabel("Thank you for participating in this study!")
#     label.setStyleSheet("font-size: 24px; font-weight: bold;")
#     layout.addWidget(label)

#     exit_button = QPushButton("Exit")
#     exit_button.setStyleSheet("font-size: 18px; padding: 10px;")
#     exit_button.clicked.connect(lambda: sys.exit())  # Exit application
#     layout.addWidget(exit_button)

#     screen.setLayout(layout)
#     return screen
