from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QRadioButton, 
    QVBoxLayout, QPushButton, QHBoxLayout, 
    QScrollArea, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


from utils.form_validator import submit_form_check
from utils.data_handler import save_to_csv


from src.state import state_manager


def create_psqi_beforePVT_screen(stack):
    """Creates the PSQI Questionnaire Screen, screen #2"""

    screen = QWidget()
    layout = QVBoxLayout()

    input_field_map = {}
    participant_id = state_manager.get_participant_id()

    def create_lineText_question(label, layout, placeholder_text):
        """Helper function to create a line question with a label and input field"""
        label = QLabel(label)
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setMaximumWidth(600)
        layout.addWidget(label)
        layout.addWidget(input_field)

        input_field_map[input_field] = label

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)


    def add_sub_question(label_text):
        """Helper function to add radio button questions"""
        question_layout = QVBoxLayout()
        label = QLabel(label_text)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        for choice in answer_choices:
            radio_button = QRadioButton(choice)
            button_group.addButton(radio_button)
            radio_layout.addWidget(radio_button)

        question_layout.addLayout(radio_layout)
        input_field_map[button_group] = label  # Store mapping in dictionary
        layout.addLayout(question_layout)  # Add to passed layout

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)

        layout.update()

    
        # Possible choices for all sub-questions
    
    answer_choices_notApplicable = [
        "Not applicable",
        "Not during the past month",
        "Less than once a week",
        "Once or twice a week",
        "Three or more times a week",
        
    ]

    def add_sub_question_11(label_text):
        """Helper function to add radio button questions"""
        question_layout = QVBoxLayout()
        label = QLabel(label_text)
        question_layout.addWidget(label)

        radio_layout = QHBoxLayout()
        button_group = QButtonGroup()

        for choice in answer_choices_notApplicable:
            radio_button = QRadioButton(choice)
            button_group.addButton(radio_button)
            radio_layout.addWidget(radio_button)

        question_layout.addLayout(radio_layout)
        input_field_map[button_group] = label  # Store mapping in dictionary
        layout.addLayout(question_layout)  # Add to passed layout

        linebreak = QLabel("\n")
        layout.addWidget(linebreak)

        layout.update()

    # ----------------------PSQI PART 1--------------------
    # Instruction Text with combining underlines (\u0332) and line breaks (\n) and "Instruction" in bold
    instruction_text = (
        "INSTRUCTIONS:\n\n"
        "The following questions relate to your usual sleep habits during the past month "
        + "\u0332".join("only") + ".\n"
        "Your answers should indicate the most accurate reply for the "
        + "\u0332".join("majority") + " of days and nights in the past month.\n"
        "Please answer all questions."
    )
    instructionslabel = QLabel(instruction_text, alignment=Qt.AlignmentFlag.AlignTop)
    instructionslabel.setWordWrap(True)
    instructionslabel.setStyleSheet("font-size: 14px;")
    layout.addWidget(instructionslabel)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    
    part1_psqi_questions = [
        ("1. During the past month, what time have you usually gone to bed on weekdays?",
        "Enter time in 24-hour format (HH:MM), e.g. 22:30"),

        ("2. During the past month, what time have you usually gone to bed on weekends?",
        "Enter time in 24-hour format (HH:MM), e.g. 00:30"),

        ("3. During the past month, what time have you usually gotten up on weekdays?",
        "Enter time in 24-hour format (HH:MM), e.g. 07:00"),

        ("4. During the past month, what time have you usually gotten up on weekends?",
        "Enter time in 24-hour format (HH:MM), e.g. 09:00"),

        ("5. During the past month, how long (in minutes) has it usually taken you to fall asleep each night?",
        "Enter number of minutes, e.g. 15"),

        ("6. During the past month, how many hours of actual sleep did you get at night (not just time in bed)?",
        "Enter total sleep duration in hours and minutes, e.g. 7:30 (HH:MM)")
    ]




    for question, placeholder in part1_psqi_questions:
        create_lineText_question(question, layout, placeholder)
    


    # ----------------------PSQI PART 2--------------------
    # Additional instruction
    instruction_text2 = (
        "For each of the remaining questions, check the one best response. Please answer all questions."
    )
    instructionslabel2 = QLabel(instruction_text2, alignment=Qt.AlignmentFlag.AlignTop)
    instructionslabel2.setWordWrap(True)
    instructionslabel2.setStyleSheet("font-size: 14px; font-weight: bold;")
    layout.addWidget(instructionslabel2)

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Fifth question: TROUBLE SLEEPING
    psqiQuestion5B_label = QLabel("5. During the past month, how often have you had trouble sleeping because you ...")
    layout.addWidget(psqiQuestion5B_label)


    # Possible choices for all sub-questions
    answer_choices = [
        "Not during the past month",
        "Less than once a week",
        "Once or twice a week",
        "Three or more times a week"
    ]

    add_sub_question("a) Cannot get to sleep within 30 minutes")
    add_sub_question("b) Wake up in the middle of the night or early morning")
    add_sub_question("c) Have to get up to use the bathroom")
    add_sub_question("d) Cannot breathe comfortably")
    add_sub_question("e) Cough or snore loudly")
    add_sub_question("f) Feel too cold")
    add_sub_question("g) Feel too hot")
    add_sub_question("h) Had bad dreams")
    add_sub_question("i) Have pain")
    create_lineText_question("j) Other reason(s), please describe:", layout, "Describe your reason(s)...")
    add_sub_question("How often during the past month have you had trouble sleeping because of this?")



    # ----------------------PSQI PART 3--------------------

    # Sixth question: SLEEP QUALITY
    psqiQuestion6B_label = QLabel("6. During the past month, how would you rate your sleep quality overall?")
    layout.addWidget(psqiQuestion6B_label)

    # add options for question 6: "Very good", "Fairly good", "Fairly bad", "Very bad"
    psqiQuestion6B_radio_layout = QVBoxLayout()
    psqiQuestion6B_button_group = QButtonGroup()

    for choice in ["Very good", "Fairly good", "Fairly bad", "Very bad"]:
        radio_button = QRadioButton(choice)
        psqiQuestion6B_button_group.addButton(radio_button)
        psqiQuestion6B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion6B_radio_layout)
    input_field_map[psqiQuestion6B_button_group] = psqiQuestion6B_label  # Store mapping in dictionary

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Seventh question: 7. During the past month, how often have you taken medicine to help you sleep (prescribed or "over the counter")? 
    psqiQuestion7B_label = QLabel("7. During the past month, how often have you taken medicine to help you sleep (prescribed or 'over the counter')?")
    layout.addWidget(psqiQuestion7B_label)

    # add options for question 7:"Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"
    psqiQuestion7B_radio_layout = QHBoxLayout()
    psqiQuestion7B_button_group = QButtonGroup()

    for choice in answer_choices:
        radio_button = QRadioButton(choice)
        psqiQuestion7B_button_group.addButton(radio_button)
        psqiQuestion7B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion7B_radio_layout)
    input_field_map[psqiQuestion7B_button_group] = psqiQuestion7B_label  # Store mapping in dictionary

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Eighth question: 8. 8. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?
    psqiQuestion8B_label = QLabel("8. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?")
    layout.addWidget(psqiQuestion8B_label)

    # add options for question 8:"Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"
    psqiQuestion8B_radio_layout = QHBoxLayout()
    psqiQuestion8B_button_group = QButtonGroup()

    for choice in answer_choices:
        radio_button = QRadioButton(choice)
        psqiQuestion8B_button_group.addButton(radio_button)
        psqiQuestion8B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion8B_radio_layout)
    input_field_map[psqiQuestion8B_button_group] = psqiQuestion8B_label  # Store mapping in dictionary

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    # Ninth question: 9. 9. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?
    psqiQuestion9B_label = QLabel("9. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?")
    layout.addWidget(psqiQuestion9B_label)

    # add options for question 9:"No problem at all", "Only a slight problem", "Somewhat of a problem", "A very big problem"
    psqiQuestion9B_radio_layout = QVBoxLayout()
    psqiQuestion9B_button_group = QButtonGroup()

    for choice in ["No problem at all", "Only a slight problem", "Somewhat of a problem", "A very big problem"]:
        radio_button = QRadioButton(choice)
        psqiQuestion9B_button_group.addButton(radio_button)
        psqiQuestion9B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion9B_radio_layout)
    input_field_map[psqiQuestion9B_button_group] = psqiQuestion9B_label  # Store mapping in dictionary

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)



    # ----------------------PSQI PART 4--------------------


    # Tenth question: 10. Do you have a bed partner or room mate?
    psqiQuestion10B_label = QLabel("10. Do you have a bed partner or room mate?")
    layout.addWidget(psqiQuestion10B_label)

    # add options for question 10:"No bed partner or room mate", "Partner/room mate in other room", "Partner in same room, but not same bed", "Partner in same bed"
    psqiQuestion10B_radio_layout = QVBoxLayout()
    psqiQuestion10B_button_group = QButtonGroup()

    for choice in ["No bed partner or room mate", "Partner/room mate in other room", "Partner in same room, but not same bed", "Partner in same bed"]:
        radio_button = QRadioButton(choice)
        psqiQuestion10B_button_group.addButton(radio_button)
        psqiQuestion10B_radio_layout.addWidget(radio_button)

    layout.addLayout(psqiQuestion10B_radio_layout)
    input_field_map[psqiQuestion10B_button_group] = psqiQuestion10B_label  # Store mapping in dictionary

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)

    psqiQuestion11B_label = QLabel("11. If you have a room mate or bed partner, ask him/her how often in the past month you have had ... ...")
    layout.addWidget(psqiQuestion11B_label)


    add_sub_question_11("a) Loud snoring")
    add_sub_question_11("b) Long pauses between breaths while asleep")
    add_sub_question_11("c) Legs twitching or jerking while you sleep")
    add_sub_question_11("d) Episodes of disorientation or confusion during sleep")


    # Special case for 11.e (text input + radio buttons)
    psqiQuestion11eB_label = QLabel("e) Other restlessness while you sleep; ")
    psqiQuestion11eB_input = QLineEdit()
    psqiQuestion11eB_input.setPlaceholderText("please describe ...")
    layout.addWidget(psqiQuestion11eB_label)
    layout.addWidget(psqiQuestion11eB_input)

    input_field_map[psqiQuestion11eB_input] = psqiQuestion11eB_label  # Store mapping in dictionary

    # Add radio button choices for 11.e
    add_sub_question_11("How often during the past month have you faced this?")

    linebreak = QLabel("\n")
    layout.addWidget(linebreak)
    

    # .--------------End of psqi questionnaire-----------------.



    # Label to display form submission message or error message
    submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
    submission_message.setStyleSheet("font-size: 12px; color: red;")
    layout.addWidget(submission_message)

    # Navigation Buttons
    nav_layout = QHBoxLayout()
    # back_button = QPushButton("Back")
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(1))
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
        questionnaire_type = "PSQI_B"
        save_to_csv(participant_id, questionnaire_type, form_data)

        # Display success message
        submission_message.setText("Your responses have been submitted successfully! Click Next to proceed.")
        next_button.setEnabled(True)  # Enable the "Next" button


    
    submit_button.clicked.connect(handle_submit)
    nav_layout.addWidget(submit_button)

    next_button = QPushButton("Next")
    next_button.setEnabled(False)  # Initially disabled
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

