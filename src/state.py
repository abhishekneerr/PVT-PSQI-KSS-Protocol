# src/state.py

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from PyQt6.QtCore import QObject, pyqtSignal

class StateManager(QObject):
    languageChanged = pyqtSignal()  # <-- This signal will be emitted whenever language changes

    def __init__(self):
        super().__init__()
        self.language = "en"
        self.participant_id = None

    def set_language(self, lang_code):
        self.language = lang_code
        # After changing language, emit signal so all translated widgets can refresh
        self.languageChanged.emit()

    def get_language(self):
        return self.language

    def set_participant_id(self, pid):
        self.participant_id = pid

    def get_participant_id(self):
        return self.participant_id


# Create the shared instance
state_manager = StateManager()


