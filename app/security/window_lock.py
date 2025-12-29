from PyQt6.QtCore import Qt, QTimer


def apply_window_lock(window):
    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    window.setWindowFlag(Qt.WindowType.Tool)
    window.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # Fokusni doimiy tekshiruvchi timer
    focus_timer = QTimer(window)
    focus_timer.timeout.connect(lambda: _ensure_focus(window))
    focus_timer.start(500)  # har 0.5 soniyada


def _ensure_focus(window):
    if not window.isActiveWindow():
        window.raise_()
        window.activateWindow()