# def create_psqi_afterPVT_screen(stack):
#     # empty function
#     pass

# def create_psqi_afterPVT_screen(stack):
#     """Creates the PSQI Questionnaire Screen, screen #7"""
#     screen = QWidget()
#     layout = QVBoxLayout()

#     input_field_map = {}
#     participant_id = state_manager.get_participant_id()

#     def create_lineText_question(label, layout, placeholder_text):
#         """Helper function to create a line question with a label and input field"""
#         label = QLabel(label)
#         input_field = QLineEdit()
#         input_field.setPlaceholderText(placeholder_text)
#         input_field.setMaximumWidth(600)
#         layout.addWidget(label)
#         layout.addWidget(input_field)

#         input_field_map[input_field] = label

#         linebreak = QLabel("\n")
#         layout.addWidget(linebreak)


#     def add_sub_question(label_text):
#         """Helper function to add radio button questions"""
#         question_layout = QVBoxLayout()
#         label = QLabel(label_text)
#         question_layout.addWidget(label)

#         radio_layout = QHBoxLayout()
#         button_group = QButtonGroup()

#         for choice in answer_choices:
#             radio_button = QRadioButton(choice)
#             button_group.addButton(radio_button)
#             radio_layout.addWidget(radio_button)

#         question_layout.addLayout(radio_layout)
#         input_field_map[button_group] = label  # Store mapping in dictionary
#         layout.addLayout(question_layout)  # Add to passed layout

