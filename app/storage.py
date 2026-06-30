"""Local file storage for Todos and Settings."""

import os
import json
from pathlib import Path

APP_DIR = Path(os.environ.get("APPDATA", Path.home() / ".config")) / "Tack"


def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_data_dir() -> str:
    s = load_settings()
    return s.get("data_dir", "")


def _get_todos_path() -> Path:
    data_dir = _get_data_dir()
    if data_dir and Path(data_dir).exists():
        return Path(data_dir) / "tack_todos.json"
    _ensure_dir(APP_DIR)
    return APP_DIR / "tack_todos.json"


def _get_settings_path() -> Path:
    _ensure_dir(APP_DIR)
    return APP_DIR / "settings.json"


# ── Todos ──────────────────────────────────────────────────────

def save_todos(todos: list[dict]) -> None:
    path = _get_todos_path()
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "todos": todos}, f, ensure_ascii=False, indent=2)


def load_todos() -> list[dict]:
    path = _get_todos_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("todos", [])
    except (json.JSONDecodeError, KeyError):
        return []


# ── Settings ───────────────────────────────────────────────────

def save_settings(settings: dict) -> None:
    path = _get_settings_path()
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def load_settings() -> dict:
    path = _get_settings_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


# ── Data directory ─────────────────────────────────────────────

def get_data_dir() -> str:
    return _get_data_dir()


def set_data_dir(path: str) -> None:
    s = load_settings()
    s["data_dir"] = path
    save_settings(s)
