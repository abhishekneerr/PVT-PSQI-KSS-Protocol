from PyQt6.QtWidgets import QLineEdit, QButtonGroup
from utils.translation_handler import tr

def submit_form_check(input_field_map, submission_message):
    """Handles form submission and marks missing answers with a star (*)"""
    all_filled = True

    for field, label in input_field_map.items():
        # Skip validation for 5.j (the last entry in the map) startwith("j)" or e) Other restlessness while you sleep
        # Skip validation for optional fields (5.j and 11.e)
        if isinstance(field, QLineEdit) and (
            label.text().startswith("j)") or 
            label.text().startswith("e) Other restlessness while you sleep") or 
            label.text().startswith("e) Autre agitation pendant votre sommeil")
        ):
            continue

        if isinstance(field, QButtonGroup) and (
            "How often during the past month" in label.text() or
            "Indiquez la fréquence des troubles du sommeil pour ces raisons" in label.text() or
            "À quelle fréquence au cours du dernier mois avez-vous fait face à cela" in label.text()
        ):
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

# If everything is filled, show success message;
    # else show the translated error
    if all_filled:
        submission_message.setText(tr("form_success_submit"))
        submission_message.setStyleSheet("color: green;")
    else:
        submission_message.setText(tr("form_error_required_questions"))
        submission_message.setStyleSheet("color: red;")