#         linebreak = QLabel("\n")
#         layout.addWidget(linebreak)

#         layout.update()

    
#         # Possible choices for all sub-questions
#     answer_choices_notApplicable = [
#         "Not applicable",
#         "Not during the past month",
#         "Less than once a week",
#         "Once or twice a week",
#         "Three or more times a week",
        
#     ]

#     def add_sub_question_11(label_text):
#         """Helper function to add radio button questions"""
#         question_layout = QVBoxLayout()
#         label = QLabel(label_text)
#         question_layout.addWidget(label)

#         radio_layout = QHBoxLayout()
#         button_group = QButtonGroup()

#         for choice in answer_choices_notApplicable:
#             radio_button = QRadioButton(choice)
#             button_group.addButton(radio_button)
#             radio_layout.addWidget(radio_button)

#         question_layout.addLayout(radio_layout)
#         input_field_map[button_group] = label  # Store mapping in dictionary
#         layout.addLayout(question_layout)  # Add to passed layout

#         linebreak = QLabel("\n")
#         layout.addWidget(linebreak)

#         layout.update()

#     # ----------------------PSQI PART 1--------------------
#     # Instruction Text with combining underlines (\u0332) and line breaks (\n) and "Instruction" in bold
#     instruction_text = (
#         "INSTRUCTIONS:\n\n"
#         "The following questions relate to your usual sleep habits during the past month "
#         + "\u0332".join("only") + ".\n"
#         "Your answers should indicate the most accurate reply for the "
#         + "\u0332".join("majority") + " of days and nights in the past month.\n"
#         "Please answer all questions."
#     )
#     instructionslabel = QLabel(instruction_text, alignment=Qt.AlignmentFlag.AlignTop)
#     instructionslabel.setWordWrap(True)
#     instructionslabel.setStyleSheet("font-size: 14px;")
#     layout.addWidget(instructionslabel)

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

    
#     part1_psqi_questions = [("1. During the past month, what time have you usually gone to bed at night?", "BED TIME__"),
#                             ("2. During the past month, how long (in minutes) has it usually taken you to fall asleep each night?", "NUMBER OF MINUTES___"),
#                             ("3. During the past month, what time have you usually gotten up in the morning?", "GETTING UP TIME__"),
#                             ("4. During the past month, how many hours of actual sleep did you get at night?", "HOURS OF SLEEP PER NIGHT__")]


