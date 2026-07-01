#!/usr/bin/env python3
"""Generate ``resources/icon.ico`` and ``resources/icon.png`` for Tack.

Requires PyQt6 (the same runtime the app uses).

Usage:
    python tools/generate_icon.py
"""

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice

# Must create a QApplication before doing anything paint-related
_app = QApplication(sys.argv)

from app.icons import make_tack_pixmap

OUT = ROOT / "resources"
OUT.mkdir(parents=True, exist_ok=True)


def pixmap_to_png_bytes(pm: QPixmap) -> bytes:
    """Convert QPixmap to raw PNG bytes."""
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    pm.save(buf, b"PNG")
    buf.close()
    return bytes(ba)


def build_ico(sizes: tuple[int, ...] = (16, 32, 48, 256)) -> bytes:
    """Build a multi-resolution .ico file with embedded PNG images."""
    images = []
    for s in sizes:
        pm = make_tack_pixmap(s)
        data = pixmap_to_png_bytes(pm)
        images.append((s, data))

    num = len(images)

    # ── ICO header ──────────────────────────────────────────────
    header = struct.pack("<HHH", 0, 1, num)  # reserved, type(ico), count

    # ── Directory entries + images ──────────────────────────────
    offset = 6 + 16 * num  # first image starts right after the directory
    directory = b""
    image_data = b""

    for w, data in images:
        # ICO spec: 0 means 256 for width/height
        ico_w = 0 if w >= 256 else w
        ico_h = 0 if w >= 256 else w
        dir_entry = struct.pack(
            "<BBBBHHII",
            ico_w,        # width
            ico_h,        # height
            0,            # palette colors (0 = none)
            0,            # reserved
            1,            # color planes
            32,           # bits per pixel
            len(data),    # image data size
            offset,       # offset in file
        )
        directory += dir_entry
        image_data += data
        offset += len(data)

    return header + directory + image_data


def main():
    # ── PNG ─────────────────────────────────────────────────────
    pm = make_tack_pixmap(256)
    png_path = OUT / "icon.png"
    pm.save(str(png_path), b"PNG")
    print(f"[OK] Saved {png_path} ({png_path.stat().st_size} bytes)")

    # ── ICO ─────────────────────────────────────────────────────
    ico_bytes = build_ico([16, 32, 48, 256])
    ico_path = OUT / "icon.ico"
    ico_path.write_bytes(ico_bytes)
    print(f"[OK] Saved {ico_path} ({ico_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
