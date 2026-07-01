"""System tray icon for Tack."""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from app.icons import make_tack_icon


class TrayIcon(QSystemTrayIcon):
    """Minimize-to-tray support with context menu."""

    def __init__(self, parent=None):
        self._lang = 'zh'
        icon = make_tack_icon(64)
        super().__init__(icon, parent)
        self.setToolTip("Tack")

        self._menu = QMenu()
        self.setContextMenu(self._menu)
        self._setup_actions()

    def _setup_actions(self):
        self._act_show = QAction(self._tr_show())
        self._act_show.triggered.connect(self._on_show)
        self._menu.addAction(self._act_show)

        self._menu.addSeparator()

        self._act_quit = QAction(self._tr_quit())
        self._act_quit.triggered.connect(self._on_quit)
        self._menu.addAction(self._act_quit)

        # Left-click also shows
        self.activated.connect(self._on_activated)

    def _tr_show(self) -> str:
        return "打开 Tack" if self._lang == 'zh' else "Open Tack"

    def _tr_quit(self) -> str:
        return "退出" if self._lang == 'zh' else "Quit"

    def set_lang(self, lang: str):
        self._lang = lang
        self._act_show.setText(self._tr_show())
        self._act_quit.setText(self._tr_quit())

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._on_show()

    def _on_show(self):
        self._show_callback() if hasattr(self, "_show_callback") else None

    def _on_quit(self):
        self._quit_callback() if hasattr(self, "_quit_callback") else None

    def set_show_callback(self, fn):
        self._show_callback = fn

    def set_quit_callback(self, fn):
        self._quit_callback = fn