#     for question, placeholder in part1_psqi_questions:
#         create_lineText_question(question, layout, placeholder)
    


#     # ----------------------PSQI PART 2--------------------
#     # Additional instruction
#     instruction_text2 = (
#         "For each of the remaining questions, check the one best response. Please answer all questions."
#     )
#     instructionslabel2 = QLabel(instruction_text2, alignment=Qt.AlignmentFlag.AlignTop)
#     instructionslabel2.setWordWrap(True)
#     instructionslabel2.setStyleSheet("font-size: 14px; font-weight: bold;")
#     layout.addWidget(instructionslabel2)

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

#     # Fifth question: TROUBLE SLEEPING
#     psqiQuestion5B_label = QLabel("5. During the past month, how often have you had trouble sleeping because you ...")
#     layout.addWidget(psqiQuestion5B_label)


#     # Possible choices for all sub-questions
#     answer_choices = [
#         "Not during the past month",
#         "Less than once a week",
#         "Once or twice a week",
#         "Three or more times a week"
#     ]

#     add_sub_question("a) Cannot get to sleep within 30 minutes")
#     add_sub_question("b) Wake up in the middle of the night or early morning")
#     add_sub_question("c) Have to get up to use the bathroom")
#     add_sub_question("d) Cannot breathe comfortably")
#     add_sub_question("e) Cough or snore loudly")
#     add_sub_question("f) Feel too cold")
#     add_sub_question("g) Feel too hot")
#     add_sub_question("h) Had bad dreams")
#     add_sub_question("i) Have pain")
#     create_lineText_question("j) Other reason(s), please describe:", layout, "Describe your reason(s)...")
#     add_sub_question("How often during the past month have you had trouble sleeping because of this?")



#     # ----------------------PSQI PART 3--------------------

