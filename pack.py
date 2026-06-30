"""PyInstaller build script for Tack – single-file exe.

Usage:
    python pack.py
"""
import PyInstaller.__main__
from pathlib import Path

ROOT = Path(__file__).parent

PyInstaller.__main__.run([
    str(ROOT / "Tack.spec"),
    "--clean",
    "--noconfirm",
    "--distpath", str(ROOT / "dist"),
    "--workpath", str(ROOT / "build"),
])
