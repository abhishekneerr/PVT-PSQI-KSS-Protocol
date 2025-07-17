# utils/translated_widgets.py
from PyQt6.QtWidgets import QLabel, QPushButton, QRadioButton, QLineEdit
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

    def setTranslationKey(self, new_key):
        """Update the translation key and refresh the displayed text."""
        self.translation_key = new_key
        self.update_text()

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


class TranslatedLineEdit(QLineEdit):
    def __init__(self, placeholder_key=None, parent=None):
        super().__init__(parent)
        self.placeholder_key = placeholder_key

        if placeholder_key:
            self.update_placeholder()  # Set initial placeholder
            state_manager.languageChanged.connect(self.update_placeholder)

    @pyqtSlot()
    def update_placeholder(self):
        if self.placeholder_key:
            self.setPlaceholderText(tr(self.placeholder_key))