#     # Sixth question: SLEEP QUALITY
#     psqiQuestion6B_label = QLabel("6. During the past month, how would you rate your sleep quality overall?")
#     layout.addWidget(psqiQuestion6B_label)

#     # add options for question 6: "Very good", "Fairly good", "Fairly bad", "Very bad"
#     psqiQuestion6B_radio_layout = QVBoxLayout()
#     psqiQuestion6B_button_group = QButtonGroup()

#     for choice in ["Very good", "Fairly good", "Fairly bad", "Very bad"]:
#         radio_button = QRadioButton(choice)
#         psqiQuestion6B_button_group.addButton(radio_button)
#         psqiQuestion6B_radio_layout.addWidget(radio_button)

#     layout.addLayout(psqiQuestion6B_radio_layout)
#     input_field_map[psqiQuestion6B_button_group] = psqiQuestion6B_label  # Store mapping in dictionary

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

#     # Seventh question: 7. During the past month, how often have you taken medicine to help you sleep (prescribed or "over the counter")? 
#     psqiQuestion7B_label = QLabel("7. During the past month, how often have you taken medicine to help you sleep (prescribed or 'over the counter')?")
#     layout.addWidget(psqiQuestion7B_label)

#     # add options for question 7:"Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"
#     psqiQuestion7B_radio_layout = QHBoxLayout()
#     psqiQuestion7B_button_group = QButtonGroup()

#     for choice in answer_choices:
#         radio_button = QRadioButton(choice)
#         psqiQuestion7B_button_group.addButton(radio_button)
#         psqiQuestion7B_radio_layout.addWidget(radio_button)

#     layout.addLayout(psqiQuestion7B_radio_layout)
#     input_field_map[psqiQuestion7B_button_group] = psqiQuestion7B_label  # Store mapping in dictionary

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

#     # Eighth question: 8. 8. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?
#     psqiQuestion8B_label = QLabel("8. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?")
#     layout.addWidget(psqiQuestion8B_label)

#     # add options for question 8:"Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"
#     psqiQuestion8B_radio_layout = QHBoxLayout()
#     psqiQuestion8B_button_group = QButtonGroup()

#     for choice in answer_choices:
#         radio_button = QRadioButton(choice)
#         psqiQuestion8B_button_group.addButton(radio_button)
#         psqiQuestion8B_radio_layout.addWidget(radio_button)

#     layout.addLayout(psqiQuestion8B_radio_layout)
#     input_field_map[psqiQuestion8B_button_group] = psqiQuestion8B_label  # Store mapping in dictionary

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

#     # Ninth question: 9. 9. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?
#     psqiQuestion9B_label = QLabel("9. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?")
#     layout.addWidget(psqiQuestion9B_label)

#     # add options for question 9:"No problem at all", "Only a slight problem", "Somewhat of a problem", "A very big problem"
#     psqiQuestion9B_radio_layout = QVBoxLayout()
#     psqiQuestion9B_button_group = QButtonGroup()

#     for choice in ["No problem at all", "Only a slight problem", "Somewhat of a problem", "A very big problem"]:
#         radio_button = QRadioButton(choice)
#         psqiQuestion9B_button_group.addButton(radio_button)
#         psqiQuestion9B_radio_layout.addWidget(radio_button)

#     layout.addLayout(psqiQuestion9B_radio_layout)
#     input_field_map[psqiQuestion9B_button_group] = psqiQuestion9B_label  # Store mapping in dictionary

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)



#     # ----------------------PSQI PART 4--------------------


#     # Tenth question: 10. Do you have a bed partner or room mate?
#     psqiQuestion10B_label = QLabel("10. Do you have a bed partner or room mate?")
#     layout.addWidget(psqiQuestion10B_label)

#     # add options for question 10:"No bed partner or room mate", "Partner/room mate in other room", "Partner in same room, but not same bed", "Partner in same bed"
#     psqiQuestion10B_radio_layout = QVBoxLayout()
#     psqiQuestion10B_button_group = QButtonGroup()

#     for choice in ["No bed partner or room mate", "Partner/room mate in other room", "Partner in same room, but not same bed", "Partner in same bed"]:
#         radio_button = QRadioButton(choice)
#         psqiQuestion10B_button_group.addButton(radio_button)
#         psqiQuestion10B_radio_layout.addWidget(radio_button)

