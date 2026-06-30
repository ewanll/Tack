"""System tray icon for Tack."""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class TrayIcon(QSystemTrayIcon):
    """Minimize-to-tray support with context menu."""

    def __init__(self, parent=None):
        # Create a simple icon programmatically
        icon = QIcon.fromTheme("appointment-soon")
        if icon.isNull():
            # Fallback: small colored pixmap
            from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush
            pm = QPixmap(16, 16)
            pm.fill(Qt.GlobalColor.transparent)
            p = QPainter(pm)
            p.setBrush(QBrush(QColor("#4F8CFF")))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(0, 0, 16, 16, 4, 4)
            p.end()
            icon = QIcon(pm)

        super().__init__(icon, parent)
        self.setToolTip("Tack")

        self._menu = QMenu()
        self.setContextMenu(self._menu)
        self._setup_actions()

    def _setup_actions(self):
        self._act_show = QAction("打开 Tack")
        self._act_show.triggered.connect(self._on_show)
        self._menu.addAction(self._act_show)

        self._menu.addSeparator()

        self._act_quit = QAction("退出")
        self._act_quit.triggered.connect(self._on_quit)
        self._menu.addAction(self._act_quit)

        # Left-click also shows
        self.activated.connect(self._on_activated)

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
