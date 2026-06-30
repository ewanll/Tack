"""Floating transparent clock window – always-on-top, draggable."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QDateTime, QRect, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QFontMetrics


class ClockWidget(QWidget):
    """Semi-transparent frameless window showing HH:MM:SS + todo count."""

    doubleClicked = pyqtSignal()
    positionChanged = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        # Defaults (overridden by settings) — must be BEFORE _setup_timers
        self._drag_active = False
        self._drag_offset = None
        self._font_size = 48
        self._opacity = 1.0
        self._text_color = QColor(255, 255, 255)
        self._font_family = "'Consolas', 'SF Mono', 'Fira Code', 'Courier New', monospace"
        self._todo_count = 0
        self._lang = 'zh'

        self._setup_window()
        self._setup_ui()
        self._setup_timers()

    # ── window setup ──────────────────────────────────────────────

    def _setup_window(self):
        self.setWindowTitle("Tack")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # start at a reasonable default (centered top 1/8)
        screen = self.screen()
        if screen:
            g = screen.geometry()
            w, h = 260, 90
            x = (g.width() - w) // 2
            y = g.height() // 8 - h // 2
            self.setGeometry(x, y, w, h)
        else:
            self.setGeometry(640, 60, 260, 90)

    def _setup_ui(self):
        self._time_label = QLabel(self)
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._time_label.setStyleSheet("background: transparent;")

        self._todo_label = QLabel(self)
        self._todo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._todo_label.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 4)
        layout.setSpacing(0)
        layout.addWidget(self._time_label)
        layout.addWidget(self._todo_label)

    def _setup_timers(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        self._apply_style()
        self._tick()
        self._update_todo_label()

    def _tick(self):
        now = QDateTime.currentDateTime()
        self._time_label.setText(now.toString("HH:mm:ss"))

    def _update_todo_label(self):
        if self._lang == 'en':
            d = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            fmt = "{} Today {}"
        else:
            d = ['周一','周二','周三','周四','周五','周六','周日']
            fmt = "{} 今日待办 {}"
        day_name = d[QDateTime.currentDateTime().date().dayOfWeek() - 1]
        self._todo_label.setText(fmt.format(day_name, self._todo_count))

    def set_lang(self, lang: str):
        self._lang = lang
        self._update_todo_label()

    def set_todo_count(self, n: int):
        self._todo_count = n
        self._update_todo_label()

    # ── styling ──────────────────────────────────────────────────

    def _apply_style(self):
        r, g, b = self._text_color.red(), self._text_color.green(), self._text_color.blue()
        self._time_label.setStyleSheet(
            f"color: rgb({r},{g},{b}); background: transparent; font-size: {self._font_size}px; "
            f"font-family: {self._font_family};"
        )
        fs = max(16, self._font_size // 2)
        self._todo_label.setStyleSheet(
            f"color: rgba({r},{g},{b},200); background: transparent; font-size: {fs}px; font-weight: 600;"
        )
        self.setWindowOpacity(self._opacity)
        self.setStyleSheet(
            "ClockWidget{border-radius:12px;border:1px solid transparent;background:transparent;}"
            "ClockWidget:hover{border:1px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.05);}"
        )

    def set_text_color(self, hex_color: str):
        self._text_color = QColor(hex_color)
        self._apply_style()

    def set_font_family(self, family: str):
        families = {
            # Backward-compat aliases
            'Mono': "'SF Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace",
            'Sans': "-apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
            'Serif': "Georgia, 'Noto Serif SC', 'Times New Roman', serif",
            # 8 common fonts — rich fallback chains
            'Consolas': "Consolas, 'SF Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace",
            'SF_Mono': "'SF Mono', 'Fira Code', 'Cascadia Code', 'SF Pro Display', Consolas, monospace",
            'Segoe_UI': "'Segoe UI', -apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif",
            'YaHei': "'Microsoft YaHei', '微软雅黑', 'PingFang SC', 'Noto Sans SC', -apple-system, sans-serif",
            'Arial': "Arial, 'Helvetica Neue', Helvetica, -apple-system, sans-serif",
            'Georgia': "Georgia, 'Noto Serif SC', 'Times New Roman', serif",
            'Courier_New': "'Courier New', 'Courier', 'Nimbus Mono', Consolas, monospace",
            'JetBrains_Mono': "'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'SF Mono', Consolas, monospace",
        }
        self._font_family = families.get(family, families['Consolas'])
        self._apply_style()

    def set_font_size_pt(self, size: int):
        self._font_size = size
        self._apply_style()

    def set_widget_opacity(self, opacity: float):
        self._opacity = opacity
        self._apply_style()

    # ── mouse drag ───────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_active and self._drag_offset:
            self.move(self.mapToParent(event.position().toPoint() - self._drag_offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            was_dragging = self._drag_active
            self._drag_active = False
            self._drag_offset = None
            if was_dragging:
                self.positionChanged.emit(self.x(), self.y())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.doubleClicked.emit()
