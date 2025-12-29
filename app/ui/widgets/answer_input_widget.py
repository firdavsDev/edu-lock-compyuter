from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit


class AnswerInputWidget(QLineEdit):
    submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setValidator(QIntValidator())  # 👈 faqat integer
        self.returnPressed.connect(self._emit_submit)

    def _emit_submit(self):
        self.submitted.emit(self.text())

    def clear_input(self):
        self.clear()
