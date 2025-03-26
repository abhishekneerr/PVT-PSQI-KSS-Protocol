import logging
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QRadioButton,
    QVBoxLayout, QPushButton, QHBoxLayout,
    QButtonGroup, QLabel
)
from PyQt6.QtCore import Qt
from utils.form_validator import submit_form_check
from utils.data_handler import save_to_csv

from src.state import state_manager

# 1) Import the custom translated widgets
from utils.translation_handler import tr, get_english_from_displayed
from utils.translated_widgets import (
    TranslatedLabel, TranslatedButton, TranslatedRadioButton
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def create_kss_beforePVT_screen(stack):
    """Creates the KSS Questionnaire Screen, screen #3"""
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # center the layout vertically

    participant_id = state_manager.get_participant_id()
    input_field_map = {}

    # 2) Use a TranslatedLabel for the KSS question
    kss_label = TranslatedLabel("kss_label")
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(kss_label)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # 3) Use TranslatedRadioButton keys for each option
    kss_options_keys = [
        "kss_option_1",
        "kss_option_2",
        "kss_option_3",
        "kss_option_4",
        "kss_option_5",
        "kss_option_6",
        "kss_option_7",
        "kss_option_8",
        "kss_option_9",
        "kss_option_10"
    ]

    kss_radio_layout = QVBoxLayout()
    kss_radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    kss_button_group = QButtonGroup()
    
    for key in kss_options_keys:
        radio_button = TranslatedRadioButton(key)
        radio_button.setStyleSheet("font-size: 16px;")
        kss_button_group.addButton(radio_button)
        kss_radio_layout.addWidget(radio_button)

    input_field_map[kss_button_group] = kss_label
    layout.addLayout(kss_radio_layout)

    # Submission message label
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    # Navigation
    nav_layout = QHBoxLayout()

    submit_button = TranslatedButton("kss_submit_button")

    def handle_submit():
        participant_id = state_manager.get_participant_id()
        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        # Validate
        submit_form_check(input_field_map, submission_message)

        # Check if the fill-required error is shown
        if tr("kss_fill_required") in submission_message.text():
            return  # Stop if not all questions are filled

        # If we get here, gather data
        form_data = {}
        for field, label in input_field_map.items():
            if isinstance(field, QLineEdit):
                form_data[label.text()] = field.text()
            elif isinstance(field, QButtonGroup):
                selected_button = field.checkedButton()
                if selected_button:
                    english_label = get_english_from_displayed(selected_button.text())
                    english_question = get_english_from_displayed(label.text())
                    form_data[english_question] = english_label

        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        save_to_csv(participant_id, "KSS_B", form_data)

        submission_message.setText(tr("kss_submit_success"))
        next_button.setEnabled(True)

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = TranslatedButton("kss_next_button")
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(4))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)
    return screen

def create_kss_afterPVT_screen(stack):
    """Creates the KSS Questionnaire Screen, screen #6 """
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    participant_id = state_manager.get_participant_id()
    input_field_map = {}

    kss_label = TranslatedLabel("kss_label")
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(kss_label)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    kss_options_keys = [
        "kss_option_1",
        "kss_option_2",
        "kss_option_3",
        "kss_option_4",
        "kss_option_5",
        "kss_option_6",
        "kss_option_7",
        "kss_option_8",
        "kss_option_9",
        "kss_option_10"
    ]

    kss_radio_layout = QVBoxLayout()
    kss_radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    kss_button_group = QButtonGroup()

    for key in kss_options_keys:
        radio_button = TranslatedRadioButton(key)
        radio_button.setStyleSheet("font-size: 16px;")
        kss_button_group.addButton(radio_button)
        kss_radio_layout.addWidget(radio_button)

    input_field_map[kss_button_group] = kss_label
    layout.addLayout(kss_radio_layout)

    # Submission message
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    nav_layout = QHBoxLayout()

    submit_button = TranslatedButton("kss_submit_button")

    def handle_submit():
        participant_id = state_manager.get_participant_id()
        
        submit_form_check(input_field_map, submission_message)
        
        # If the fill-required error is shown, stop
        if tr("kss_fill_required") in submission_message.text():
            return

        form_data = {}
        for field, label in input_field_map.items():
            if isinstance(field, QLineEdit):
                form_data[label.text()] = field.text()
            elif isinstance(field, QButtonGroup):
                selected_button = field.checkedButton()
                if selected_button:
                    english_label = get_english_from_displayed(selected_button.text())
                    english_question = get_english_from_displayed(label.text())
                    form_data[english_question] = english_label

        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        save_to_csv(participant_id, "KSS_A", form_data)

        submission_message.setText(tr("kss_submit_success"))
        next_button.setEnabled(True)

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = TranslatedButton("kss_next_button")
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(7))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)
    
    return screen
