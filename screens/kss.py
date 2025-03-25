import logging
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QRadioButton,
    QVBoxLayout, QPushButton, QHBoxLayout,
    QButtonGroup
)
from PyQt6.QtCore import Qt
from utils.form_validator import submit_form_check
from utils.data_handler import save_to_csv

from src.state import state_manager
# 1) Import the translation helper
from utils.translation_handler import tr

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_kss_beforePVT_screen(stack):
    """Creates the KSS Questionnaire Screen, screen #3 """
    participant_id = state_manager.get_participant_id()
    # logging.info(f"Participant ID inside create_kss_beforePVT_screen: {participant_id}")
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout
    
    input_field_map = {}

    # 2) Use tr("kss_label")
    kss_label = QLabel(tr("kss_label"))
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Center the label
    layout.addWidget(kss_label)

    # add a line break
    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # 3) Translate each KSS option
    kss_options = [
        tr("kss_option_1"),
        tr("kss_option_2"),
        tr("kss_option_3"),
        tr("kss_option_4"),
        tr("kss_option_5"),
        tr("kss_option_6"),
        tr("kss_option_7"),
        tr("kss_option_8"),
        tr("kss_option_9"),
        tr("kss_option_10")
    ]

    kss_radio_layout = QVBoxLayout()
    kss_radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the radio buttons layout
    kss_button_group = QButtonGroup()
    
    for option in kss_options:
        radio_button = QRadioButton(option)
        radio_button.setStyleSheet("font-size: 16px;")  # Increase font size
        kss_button_group.addButton(radio_button)
        kss_radio_layout.addWidget(radio_button)

    input_field_map[kss_button_group] = kss_label
    layout.addLayout(kss_radio_layout)

    # Navigation Buttons
    # Label to display form submission message or error message
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    # Navigation Buttons
    nav_layout = QHBoxLayout()

    # 4) Translate "Submit"
    submit_button = QPushButton(tr("kss_submit_button"))
    
    def handle_submit():
        # Collect the data from the form (this is an example structure)
        participant_id = state_manager.get_participant_id()
        form_data = {}
        # logging.debug(f"Current participant_id inside kss handle submit: {participant_id}")

        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        # Call the submit_form_check function as per your original logic
        submit_form_check(input_field_map, submission_message)
        
        # Check if there are any errors from submit_form_check
        if tr("kss_fill_required") in submission_message.text():
            return  # Do not proceed with saving if validation failed

        # Collect data for text inputs
        for input_field, label in input_field_map.items():
            if isinstance(input_field, QLineEdit):
                form_data[label.text()] = input_field.text()

        # Collect data for radio button selections
        for button_group, label in input_field_map.items():
            if isinstance(button_group, QButtonGroup):
                selected_button = button_group.checkedButton()
                if selected_button:
                    form_data[label.text()] = selected_button.text()

        # If participant_id is not set, show an error
        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        # Save the form data to CSV
        questionnaire_type = "KSS_B"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Display success message
        submission_message.setText(tr("kss_submit_success"))
        next_button.setEnabled(True)  # Enable the "Next" button

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    # 5) Translate "Next" (optional if you want the button localized)
    next_button = QPushButton(tr("kss_next_button"))
    next_button.setEnabled(False)  # Initially disabled
    next_button.clicked.connect(lambda: stack.setCurrentIndex(4))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)

    screen.setLayout(layout)
    return screen


def create_kss_afterPVT_screen(stack):
    """Creates the KSS Questionnaire Screen, screen #6 """
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout

    participant_id = state_manager.get_participant_id()
    input_field_map = {}

    kss_label = QLabel(tr("kss_label"))
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Center the label
    layout.addWidget(kss_label)

    # add a line break
    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    kss_options = [
        tr("kss_option_1"),
        tr("kss_option_2"),
        tr("kss_option_3"),
        tr("kss_option_4"),
        tr("kss_option_5"),
        tr("kss_option_6"),
        tr("kss_option_7"),
        tr("kss_option_8"),
        tr("kss_option_9"),
        tr("kss_option_10")
    ]

    kss_radio_layout = QVBoxLayout()
    kss_radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    kss_button_group = QButtonGroup()
    
    for option in kss_options:
        radio_button = QRadioButton(option)
        radio_button.setStyleSheet("font-size: 16px;")
        kss_button_group.addButton(radio_button)
        kss_radio_layout.addWidget(radio_button)

    input_field_map[kss_button_group] = kss_label
    layout.addLayout(kss_radio_layout)

    # Navigation Buttons
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    nav_layout = QHBoxLayout()
    submit_button = QPushButton(tr("kss_submit_button"))

    def handle_submit():
        participant_id = state_manager.get_participant_id()
        form_data = {}
        
        submit_form_check(input_field_map, submission_message)
        
        if tr("kss_fill_required") in submission_message.text():
            return  # Validation failed

        # Collect the data for text inputs
        for input_field, label in input_field_map.items():
            if isinstance(input_field, QLineEdit):
                form_data[label.text()] = input_field.text()

        # Collect the data for radio button selections
        for button_group, label in input_field_map.items():
            if isinstance(button_group, QButtonGroup):
                selected_button = button_group.checkedButton()
                if selected_button:
                    form_data[label.text()] = selected_button.text()

        if not participant_id:
            submission_message.setText(tr("kss_error_id_required"))
            return

        questionnaire_type = "KSS_A"
        save_to_csv(participant_id, questionnaire_type, form_data)

        submission_message.setText(tr("kss_submit_success"))
        next_button.setEnabled(True)

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton(tr("kss_next_button"))
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(7))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)

    screen.setLayout(layout)
    
    return screen
