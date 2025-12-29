import sys

from PyQt6.QtWidgets import QApplication

from app.core.session_manager import SessionManager
from app.persistence.db import Database
from app.persistence.repository import SessionRepository
from app.security.autostart import enable_autostart
from app.ui.main_window import MainWindow


def main():
    # 1️⃣ DB init
    Database.init()

    # 2️⃣ Autostart faqat bir marta
    enable_autostart("EduLock")

    # 3️⃣ Session tekshiruvi
    session_manager = SessionManager(SessionRepository())
    # if not session_manager.can_continue():
    #     return

    # 4️⃣ UI
    app = QApplication(sys.argv)
    window = MainWindow(session_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
