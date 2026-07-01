"""Shared icon assets for Tack – both window/taskbar and system tray."""

from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPen, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRectF, QPointF


# Tack brand colour (matches --accent in ui/app.html)
BRAND_BLUE = QColor("#4F8CFF")
WHITE = QColor("#FFFFFF")


def _draw_tack_icon(painter: QPainter, size: int) -> None:
    """Paint a Tack-brand icon on *painter* for a *size*×*size* pixmap.

    The icon is a rounded rectangle in the brand blue with a white bold "T"
    centred inside it.
    """
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # ── background ────────────────────────────────────────────────
    margin = max(1, size * 0.06)
    r = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)
    painter.setBrush(QBrush(BRAND_BLUE))
    painter.setPen(Qt.PenStyle.NoPen)
    corner = max(1, size * 0.22)
    painter.drawRoundedRect(r, corner, corner)

    # ── white "T" via font ────────────────────────────────────────
    font_size = int(size * 0.65)
    font = QFont("Segoe UI", font_size)
    font.setBold(True)
    # Prefer Segoe UI (Windows); fall back to any sans-serif
    font.setStyleHint(QFont.StyleHint.SansSerif)
    painter.setFont(font)

    fm = QFontMetrics(font)
    text_rect = fm.boundingRect("T")

    # Vertically centre the text – boundingRect gives a y = ascent above baseline,
    # so we shift by -(y) to align the top of the glyph, then add half the height
    # of the text to centre it inside the capsule.
    x = (size - text_rect.width()) / 2.0
    y = (size - text_rect.height()) / 2.0 - text_rect.y()

    painter.setPen(QPen(WHITE, max(1, size // 32)))
    painter.drawText(QPointF(x, y), "T")


def make_tack_pixmap(size: int = 64) -> QPixmap:
    """Return a *size*×*size* ``QPixmap`` with the Tack icon."""
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    _draw_tack_icon(p, size)
    p.end()
    return pm


def make_tack_icon(base_size: int = 64) -> "QIcon":
    """Return a ``QIcon`` built from a *base_size* pixmap.

    ``QIcon`` auto-scales internally, so one high-quality source is sufficient
    for both the taskbar (32–48 px) and the system tray (16–24 px).
    """
    from PyQt6.QtGui import QIcon
    return QIcon(make_tack_pixmap(base_size))
