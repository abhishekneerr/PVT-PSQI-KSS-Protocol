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
# Import your custom translated widgets
from utils.translated_widgets import TranslatedLabel, TranslatedButton, TranslatedRadioButton, TranslatedLineEdit

def create_psqi_beforePVT_screen(stack):
    """Creates the PSQI Questionnaire Screen, screen #2"""

    screen = QWidget()
    layout = QVBoxLayout()

    input_field_map = {}
    participant_id = state_manager.get_participant_id()

    #
    # Helper function to create a text question + line edit
    #
    def create_lineText_question(question_key, layout, placeholder_key):
        """
        Creates a line question with a TranslatedLabel using the raw KEY (not tr(...)) 
        and a QLineEdit with an optional translated placeholder.
        """
        # Use the key directly for TranslatedLabel
        label = TranslatedLabel(question_key)
        input_field = TranslatedLineEdit(placeholder_key)
        # For placeholders, calling tr(...) is OK if you don’t need them to auto-refresh 
        # input_field.setPlaceholderText(tr(placeholder_key))
        input_field.setMaximumWidth(600)
        layout.addWidget(label)
        layout.addWidget(input_field)

        input_field_map[input_field] = label

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)

    #
    # Helper function to add sub-questions with standard 4 radio choices
    #
    def add_sub_question(label_key):
        """Adds a label + radio group for standard 4 PSQI answer choices."""
        question_layout = QVBoxLayout()
        # Key to TranslatedLabel
        label = TranslatedLabel(label_key)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        # Here we pass KEYS to TranslatedRadioButton
        answer_keys = [
            "psqi_answer_not_during_past_month",
            "psqi_answer_less_than_once_week",
            "psqi_answer_once_twice_week",
            "psqi_answer_three_or_more_week"
        ]
        for choice_key in answer_keys:
            radio_button = TranslatedRadioButton(choice_key)
            button_group.addButton(radio_button)
            radio_layout.addWidget(radio_button)

        question_layout.addLayout(radio_layout)
        input_field_map[button_group] = label  # Store mapping
        layout.addLayout(question_layout)

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)
        layout.update()

    #
    # Helper function for question #11 with special answer set (incl. "Not applicable")
    #
    def add_sub_question_11(label_key):
        """Adds a label + radio group for question #11 with 5 choices (including 'Not applicable')."""
        question_layout = QVBoxLayout()
        label = TranslatedLabel(label_key)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        # We include "Not applicable" raw text if needed,
        # or you could add a dictionary key for it if you want it to be translated too
        answer_choices_notApplicable = [
            "psqi_answer_not_during_past_month",
            "psqi_not_applicable",  # We'll handle this carefully below
            "psqi_answer_less_than_once_week",
            "psqi_answer_once_twice_week",
            "psqi_answer_three_or_more_week"
        ]

        for choice in answer_choices_notApplicable:
            if choice == "not_applicable_raw":
                # Hard-coded string if you truly need "Not applicable" un-translated
                radio_button = TranslatedRadioButton("psqi_not_applicable") 
            else:
                # Otherwise, pass the key to TranslatedRadioButton
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
    # Instruction Text with combining underlines (\u0332) and line breaks (\n) 
    # and "Instruction" in bold
    # Instead of passing tr(...) to TranslatedLabel, pass the key directly if you have one.
    # If you only have raw text, you'd either create a new dictionary key or do a custom approach.
    # Suppose you have "psqi_instructions_1" in your JSON. We'll pass that key to TranslatedLabel directly:

    instructionslabel = TranslatedLabel("psqi_instructions_1")
    instructionslabel.setWordWrap(True)
    instructionslabel.setStyleSheet("font-size: 14px;")
    layout.addWidget(instructionslabel)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    ## NOTE: We reference our JSON keys for each question & placeholder
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
    instructionslabel2 = TranslatedLabel("psqi_instructions_2")
    instructionslabel2.setWordWrap(True)
    instructionslabel2.setStyleSheet("font-size: 14px; font-weight: bold;")
    layout.addWidget(instructionslabel2)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Fifth question: TROUBLE SLEEPING
    psqiQuestion5B_label = TranslatedLabel("psqi_part2_header")
    layout.addWidget(psqiQuestion5B_label)

    # Sub-questions share the same 4 radio choices
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
    psqiQuestion6B_label = TranslatedLabel("psqi_q6_label")
    layout.addWidget(psqiQuestion6B_label)

    psqiQuestion6B_radio_layout = QVBoxLayout()
    psqiQuestion6B_button_group = QButtonGroup()

    # We'll pass the KEYS for each choice
    q6_choice_keys = [
        "psqi_q6_choices_very_good",
        "psqi_q6_choices_fairly_good",
        "psqi_q6_choices_fairly_bad",
        "psqi_q6_choices_very_bad"
    ]
    for choice_key in q6_choice_keys:
        radio_button = TranslatedRadioButton(choice_key)
        psqiQuestion6B_button_group.addButton(radio_button)
        psqiQuestion6B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion6B_radio_layout)
    input_field_map[psqiQuestion6B_button_group] = psqiQuestion6B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Seventh question
    psqiQuestion7B_label = TranslatedLabel("psqi_q7_label")
    layout.addWidget(psqiQuestion7B_label)

    psqiQuestion7B_radio_layout = QHBoxLayout()
    psqiQuestion7B_button_group = QButtonGroup()

    for choice_key in [
        "psqi_answer_not_during_past_month",
        "psqi_answer_less_than_once_week",
        "psqi_answer_once_twice_week",
        "psqi_answer_three_or_more_week"
    ]:
        radio_button = TranslatedRadioButton(choice_key)
        psqiQuestion7B_button_group.addButton(radio_button)
        psqiQuestion7B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion7B_radio_layout)
    input_field_map[psqiQuestion7B_button_group] = psqiQuestion7B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Eighth question
    psqiQuestion8B_label = TranslatedLabel("psqi_q8_label")
    layout.addWidget(psqiQuestion8B_label)

    psqiQuestion8B_radio_layout = QHBoxLayout()
    psqiQuestion8B_button_group = QButtonGroup()

    for choice_key in [
        "psqi_answer_not_during_past_month",
        "psqi_answer_less_than_once_week",
        "psqi_answer_once_twice_week",
        "psqi_answer_three_or_more_week"
    ]:
        radio_button = TranslatedRadioButton(choice_key)
        psqiQuestion8B_button_group.addButton(radio_button)
        psqiQuestion8B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion8B_radio_layout)
    input_field_map[psqiQuestion8B_button_group] = psqiQuestion8B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Ninth question
    psqiQuestion9B_label = TranslatedLabel("psqi_q9_label")
    layout.addWidget(psqiQuestion9B_label)

    psqiQuestion9B_radio_layout = QVBoxLayout()
    psqiQuestion9B_button_group = QButtonGroup()

    for choice_key in [
        "psqi_q9_no_problem",
        "psqi_q9_slight_problem",
        "psqi_q9_somewhat_problem",
        "psqi_q9_very_big_problem"
    ]:
        radio_button = TranslatedRadioButton(choice_key)
        psqiQuestion9B_button_group.addButton(radio_button)
        psqiQuestion9B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion9B_radio_layout)
    input_field_map[psqiQuestion9B_button_group] = psqiQuestion9B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # ----------------------PSQI PART 4--------------------
    # Tenth question
    psqiQuestion10B_label = TranslatedLabel("psqi_q10_label")
    layout.addWidget(psqiQuestion10B_label)

    psqiQuestion10B_radio_layout = QVBoxLayout()
    psqiQuestion10B_button_group = QButtonGroup()

    for choice_key in [
        "psqi_q10_no_partner",
        "psqi_q10_other_room",
        "psqi_q10_same_room_not_bed",
        "psqi_q10_same_bed"
    ]:
        radio_button = TranslatedRadioButton(choice_key)
        psqiQuestion10B_button_group.addButton(radio_button)
        psqiQuestion10B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion10B_radio_layout)
    input_field_map[psqiQuestion10B_button_group] = psqiQuestion10B_label

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    psqiQuestion11B_label = TranslatedLabel("psqi_q11_label")
    layout.addWidget(psqiQuestion11B_label)

    add_sub_question_11("psqi_q11_a")
    add_sub_question_11("psqi_q11_b")
    add_sub_question_11("psqi_q11_c")
    add_sub_question_11("psqi_q11_d")

    # Special case for 11.e (text input + radio buttons)
    # If you want a fully dynamic placeholder, you'd also need a custom TranslatedLineEdit
    psqiQuestion11eB_label = TranslatedLabel("psqi_q11_e_label")
    psqiQuestion11eB_input = TranslatedLineEdit("psqi_q11_e_placeholder")
    # psqiQuestion11eB_input.setPlaceholderText(tr("psqi_q11_e_placeholder"))
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
        # Collect the data from the form
        participant_id = state_manager.get_participant_id()
        form_data = {}

        # Validate required fields
        submit_form_check(input_field_map, submission_message)
        
        # If validation fails, submission_message includes "Please fill all..."
        if "Please fill all required questions (*" in submission_message.text():
            return
        
        if "Veuillez remplir toutes les questions requises (*)" in submission_message.text():
            return

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

        if not participant_id:
            submission_message.setText("Error: ID is required!")
            return

        # Save the form data
        questionnaire_type = "PSQI_B"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Show success message
        submission_message.setText(tr("psqi_submit_success"))
        next_button.setEnabled(True)

    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton(tr("next_button"))
    next_button.setEnabled(False)
    next_button.clicked.connect(lambda: stack.setCurrentIndex(3))
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)

    # Make the screen scrollable
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    scroll_widget.setLayout(layout)
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)

    screen_layout = QVBoxLayout()
    screen_layout.addWidget(scroll_area)
    screen.setLayout(screen_layout)

    return screen
