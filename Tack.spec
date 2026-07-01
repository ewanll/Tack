# -*- mode: python ; coding: utf-8 -*-
"""Tack.spec – PyInstaller build with size optimizations."""

import os
from pathlib import Path

ROOT = Path.cwd()

# ── Substrings that identify unnecessary files ─────────────────────────
# SAFE exclusions only – Qt6WebEngineCore.dll needs Qt6Qml, Qt6Quick,
# Qt6Positioning at runtime (Chromium integration layer), so we CANNOT
# exclude those.
EXCLUDED_PATTERNS = [
    # DevTools Chrome debugger – not needed in a production app
    "qtwebengine_devtools_resources.debug.pak",   # -72 MB
    "qtwebengine_devtools_resources.pak",          # -11 MB
    # Software OpenGL fallback – only needed if GPU/ANGLE fails
    "opengl32sw.dll",                               # -20 MB
    # Qt Designer – not used at runtime
    "Qt6Designer",
]

def _filter_out_unnecessary(toc):
    """Remove entries matching any EXCLUDED_PATTERN by substring."""
    kept = []
    for e in toc:
        # Check against both destination and source paths
        haystack = str(e[0]) + "|" + (str(e[1]) if len(e) > 1 else "")
        if any(p in haystack for p in EXCLUDED_PATTERNS):
            continue
        kept.append(e)
    return kept


a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[],
    binaries=[],
    datas=[
        (str(ROOT / "ui"), "ui"),
        (str(ROOT / "resources" / "icon.png"), "resources"),
    ],
    hiddenimports=[
        "PyQt6.QtWebEngineWidgets",
        "PyQt6.QtWebChannel",
        "PyQt6.QtWebEngineCore",
        # Intentionally NOT including QtWebEngineQuick – we don't use QML/Quick
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# ── Filter out bloat before building EXE ──────────────────────────────
a.binaries = _filter_out_unnecessary(a.binaries)
a.datas = _filter_out_unnecessary(a.datas)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Tack",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / "resources" / "icon.ico"),
)
