# utils/translated_widgets.py
from PyQt6.QtWidgets import QLabel, QPushButton, QRadioButton
from PyQt6.QtCore import pyqtSlot
from utils.translation_handler import tr
from src.state import state_manager

class TranslatedLabel(QLabel):
    def __init__(self, translation_key, alignment=None, parent=None):
        super().__init__(parent)
        self.translation_key = translation_key
        self.update_text()
        # Listen for language changes
        state_manager.languageChanged.connect(self.update_text)

        if alignment:
            self.setAlignment(alignment)   

    @pyqtSlot()
    def update_text(self):
        self.setText(tr(self.translation_key))

class TranslatedButton(QPushButton):
    def __init__(self, translation_key, parent=None):
        super().__init__(parent)
        self.translation_key = translation_key
        self.update_text()
        state_manager.languageChanged.connect(self.update_text)

    @pyqtSlot()
    def update_text(self):
        self.setText(tr(self.translation_key))

class TranslatedRadioButton(QRadioButton):
    def __init__(self, translation_key, parent=None):
        super().__init__(parent)
        self.translation_key = translation_key
        self.update_text()
        state_manager.languageChanged.connect(self.update_text)

    @pyqtSlot()
    def update_text(self):
        self.setText(tr(self.translation_key))
