"""Tack – Desktop todo app with floating clock.

Usage:
    python main.py
"""

import os
import sys
from PyQt6.QtWidgets import QApplication

# QtWebEngine needs sandbox disabled when running from PyInstaller temp dir
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

from app.clock_widget import ClockWidget
from app.main_window import MainWindow
from app.tray import TrayIcon


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("Tack")

    # ── floating clock ───────────────────────────────────────────
    clock = ClockWidget()
    clock.show()

    # ── main window (todos) ──────────────────────────────────────
    main_win = MainWindow(clock_widget=clock)

    # ── system tray ──────────────────────────────────────────────
    tray = TrayIcon()
    tray.set_show_callback(main_win.show_window)
    tray.set_quit_callback(lambda: (main_win.close(), clock.close(), app.quit()))
    tray.show()

    # ── run ──────────────────────────────────────────────────────
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
