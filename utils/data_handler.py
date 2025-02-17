import csv
import os
import logging

# Example usage in your existing submit logic:
def on_submit(participant_id, questionnaire_type, responses):
    save_to_csv(participant_id, questionnaire_type, responses)
    print(f"Responses saved to {participant_id}_{questionnaire_type}.csv")


def save_to_csv(participant_id, questionnaire_type, data):
    """Saves form data to a CSV file named using participant ID and questionnaire type"""
    root_folder = "participants_data"
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    folder_name = os.path.join(root_folder, f"participant_{participant_id}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = os.path.join(folder_name, f"{participant_id}_{questionnaire_type}.csv")
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        # Write header only if the file doesn't exist
        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

    logging.info(f"Data saved to {filename}")