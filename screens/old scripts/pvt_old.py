from PyQt6.QtWidgets import (
    QWidget, QLabel, 
    QVBoxLayout, QPushButton, QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer
import random
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from utils.data_handler import save_to_csv
from src.state import state_manager


import time
import random
from PyQt6.QtCore import QTimer, Qt


def start_pvt_logic(label, test_duration_minutes=1, isi_min=1, isi_max=5, update_interval=10):
    """
    Sets up the PVT logic using the provided label widget.
    Logs both true and false key press events.
    
    True key press events (when stimulus is shown) are logged with reaction times.
    False key press events (when stimulus is not shown) are logged without reaction times.
    
    Parameters:
      label: A QLabel (or widget with setText) where the timer will be displayed.
      test_duration_minutes: Duration of the test in minutes.
      isi_min: Minimum inter-stimulus interval in seconds.
      isi_max: Maximum inter-stimulus interval in seconds.
      update_interval: Timer update interval in milliseconds.
      
    Returns:
      A dictionary with:
         "pvt_key_press": function to be called on key press events.
         "pvt_mouse_press": function to be called on mouse press events.
         "timer": the QTimer instance driving the logic.
         "logs": a list holding log entries.
    """
    # Hard-coded participant_id and logs list.
    #participant_id = "XT1010"
    participant_id = state_manager.get_participant_id()
    # log the participant ID in console using the logging module
    logging.info(f"Participant ID: {participant_id}")
    print(f"Participant ID: {participant_id}")
    logs = []
    
    # Internal state for the PVT logic stored in a closure.
    state = {
        "started": False,
        "test_start_time": None,
        "test_duration_ms": test_duration_minutes * 60 * 1000,
        "trial_state": "waiting",   # "waiting" until stimulus appears, then "active"
        "waiting_start_time": None,
        "isi_delay": None,
        "stimulus_start_time": None,
    }
    
    def initialize_state():
        current_time = time.time()
        state["test_start_time"] = current_time
        state["trial_state"] = "waiting"
        state["waiting_start_time"] = current_time
        state["isi_delay"] = random.randint(int(isi_min * 1000), int(isi_max * 1000))
        state["stimulus_start_time"] = None
        print(f"Test started. Waiting period set with random ISI of {state['isi_delay']} ms.")
    
    def update_display():
        # If the test hasn't started, show the starting message.
        if not state["started"]:
            label.setText("Click on the screen to start the test")
            return

        current_time = time.time()
        elapsed_test_ms = (current_time - state["test_start_time"]) * 1000

        # End test if duration has passed.
        if elapsed_test_ms >= state["test_duration_ms"]:
            print("Test finished.")
            timer.stop()
            return

        if state["trial_state"] == "waiting":
            elapsed_waiting_ms = (current_time - state["waiting_start_time"]) * 1000
            if elapsed_waiting_ms >= state["isi_delay"]:
                state["trial_state"] = "active"
                state["stimulus_start_time"] = current_time
                print(f"Stimulus presented. ISI delay was: {state['isi_delay']} ms. Timer started.")
            label.setText("0000")
        elif state["trial_state"] == "active":
            elapsed_stimulus_ms = int((current_time - state["stimulus_start_time"]) * 1000)
            label.setText(f"{elapsed_stimulus_ms:04d}")

    def pvt_key_press(event):
        """
        Call this function from your keyPressEvent handler.
        It expects a QKeyEvent.
        Logs true key presses (with reaction time) and false key presses.
        """

        participant_id = state_manager.get_participant_id()

        if event.key() == Qt.Key.Key_Space:
            current_time = time.time()
            if not state["started"]:
                # Test hasn't started yet so ignore space bar presses.
                return

            if state["trial_state"] == "active":
                reaction_time = int((current_time - state["stimulus_start_time"]) * 1000)
                log_entry = {
                    "participant_id": participant_id,
                    "event": "true_press",
                    "reaction_time_ms": reaction_time,
                    "isi_delay": state["isi_delay"],
                    "timestamp": current_time,
                }
                logs.append(log_entry)
                # Save the latest entry immediately.
                save_to_csv(participant_id, "PVT", log_entry)
                print(f"True press: Reaction time = {reaction_time} ms. Log: {log_entry}")
                # Restart the trial.
                state["trial_state"] = "waiting"
                state["waiting_start_time"] = current_time
                state["isi_delay"] = random.randint(int(isi_min * 1000), int(isi_max * 1000))
                state["stimulus_start_time"] = None
            elif state["trial_state"] == "waiting":
                log_entry = {
                    "participant_id": participant_id,
                    "event": "false_press",
                    "isi_delay": state["isi_delay"],
                    "timestamp": current_time,
                }
                logs.append(log_entry)
                # Save the latest entry immediately.
                save_to_csv(participant_id, "PVT", log_entry)
                print(f"False press: Key pressed during inactive period. Log: {log_entry}")


    def pvt_mouse_press(event):
        """
        Call this function from your mousePressEvent handler.
        It expects a QMouseEvent.
        Starts the test on first click.
        """
        if not state["started"]:
            state["started"] = True
            initialize_state()

    # Set up the timer that drives the display updates.
    timer = QTimer()
    timer.timeout.connect(update_display)
    timer.start(update_interval)  # update interval in ms

    # Return the event handler functions and logs.
    return {
        "pvt_key_press": pvt_key_press,
        "pvt_mouse_press": pvt_mouse_press,
        "timer": timer,
        "logs": logs,
    }
def create_experiment_PVT_screen(stack, trial_duration_minutes=1):
    """Creates the Experiment Trials Screen (PVT), screen #5"""
    screen = QWidget()
    layout = QVBoxLayout()

    participant_id = state_manager.get_participant_id()

    # Message label to prompt user to click
    message_label = QLabel("Click on the screen to start")
    message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    message_label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(message_label)

    # Counter label (hidden initially)
    counter_label = QLabel("0000")
    counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    counter_label.setStyleSheet("font-size: 40px; font-weight: bold;")
    counter_label.setVisible(False)  # Initially hidden
    layout.addWidget(counter_label)

    # Navigation Buttons (Initially hidden)
    nav_layout = QHBoxLayout()
    # back_button = QPushButton("Back")
    # back_button.setVisible(False)  # Hide initially
    # back_button.clicked.connect(lambda: stack.setCurrentIndex(4))  # Go back to KSS
    # nav_layout.addWidget(back_button)

    next_button = QPushButton("Next")
    next_button.setVisible(False)  # Hide initially
    next_button.clicked.connect(lambda: stack.setCurrentIndex(6))  # Move to PSQI/KSS (Post)
    nav_layout.addWidget(next_button)

    layout.addLayout(nav_layout)
    screen.setLayout(layout)

    # Start PVT logic
    pvt_data = start_pvt_logic(counter_label, test_duration_minutes=trial_duration_minutes)

    def finish_test():
        # This is called by the one-shot timer when the test duration has elapsed.
        message_label.setText("Thank you for taking the test, click next to proceed.")
        message_label.setVisible(True)
        next_button.setVisible(True)
        pvt_data["timer"].stop()  # Stop the PVT logic timer
        # back_button.setVisible(True)  # Show the back button
        # hide the counter label
        counter_label.setVisible(False)

    # Function to handle mouse press (start the test when the screen is clicked)
    def on_mouse_press(event):
        if not pvt_data.get("test_started", False):
            pvt_data["test_started"] = True
            # Schedule a one-shot timer that fires exactly after the trial duration (in ms)
            QTimer.singleShot(trial_duration_minutes * 60 * 1000, finish_test)
        pvt_data["pvt_mouse_press"](event)
        message_label.setVisible(False)  # Hide the start message
        counter_label.setVisible(True)  # Show the counter when the test starts

    # Function to handle key press (for spacebar to register a key event)
    def on_key_press(event):
        pvt_data["pvt_key_press"](event)

    # Connect key and mouse events
    screen.mousePressEvent = on_mouse_press
    screen.keyPressEvent = on_key_press

    # Set screen to be focusable and accept key events
    screen.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    screen.setAttribute(Qt.WidgetAttribute.WA_KeyCompression, True)

    return screen