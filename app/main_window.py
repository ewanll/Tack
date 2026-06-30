"""Main window with QWebEngineView for the todo UI."""

import json
from datetime import date, timedelta
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl, QEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from .bridge import Bridge
from . import storage


class MainWindow(QWidget):
    def __init__(self, clock_widget=None):
        super().__init__()
        self._clock = clock_widget
        self._bridge = Bridge()

        self._setup_window()
        self._setup_webview()
        self._setup_bridge()
        self._connect_bridge_signals()

        if self._clock:
            self._clock.doubleClicked.connect(self.show_window)

    def _setup_window(self):
        self.setWindowTitle("Tack")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(640, 720)
        self.setMinimumSize(420, 520)
        screen = self.screen()
        if screen:
            g = screen.geometry()
            self.move((g.width() - 640) // 2, (g.height() - 720) // 2)

    def _setup_webview(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._webview = QWebEngineView(self)
        self._webview.page().setBackgroundColor(Qt.GlobalColor.transparent)

        # Allow clipboard read/write
        from PyQt6.QtWebEngineCore import QWebEngineSettings
        settings = self._webview.page().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

        self._layout.addWidget(self._webview)
        html_path = Path(__file__).parent.parent / "ui" / "app.html"
        if html_path.exists():
            self._webview.load(QUrl.fromLocalFile(str(html_path.resolve())))

    def _setup_bridge(self):
        self._channel = QWebChannel(self._webview)
        self._channel.registerObject("bridge", self._bridge)
        self._webview.page().setWebChannel(self._channel)
        self._webview.page().loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok: bool):
        if not ok:
            return

        # Seed data from Python if empty
        todos = storage.load_todos()
        if not todos:
            todos = self._create_sample_data()
            storage.save_todos(todos)

        # Push data to JS via bridge-init function
        todos_str = json.dumps(todos, ensure_ascii=False)
        settings = storage.load_settings()
        settings_str = json.dumps(settings, ensure_ascii=False)

        js = f"window.__tackInit({todos_str}, {settings_str});"
        self._webview.page().runJavaScript(js)

        # Apply clock settings
        if self._clock:
            color = settings.get("tack_widget_color", "#ffffff")
            fsize = float(settings.get("tack_font_size", "3"))
            opacity = float(settings.get("tack_opacity", "1"))
            self._clock.set_text_color(color)
            self._clock.set_font_size_pt(int(fsize * 16))
            self._clock.set_widget_opacity(opacity)
            font_family = settings.get("tack_font_family", "Mono")
            self._clock.set_font_family(font_family)
            today = date.today().isoformat()
            count = sum(1 for t in todos if t.get("date") == today and not t.get("done"))
            self._clock.set_todo_count(count)
            # Restore saved clock position
            pos = settings.get("widget_pos")
            if pos:
                self._clock.move(pos["x"], pos["y"])

    def _create_sample_data(self) -> list[dict]:
        today = date.today()
        samples = [
            ("整理 Tack 工具的功能需求", False, 4),
            ("研究 Google Drive API 接入方案", True, 2),
            ("设计浮动时钟小部件的UI", False, 1),
            ("实现待办事项的增删改查", False, 0),
            ("完成技术选型文档", False, 3),
            ("购买生日礼物 🎂", True, 0),
        ]
        result = []
        for i, (text, done, offset) in enumerate(samples):
            d = today - timedelta(days=offset)
            result.append({
                "id": i + 1,
                "text": text,
                "done": done,
                "date": d.isoformat(),
                "createdAt": d.isoformat() + "T08:00:00.000Z",
                "sortOrder": i,
            })
        return result

    def _connect_bridge_signals(self):
        self._bridge.closeRequested.connect(self.hideWindow)
        self._bridge.windowDragRequested.connect(self._on_drag)
        if self._clock:
            self._clock.positionChanged.connect(self._save_clock_position)
            self._bridge.widgetColorChanged.connect(self._clock.set_text_color)
            self._bridge.widgetFontSizeChanged.connect(
                lambda v: self._clock.set_font_size_pt(int(v * 16))
            )
            self._bridge.widgetOpacityChanged.connect(self._clock.set_widget_opacity)
            self._bridge.clockLangChanged.connect(self._clock.set_lang)
            self._bridge.fontFamilyChanged.connect(self._clock.set_font_family)
            self._bridge.widgetTodoCountChanged.connect(self._clock.set_todo_count)

    def _on_drag(self, dx: int, dy: int):
        self.move(self.x() + dx, self.y() + dy)

    def _save_clock_position(self, x: int, y: int):
        """Persist clock widget position to disk."""
        s = storage.load_settings()
        s["widget_pos"] = {"x": x, "y": y}
        storage.save_settings(s)

    def show_window(self):
        if self.isVisible():
            self.raise_()
            self.activateWindow()
        else:
            self.show()
        self._webview.setFocus()

    def hideWindow(self):
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.hideWindow()

    @property
    def bridge(self) -> Bridge:
        return self._bridge
