from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from app.config import TIME_LIMIT_SECONDS
from app.core.math_engine import MathEngine
from app.core.session_manager import SessionManager
from app.persistence.models import Answer
from app.persistence.repository import AnswerRepository
from app.security.window_lock import apply_window_lock
from app.ui.widgets.answer_input_widget import AnswerInputWidget
from app.ui.widgets.question_widget import QuestionWidget
from app.ui.widgets.timer_widget import TimerWidget


class MainWindow(QWidget):
    def __init__(self, session_manager: SessionManager):
        super().__init__()

        # --- dependencies ---
        self.session_manager = session_manager
        self.engine = MathEngine()
        self.answer_repo = AnswerRepository()

        # --- state ---
        self.current_question = None
        self.remaining = TIME_LIMIT_SECONDS
        self.processing = False

        # --- ui ---
        self._build_ui()
        apply_window_lock(self)

        # --- timer ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)

        # --- start ---
        self._next_question()

    # ---------------- UI ----------------

    def _build_ui(self):
        self.setFixedSize(520, 320)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #111;
                color: #fff;
            }
        """
        )

        self.question_widget = QuestionWidget(self)
        self.question_widget.setStyleSheet("font-size: 42px;")

        self.timer_widget = TimerWidget(self)
        self.timer_widget.setStyleSheet("font-size: 18px; color: #ff5555;")

        self.answer_input = AnswerInputWidget(self)
        self.answer_input.setStyleSheet(
            """
            font-size: 26px;
            padding: 8px;
            background-color: #222;
            color: #00ff99;
            border: 2px solid #444;
            border-radius: 6px;
        """
        )
        self.answer_input.submitted.connect(self._on_submit)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.addWidget(self.question_widget)
        layout.addWidget(self.timer_widget)
        layout.addWidget(self.answer_input)

        self.setLayout(layout)

    # ---------------- FLOW ----------------

    def _next_question(self):
        if not self.session_manager.can_continue():
            self._shutdown()
            return

        self.current_question = self.engine.generate()
        self.processing = False

        self.question_widget.set_question(self.current_question.text)
        self.answer_input.clear_input()

        self.remaining = TIME_LIMIT_SECONDS
        self.timer_widget.update_time(self.remaining)

        self.timer.start(1000)

    def _on_tick(self):
        if self.processing:
            return

        self.remaining -= 1
        self.timer_widget.update_time(self.remaining)

        if self.remaining <= 0:
            self._handle_answer("")

    def _on_submit(self, text: str):
        self._handle_answer(text)

    def _handle_answer(self, user_answer: str):
        # ⛔ double trigger himoyasi
        if self.processing or self.current_question is None:
            return

        self.processing = True
        self.timer.stop()

        is_correct = self.engine.check(self.current_question, user_answer)

        self.answer_repo.save(
            Answer(
                session_date=self.session_manager.today,
                question=self.current_question.text,
                user_answer=user_answer,
                correct_answer=str(self.current_question.correct_answer),
                is_correct=is_correct,
            )
        )

        self.session_manager.register_answer()

        # keyingi savolni biroz kechiktirib yuklaymiz (event loop xavfsizligi)
        QTimer.singleShot(150, self._next_question)

    # ---------------- EXIT ----------------

    def _shutdown(self):
        self.timer.stop()
        self.current_question = None
        self.close()

    def closeEvent(self, event):
        event.ignore()
