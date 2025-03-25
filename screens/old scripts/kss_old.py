import logging
from PyQt6.QtWidgets import (
     QWidget, QLabel, QLineEdit, QRadioButton, 
    QVBoxLayout, QPushButton, QHBoxLayout, 
     QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from utils.form_validator import submit_form_check
from utils.data_handler import save_to_csv

from src.state import state_manager


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def create_kss_beforePVT_screen(stack):
    """Creates the KSS Questionnaire Screen, screen #3 """
    participant_id = state_manager.get_participant_id()
    # logging.info(f"Participant ID inside create_kss_beforePVT_screen: {participant_id}")
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout
    
    input_field_map = {}

    kss_label = QLabel("How sleepy do you feel right now?")
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Center the label
    layout.addWidget(kss_label)

    # add a line break
    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    kss_options = ["Extremely alert", "Very alert", "Alert", "Rather alert", 
                    "Neither alert nor sleepy", "Some signs of sleepiness", "Sleepy, but no effort to keep awake", 
                    "Sleepy, but some effort to keep awake", "Very sleepy, great effort to keep awake, fighting sleep", 
                    "Extremely sleepy, can't keep awake"]

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
    # back_button = QPushButton("Back")
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(2))
    # nav_layout.addWidget(back_button)

    submit_button = QPushButton("Submit")
    
    # log the participant_id
    # logging.debug(f"Current participant_id outside kss handle_submit: {participant_id}")
    def handle_submit():
        # Collect the data from the form (this is an example structure)
        participant_id = state_manager.get_participant_id()
        form_data = {}
        # logging.debug(f"Current participant_id inside kss handle submit: {participant_id}")
        if not participant_id:
            submission_message.setText("Error: ID is required!")
            return

        # Call the submit_form_check function as per your original logic
        submit_form_check(input_field_map, submission_message)
        
        # Check if there are any errors from submit_form_check
        if "Please fill all required questions (*)" in submission_message.text():
            return  # Do not proceed with saving if validation failed

        # Collect the data for text inputs
        for input_field, label in input_field_map.items():
            if isinstance(input_field, QLineEdit):  # Only for QLineEdit fields
                form_data[label.text()] = input_field.text()  # Save text entered

        # Collect the data for radio button selections
        for button_group, label in input_field_map.items():
            if isinstance(button_group, QButtonGroup):  # If it's a button group
                selected_button = button_group.checkedButton()
                if selected_button:  # Check if a button was selected
                    form_data[label.text()] = selected_button.text()


        # If participant_id is not set, show an error
        if not participant_id:
            submission_message.setText("Error: ID is required!")
            return

        # Save the form data to CSV
        questionnaire_type = "KSS_B"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Display success message
        submission_message.setText("Your responses have been submitted successfully! Click Next to proceed.")
        next_button.setEnabled(True)  # Enable the "Next" button

    
    
    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton("Next")
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

    kss_label = QLabel("How sleepy do you feel right now?")
    kss_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    kss_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Center the label
    layout.addWidget(kss_label)

    # add a line break
    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    kss_options = ["Extremely alert", "Very alert", "Alert", "Rather alert", 
                    "Neither alert nor sleepy", "Some signs of sleepiness", "Sleepy, but no effort to keep awake", 
                    "Sleepy, but some effort to keep awake", "Very sleepy, great effort to keep awake, fighting sleep", 
                    "Extremely sleepy, can't keep awake"]

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
    # back_button = QPushButton("Back")
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(5))
    # nav_layout.addWidget(back_button)

    submit_button = QPushButton("Submit")


    def handle_submit():
        # Collect the data from the form (this is an example structure)
        participant_id = state_manager.get_participant_id()
        form_data = {}
        # logging.debug(f"Current participant_id: {participant_id}")
    
        
        # Call the submit_form_check function as per your original logic
        submit_form_check(input_field_map, submission_message)
        
        # Check if there are any errors from submit_form_check
        if "Please fill all required questions (*)" in submission_message.text():
            return  # Do not proceed with saving if validation failed

        # Collect the data for text inputs
        for input_field, label in input_field_map.items():
            if isinstance(input_field, QLineEdit):  # Only for QLineEdit fields
                form_data[label.text()] = input_field.text()  # Save text entered

        # Collect the data for radio button selections
        for button_group, label in input_field_map.items():
            if isinstance(button_group, QButtonGroup):  # If it's a button group
                selected_button = button_group.checkedButton()
                if selected_button:  # Check if a button was selected
                    form_data[label.text()] = selected_button.text()


        # If participant_id is not set, show an error
        if not participant_id:
            submission_message.setText("Error: ID is required!")
            return

        # Save the form data to CSV
        questionnaire_type = "KSS_A"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Display success message
        submission_message.setText("Your responses have been submitted successfully! Click Next to proceed.")
        next_button.setEnabled(True)  # Enable the "Next" button



    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton("Next")
    next_button.setEnabled(False)  # Initially disabled
    next_button.clicked.connect(lambda: stack.setCurrentIndex(7))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)

    screen.setLayout(layout)
    
    return screen

