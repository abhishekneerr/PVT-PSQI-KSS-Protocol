from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QRadioButton, 
    QVBoxLayout, QPushButton, QHBoxLayout, 
    QScrollArea, QButtonGroup
)
from PyQt6.QtCore import Qt
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from utils.form_validator import submit_form_check
from utils.data_handler import save_to_csv
from src.state import state_manager

# Import the translation function
from utils.translation_handler import tr
from utils.translated_widgets import TranslatedLabel, TranslatedButton, TranslatedRadioButton

def create_psqi_beforePVT_screen(stack):
    """Creates the PSQI Questionnaire Screen, screen #2"""

    screen = QWidget()
    layout = QVBoxLayout()

    input_field_map = {}
    participant_id = state_manager.get_participant_id()

    def create_lineText_question(question_key, layout, placeholder_key):
        """Helper function to create a line question with a label and input field"""
        label_text = tr(question_key)
        label = TranslatedLabel(label_text)
        input_field = QLineEdit()
        input_field.setPlaceholderText(tr(placeholder_key))
        input_field.setMaximumWidth(600)
        layout.addWidget(label)
        layout.addWidget(input_field)

        input_field_map[input_field] = label

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)

    def add_sub_question(label_key):
        """Helper function to add radio button questions"""
        question_layout = QVBoxLayout()
        label_text = tr(label_key)
        label = TranslatedLabel(label_text)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        # We'll use the standard 4 choices (Not during the past month, etc.)
        answer_options = [
            tr("psqi_answer_not_during_past_month"),
            tr("psqi_answer_less_than_once_week"),
            tr("psqi_answer_once_twice_week"),
            tr("psqi_answer_three_or_more_week")
        ]
        for choice in answer_options:
            radio_button = TranslatedRadioButton(choice)
            button_group.addButton(radio_button)
            radio_layout.addWidget(radio_button)

        question_layout.addLayout(radio_layout)
        input_field_map[button_group] = label  # Store mapping in dictionary
        layout.addLayout(question_layout)  # Add to passed layout

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)
        layout.update()

    def add_sub_question_11(label_key):
        """Helper function to add radio button questions for question #11 with special answer choices"""
        question_layout = QVBoxLayout()
        label_text = tr(label_key)
        label = TranslatedLabel(label_text)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        # Special 'Not applicable' answer set
        answer_choices_notApplicable = [
            tr("psqi_answer_not_during_past_month"),      # "Not during the past month"
            "Not applicable",  # If you truly need a "Not applicable" or "No partner" option
            tr("psqi_answer_less_than_once_week"),
            tr("psqi_answer_once_twice_week"),
            tr("psqi_answer_three_or_more_week")
        ]

        for choice in answer_choices_notApplicable:
            radio_button = TranslatedRadioButton(choice)
            button_group.addButton(radio_button)
            radio_layout.addWidget(radio_button)

        question_layout.addLayout(radio_layout)
        input_field_map[button_group] = label
        layout.addLayout(question_layout)

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)
        layout.update()

    # ----------------------PSQI PART 1--------------------
    # Instruction Text with combining underlines (\u0332) and line breaks (\n) and "Instruction" in bold
    instruction_text = tr("psqi_instructions_1")
    instructionslabel = TranslatedLabel(instruction_text, alignment=Qt.AlignmentFlag.AlignTop)
    instructionslabel.setWordWrap(True)
    instructionslabel.setStyleSheet("font-size: 14px;")
    layout.addWidget(instructionslabel)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # NOTE: We reference our JSON keys for each question & placeholder
    part1_psqi_questions = [
        ("psqi_part1_q1_weekday", "psqi_part1_q1_placeholder"),
        ("psqi_part1_q2_weekend", "psqi_part1_q2_placeholder"),
        ("psqi_part1_q3_wakeup_weekday", "psqi_part1_q3_placeholder"),
        ("psqi_part1_q4_wakeup_weekend", "psqi_part1_q4_placeholder"),
        ("psqi_part1_q5_sleep_latency", "psqi_part1_q5_placeholder"),
        ("psqi_part1_q6_actual_sleep", "psqi_part1_q6_placeholder"),
    ]

    for question_key, placeholder_key in part1_psqi_questions:
        create_lineText_question(question_key, layout, placeholder_key)

    # ----------------------PSQI PART 2--------------------
    # Additional instruction
    instruction_text2 = tr("psqi_instructions_2")
    instructionslabel2 = TranslatedLabel(instruction_text2, alignment=Qt.AlignmentFlag.AlignTop)
    instructionslabel2.setWordWrap(True)
    instructionslabel2.setStyleSheet("font-size: 14px; font-weight: bold;")
    layout.addWidget(instructionslabel2)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Fifth question: TROUBLE SLEEPING
    psqiQuestion5B_label = TranslatedLabel(tr("psqi_part2_header"))
    layout.addWidget(psqiQuestion5B_label)

    # These sub-questions share the same 4 radio choices
    add_sub_question("psqi_part2_a")
    add_sub_question("psqi_part2_b")
    add_sub_question("psqi_part2_c")
    add_sub_question("psqi_part2_d")
    add_sub_question("psqi_part2_e")
    add_sub_question("psqi_part2_f")
    add_sub_question("psqi_part2_g")
    add_sub_question("psqi_part2_h")
    add_sub_question("psqi_part2_i")

    # j) text input + sub question
    create_lineText_question("psqi_part2_j", layout, "psqi_part2_j_placeholder")

    add_sub_question("psqi_part2_frequency")

    # ----------------------PSQI PART 3--------------------
    # Sixth question: SLEEP QUALITY
    psqiQuestion6B_label = TranslatedLabel(tr("psqi_q6_label"))
    layout.addWidget(psqiQuestion6B_label)

    psqiQuestion6B_radio_layout = QVBoxLayout()
    psqiQuestion6B_button_group = QButtonGroup()

    # "Very good", "Fairly good", "Fairly bad", "Very bad"
    q6_choices = [
        tr("psqi_q6_choices_very_good"),
        tr("psqi_q6_choices_fairly_good"),
        tr("psqi_q6_choices_fairly_bad"),
        tr("psqi_q6_choices_very_bad")
    ]
    for choice in q6_choices:
        radio_button = TranslatedRadioButton(choice)
        psqiQuestion6B_button_group.addButton(radio_button)
        psqiQuestion6B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion6B_radio_layout)
    input_field_map[psqiQuestion6B_button_group] = psqiQuestion6B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Seventh question
    psqiQuestion7B_label = TranslatedLabel(tr("psqi_q7_label"))
    layout.addWidget(psqiQuestion7B_label)

    psqiQuestion7B_radio_layout = QHBoxLayout()
    psqiQuestion7B_button_group = QButtonGroup()

    # The same 4 standard answer choices
    for choice in [
        tr("psqi_answer_not_during_past_month"),
        tr("psqi_answer_less_than_once_week"),
        tr("psqi_answer_once_twice_week"),
        tr("psqi_answer_three_or_more_week")
    ]:
        radio_button = TranslatedRadioButton(choice)
        psqiQuestion7B_button_group.addButton(radio_button)
        psqiQuestion7B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion7B_radio_layout)
    input_field_map[psqiQuestion7B_button_group] = psqiQuestion7B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Eighth question
    psqiQuestion8B_label = TranslatedLabel(tr("psqi_q8_label"))
    layout.addWidget(psqiQuestion8B_label)

    psqiQuestion8B_radio_layout = QHBoxLayout()
    psqiQuestion8B_button_group = QButtonGroup()

    for choice in [
        tr("psqi_answer_not_during_past_month"),
        tr("psqi_answer_less_than_once_week"),
        tr("psqi_answer_once_twice_week"),
        tr("psqi_answer_three_or_more_week")
    ]:
        radio_button = TranslatedRadioButton(choice)
        psqiQuestion8B_button_group.addButton(radio_button)
        psqiQuestion8B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion8B_radio_layout)
    input_field_map[psqiQuestion8B_button_group] = psqiQuestion8B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Ninth question
    psqiQuestion9B_label = TranslatedLabel(tr("psqi_q9_label"))
    layout.addWidget(psqiQuestion9B_label)

    psqiQuestion9B_radio_layout = QVBoxLayout()
    psqiQuestion9B_button_group = QButtonGroup()

    for choice in [
        tr("psqi_q9_no_problem"),
        tr("psqi_q9_slight_problem"),
        tr("psqi_q9_somewhat_problem"),
        tr("psqi_q9_very_big_problem")
    ]:
        radio_button = TranslatedRadioButton(choice)
        psqiQuestion9B_button_group.addButton(radio_button)
        psqiQuestion9B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion9B_radio_layout)
    input_field_map[psqiQuestion9B_button_group] = psqiQuestion9B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # ----------------------PSQI PART 4--------------------
    # Tenth question
    psqiQuestion10B_label = TranslatedLabel(tr("psqi_q10_label"))
    layout.addWidget(psqiQuestion10B_label)

    psqiQuestion10B_radio_layout = QVBoxLayout()
    psqiQuestion10B_button_group = QButtonGroup()

    for choice in [
        tr("psqi_q10_no_partner"),
        tr("psqi_q10_other_room"),
        tr("psqi_q10_same_room_not_bed"),
        tr("psqi_q10_same_bed")
    ]:
        radio_button = TranslatedRadioButton(choice)
        psqiQuestion10B_button_group.addButton(radio_button)
        psqiQuestion10B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion10B_radio_layout)
    input_field_map[psqiQuestion10B_button_group] = psqiQuestion10B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    psqiQuestion11B_label = TranslatedLabel(tr("psqi_q11_label"))
    layout.addWidget(psqiQuestion11B_label)

    add_sub_question_11("psqi_q11_a")
    add_sub_question_11("psqi_q11_b")
    add_sub_question_11("psqi_q11_c")
    add_sub_question_11("psqi_q11_d")

    # Special case for 11.e (text input + radio buttons)
    psqiQuestion11eB_label = QLabel(tr("psqi_q11_e_label"))
    psqiQuestion11eB_input = QLineEdit()
    psqiQuestion11eB_input.setPlaceholderText(tr("psqi_q11_e_placeholder"))
    layout.addWidget(psqiQuestion11eB_label)
    layout.addWidget(psqiQuestion11eB_input)
    input_field_map[psqiQuestion11eB_input] = psqiQuestion11eB_label

    # Add radio button choices for 11.e
    add_sub_question_11("psqi_q11_frequency")

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # .--------------End of psqi questionnaire-----------------.

    # Label to display form submission message or error message
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    # Navigation Buttons
    nav_layout = QHBoxLayout()

    submit_button = QPushButton(tr("psqi_submit_button"))

    def handle_submit():
        # Collect the data from the form (this is an example structure)
        participant_id = state_manager.get_participant_id()
        form_data = {}

        # Call the submit_form_check function as per your original logic
        submit_form_check(input_field_map, submission_message)
        
        # Check if there are any errors from submit_form_check
        if "Please fill all required questions (*)" in submission_message.text():
            return  # Do not proceed with saving if validation failed

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

        # If participant_id is not set, show an error
        if not participant_id:
            submission_message.setText("Error: ID is required!")
            return

        # Save the form data to CSV
        questionnaire_type = "PSQI_B"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Display success message
        submission_message.setText(tr("psqi_submit_success"))
        next_button.setEnabled(True)  # Enable the "Next" button

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton(tr("next_button"))  # If you want "Next" also localized, use tr("next_button")
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(3))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)

    # Scrollable screen
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    scroll_widget.setLayout(layout)
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)

    screen_layout = QVBoxLayout()
    screen_layout.addWidget(scroll_area)
    screen.setLayout(screen_layout)

    return screen