#     layout.addLayout(psqiQuestion10B_radio_layout)
#     input_field_map[psqiQuestion10B_button_group] = psqiQuestion10B_label  # Store mapping in dictionary

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)

#     psqiQuestion11B_label = QLabel("11. If you have a room mate or bed partner, ask him/her how often in the past month you have had ... ...")
#     layout.addWidget(psqiQuestion11B_label)


#     add_sub_question_11("a) Loud snoring")
#     add_sub_question_11("b) Long pauses between breaths while asleep")
#     add_sub_question_11("c) Legs twitching or jerking while you sleep")
#     add_sub_question_11("d) Episodes of disorientation or confusion during sleep")


#     # Special case for 11.e (text input + radio buttons)
#     psqiQuestion11eB_label = QLabel("e) Other restlessness while you sleep; ")
#     psqiQuestion11eB_input = QLineEdit()
#     psqiQuestion11eB_input.setPlaceholderText("please describe ...")
#     layout.addWidget(psqiQuestion11eB_label)
#     layout.addWidget(psqiQuestion11eB_input)

#     input_field_map[psqiQuestion11eB_input] = psqiQuestion11eB_label  # Store mapping in dictionary

#     # Add radio button choices for 11.e
#     add_sub_question_11("How often during the past month have you faced this?")

#     linebreak = QLabel("\n")
#     layout.addWidget(linebreak)
    

#     # .--------------End of psqi questionnaire-----------------.



#     # Label to display form submission message or error message
#     submission_message = QLabel("", alignment=Qt.AlignmentFlag.AlignTop)
#     submission_message.setStyleSheet("font-size: 12px; color: red;")
#     layout.addWidget(submission_message)

#     # Navigation Buttons
#     nav_layout = QHBoxLayout()
#     # back_button = QPushButton("Back")
#     # back_button.clicked.connect(lambda: stack.setCurrentIndex(6))
#     # nav_layout.addWidget(back_button)

#     submit_button = QPushButton("Submit")

#     def handle_submit():
#         # Collect the data from the form (this is an example structure)
#         participant_id = state_manager.get_participant_id()
#         form_data = {}
#         # logging.debug(f"Current participant_id: {participant_id}")
    
        
#         # Call the submit_form_check function as per your original logic
#         submit_form_check(input_field_map, submission_message)
        
#         # Check if there are any errors from submit_form_check
#         if "Please fill all required questions (*)" in submission_message.text():
#             return  # Do not proceed with saving if validation failed

#         # Collect the data for text inputs
#         for input_field, label in input_field_map.items():
#             if isinstance(input_field, QLineEdit):  # Only for QLineEdit fields
#                 form_data[label.text()] = input_field.text()  # Save text entered

#         # Collect the data for radio button selections
#         for button_group, label in input_field_map.items():
#             if isinstance(button_group, QButtonGroup):  # If it's a button group
#                 selected_button = button_group.checkedButton()
#                 if selected_button:  # Check if a button was selected
#                     form_data[label.text()] = selected_button.text()


#         # If participant_id is not set, show an error
#         if not participant_id:
#             submission_message.setText("Error: ID is required!")
#             return

#         # Save the form data to CSV
#         questionnaire_type = "PSQI_A"
#         save_to_csv(participant_id, questionnaire_type, form_data)

#         # Display success message
#         submission_message.setText("Your responses have been submitted successfully! Click Next to proceed.")
#         next_button.setEnabled(True)  # Enable the "Next" button


#     submit_button.clicked.connect(handle_submit)
#     nav_layout.addWidget(submit_button)

#     next_button = QPushButton("Next")
#     next_button.setEnabled(False)  # Initially disabled
#     next_button.clicked.connect(lambda: stack.setCurrentIndex(8))
#     nav_layout.addWidget(next_button)

#     layout.addLayout(nav_layout)

#     # Scrollable screen
#     scroll_area = QScrollArea()
#     scroll_widget = QWidget()
#     scroll_widget.setLayout(layout)
#     scroll_area.setWidget(scroll_widget)
#     scroll_area.setWidgetResizable(True)

#     screen_layout = QVBoxLayout()
#     screen_layout.addWidget(scroll_area)
#     screen.setLayout(screen_layout)

#     return screen

