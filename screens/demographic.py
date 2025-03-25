# screens/demographic.py
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QSpinBox, QHBoxLayout, QVBoxLayout, QButtonGroup
)
from PyQt6.QtCore import Qt
from utils.data_handler import save_to_csv
from utils.translation_handler import tr
from src.state import state_manager
# 1) Import your custom classes
from utils.translated_widgets import (
    TranslatedLabel, TranslatedButton, TranslatedRadioButton
)

def create_demographic_form(stack):
    screen = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    input_field_map = {}

    def add_label_input_pair(label_key, input_widget):
        # 2) Use TranslatedLabel for the label
        label = TranslatedLabel(label_key)
        layout.addWidget(label)
        layout.addWidget(input_widget)
        input_field_map[input_widget] = label

    # Name
    name_input = QLineEdit()
    name_input.setMaximumWidth(500)
    add_label_input_pair("id_label", name_input)

    # Age
    age_input = QSpinBox()
    age_input.setRange(1, 120)
    age_input.setMaximumWidth(500)
    add_label_input_pair("age_label", age_input)

    # Gender
    # 3) Use TranslatedLabel for the "Gender:" label
    gender_label = TranslatedLabel("gender_label")
    layout.addWidget(gender_label)

    gender_layout = QHBoxLayout()
    gender_button_group = QButtonGroup()

    # 4) For each radio button, use TranslatedRadioButton
    gender_options = ["male_label", "female_label", "other_label"]
    for gender_key in gender_options:
        rb = TranslatedRadioButton(gender_key)
        gender_button_group.addButton(rb)
        gender_layout.addWidget(rb)

    layout.addLayout(gender_layout)
    input_field_map[gender_button_group] = gender_label

    # Country
    country_input = QLineEdit()
    country_input.setMaximumWidth(500)
    add_label_input_pair("country_label", country_input)

    # Submission message (error or success)
    submission_message = TranslatedLabel("")  # or a plain QLabel if you prefer
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    # But note if you give it an empty key, it won't do anything. We'll set dynamic text below.
    layout.addWidget(submission_message)

    # Navigation buttons
    nav_layout = QHBoxLayout()

    back_button = TranslatedButton("back_button")
    back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
    nav_layout.addWidget(back_button)

    submit_button = TranslatedButton("submit_button")
    nav_layout.addWidget(submit_button)

    next_button = TranslatedButton("next_button")
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(2))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)

    # 5) The form submission logic
    def handle_submit():
        participant_id = name_input.text().strip()
        state_manager.set_participant_id(participant_id)

        if not participant_id:
            # For error messages, you might just call setText(tr("error_id_required"))
            submission_message.setText(tr("error_id_required"))
            return

        age = age_input.value()
        country = country_input.text().strip()

        selected_gender = None
        for btn in gender_button_group.buttons():
            if btn.isChecked():
                selected_gender = btn.text()
                break

        if not selected_gender:
            submission_message.setText(tr("error_gender_required"))
            return

        if not country:
            submission_message.setText(tr("error_country_required"))
            return

        demographic_data = {
            "ID": participant_id,
            "Age": age,
            "Gender": selected_gender,
            "Country": country,
        }

        save_to_csv(participant_id, "demo", demographic_data)

        submission_message.setStyleSheet("font-size: 12px; color: green;")
        submission_message.setText(tr("success_submission"))
        next_button.setEnabled(True)

    submit_button.clicked.connect(handle_submit)

    return screen



# old code, before translation:::::-----------------------------------------------------------------------


# import logging

# from PyQt6.QtWidgets import ( QWidget, QLabel, QLineEdit, QRadioButton, 
#     QVBoxLayout, QPushButton, QSpinBox, QHBoxLayout, 
#      QRadioButton, QButtonGroup
# )
# from PyQt6.QtCore import Qt

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# from utils.data_handler import save_to_csv

# from src.state import state_manager



# def create_demographic_form(stack):
#     """Creates the Demographic Data Form screen #1"""
#     # participant_id = state_manager.get_participant_id()
#     # logging.info(f"Participant ID inside create_demographic_form: {participant_id}")
#     screen = QWidget()
#     layout = QVBoxLayout()
#     layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout

#     input_field_map = {}

#     def add_label_input_pair(label_text, input_widget):
#         """Helper function to add a label and input widget to the layout"""
#         label = QLabel(label_text)
#         layout.addWidget(label)
#         layout.addWidget(input_widget)
#         input_field_map[input_widget] = label  # Store mapping in dictionary

#     # Name
#     name_input = QLineEdit()
#     name_input.setMaximumWidth(500)
#     add_label_input_pair("ID:", name_input)

#     # Age
#     age_input = QSpinBox()
#     age_input.setRange(1, 120)
#     age_input.setMaximumWidth(500)
#     add_label_input_pair("Age:", age_input)

#     # Gender
#     gender_label = QLabel("Gender:")
#     gender_layout = QHBoxLayout()
#     gender_button_group = QButtonGroup()
#     for gender in ["Male", "Female", "Other"]:
#         radio_button = QRadioButton(gender)
#         gender_button_group.addButton(radio_button)
#         gender_layout.addWidget(radio_button)
#     layout.addWidget(gender_label)
#     layout.addLayout(gender_layout)
#     input_field_map[gender_button_group] = gender_label  # Store mapping in dictionary

#     # Country
#     country_input = QLineEdit()
#     country_input.setMaximumWidth(500)
#     add_label_input_pair("Country:", country_input)

#     # Navigation Buttons
#     # Label to display form submission message or error message
#     submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
#     submission_message.setStyleSheet("font-size: 12px; color: red;")
#     layout.addWidget(submission_message)

#     # Navigation Buttons
#     nav_layout = QHBoxLayout()

#     back_button = QPushButton("Back")
#     back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
#     nav_layout.addWidget(back_button)

#     def handle_submit():
#         """Handles form submission, validates input, and saves data to CSV"""
#         global participant_id
#         #participant_id = name_input.text().strip()  # Corrected to name_input
#         participant_id = name_input.text().strip()
#         state_manager.set_participant_id(participant_id)
        
#         if not participant_id:
#             submission_message.setText("Error: ID is required!")
#             return
        
#         # logging.debug(f"Current participant_id in dmeographic.py: {participant_id}")

#         age = age_input.value()
#         country = country_input.text().strip()
        
#         selected_gender = None
#         for btn in gender_button_group.buttons():  # Corrected to use gender_button_group
#             if btn.isChecked():
#                 selected_gender = btn.text()
#                 break

#         if not selected_gender:
#             submission_message.setText("Error: Please select a gender!")
#             return

#         if not country:
#             submission_message.setText("Error: Country is required!")
#             return

#         # Store data in a dictionary
#         demographic_data = {
#             "ID": participant_id,
#             "Age": age,
#             "Gender": selected_gender,
#             "Country": country,
#         }

#         # Save data to CSV
#         save_to_csv(participant_id, "demo", demographic_data)

#         # Enable next button and show success message
#         submission_message.setStyleSheet("font-size: 12px; color: green;")
#         submission_message.setText(f"Data submiteed, please click next to proceed.")
#         next_button.setEnabled(True)

#     submit_button = QPushButton("Submit")
#     submit_button.clicked.connect(handle_submit)
#     nav_layout.addWidget(submit_button)

#     next_button = QPushButton("Next")
#     next_button.setEnabled(False)  # Initially disabled
#     nav_layout.addWidget(next_button)
#     next_button.clicked.connect(lambda: stack.setCurrentIndex(2)) # change to 2

#     layout.addLayout(nav_layout)
#     screen.setLayout(layout)

#     return screen
