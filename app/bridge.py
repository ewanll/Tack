"""QWebChannel bridge – Python methods callable from JavaScript."""

import json
from datetime import date
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path

from . import storage


class Bridge(QObject):
    """Exposed to JavaScript via QWebChannel."""

    # Signals for the clock widget
    widgetColorChanged = pyqtSignal(str)
    widgetFontSizeChanged = pyqtSignal(float)
    widgetOpacityChanged = pyqtSignal(float)
    widgetTodoCountChanged = pyqtSignal(int)
    clockLangChanged = pyqtSignal(str)
    fontFamilyChanged = pyqtSignal(str)

    # Window control
    closeRequested = pyqtSignal()
    windowDragRequested = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._todos: list[dict] = []

    # ── Todos ──────────────────────────────────────────────────────

    @pyqtSlot(str)
    def saveTodos(self, json_str: str) -> None:
        try:
            data = json.loads(json_str)
            todos = data if isinstance(data, list) else data.get("todos", data)
            storage.save_todos(todos)
            self._todos = todos
            today = date.today().isoformat()
            count = sum(1 for t in todos if t.get("date") == today and not t.get("done"))
            self.widgetTodoCountChanged.emit(count)
        except json.JSONDecodeError:
            pass

    @pyqtSlot(result=str)
    def loadTodos(self) -> str:
        todos = storage.load_todos()
        self._todos = todos
        return json.dumps(todos, ensure_ascii=False)

    # ── Settings ───────────────────────────────────────────────────

    @pyqtSlot(str)
    def saveSettings(self, json_str: str) -> None:
        try:
            storage.save_settings(json.loads(json_str))
        except json.JSONDecodeError:
            pass

    @pyqtSlot(result=str)
    def loadSettings(self) -> str:
        return json.dumps(storage.load_settings(), ensure_ascii=False)

    # ── Data directory ─────────────────────────────────────────────

    @pyqtSlot(result=str)
    def getDataDir(self) -> str:
        return storage.get_data_dir()

    @pyqtSlot(str)
    def setDataDir(self, path: str) -> None:
        storage.set_data_dir(path)
        # migrate existing data to new location
        old_todos = storage.load_todos()
        if old_todos:
            storage.save_todos(old_todos)

    @pyqtSlot(result=str)
    def openFolderPicker(self) -> str:
        """Open native folder dialog, return selected path or empty string."""
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.Directory)
        dlg.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dlg.setWindowTitle("Select data folder for Tack")
        if dlg.exec():
            return dlg.selectedFiles()[0]
        return ""

    # ── Widget position ────────────────────────────────────────────

    @pyqtSlot(int, int)
    def saveWidgetPosition(self, x: int, y: int) -> None:
        s = storage.load_settings()
        s["widget_pos"] = {"x": x, "y": y}
        storage.save_settings(s)

    @pyqtSlot(result=str)
    def loadWidgetPosition(self) -> str:
        s = storage.load_settings()
        return json.dumps(s.get("widget_pos", {}), ensure_ascii=False)

    # ── Clock widget styling ───────────────────────────────────────

    @pyqtSlot(str)
    def setWidgetColor(self, color: str) -> None:
        self.widgetColorChanged.emit(color)

    @pyqtSlot(float)
    def setFontSize(self, size: float) -> None:
        self.widgetFontSizeChanged.emit(size)

    @pyqtSlot(float)
    def setOpacity(self, opacity: float) -> None:
        self.widgetOpacityChanged.emit(opacity)

    @pyqtSlot(int)
    def setTodoCount(self, count: int) -> None:
        self.widgetTodoCountChanged.emit(count)

    @pyqtSlot(str)
    def setClockLang(self, lang: str) -> None:
        self.clockLangChanged.emit(lang)

    @pyqtSlot(str)
    def setFontFamily(self, family: str) -> None:
        self.fontFamilyChanged.emit(family)

    # ── Window control ─────────────────────────────────────────────

    @pyqtSlot()
    def closeWindow(self) -> None:
        self.closeRequested.emit()

    @pyqtSlot(int, int)
    def dragWindow(self, dx: int, dy: int) -> None:
        self.windowDragRequested.emit(dx, dy)

    # ── Startup registry ───────────────────────────────────────────

    @pyqtSlot(bool)
    def setStartupEnabled(self, enabled: bool) -> None:
        import sys
        import winreg
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE
            )
            if enabled:
                script = Path(sys.argv[0]).resolve()
                cmd = f'"{sys.executable}" "{script}"'
                winreg.SetValueEx(key, "Tack", 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, "Tack")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception:
            pass

    @pyqtSlot(result=str)
    def getStartupEnabled(self) -> str:
        """Return '1' if registry entry exists, '0' otherwise."""
        import winreg
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_QUERY_VALUE
            ) as key:
                winreg.QueryValueEx(key, "Tack")
                return "1"
        except FileNotFoundError:
            return "0"
        except Exception:
            return "0"
