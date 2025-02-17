from PyQt6.QtWidgets import QLineEdit, QButtonGroup

def submit_form_check(input_field_map, submission_message):
    """Handles form submission and marks missing answers with a star (*)"""
    all_filled = True

    for field, label in input_field_map.items():
        # Skip validation for 5.j (the last entry in the map) startwith("j)" or e) Other restlessness while you sleep
        if isinstance(field, QLineEdit) and label.text().startswith("j)") or label.text().startswith("e) Other restlessness while you sleep"):
            continue
        if isinstance(field, QButtonGroup) and "How often during the past month" in label.text():  # For 5.j radio button
            continue

        # Validation for Radio Buttons
        if isinstance(field, QButtonGroup):
            if field.checkedButton() is None:
                label.setText(label.text() + " *")
                all_filled = False
            else:
                label.setText(label.text().replace(" *", ""))
        
        # Validation for Text Fields
        elif isinstance(field, QLineEdit):
            if not field.text().strip():
                label.setText(label.text() + " *")
                all_filled = False
            else:
                label.setText(label.text().replace(" *", ""))

    # Display submission message
    submission_message.setText(" Submitted! Click Next to proceed." if all_filled else "Please fill all required questions (*).")
    submission_message.setStyleSheet("color: green;" if all_filled else "color: red;")
