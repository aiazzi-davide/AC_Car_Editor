"""
Toast / non-modal notification widget for AC Car Editor.

Replaces the annoying QMessageBox.information pop-ups for success messages.
Shows a brief auto-dismissing banner at the top of the parent widget.
"""

from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from gui.theme import COLORS


class ToastNotification(QLabel):
    """A brief, auto-dismissing toast notification."""

    _STYLES = {
        'success': (
            f"background-color: {COLORS['accent_light']}; "
            f"color: {COLORS['accent_hover']}; "
            f"border-left: 4px solid {COLORS['accent']}; "
            f"border-radius: 6px; padding: 12px 18px; font-weight: 600; font-size: 13px;"
        ),
        'info': (
            f"background-color: {COLORS['primary_light']}; "
            f"color: {COLORS['primary_hover']}; "
            f"border-left: 4px solid {COLORS['primary']}; "
            f"border-radius: 6px; padding: 12px 18px; font-weight: 600; font-size: 13px;"
        ),
        'warning': (
            f"background-color: {COLORS['warning_light']}; "
            f"color: {COLORS['warning_text']}; "
            f"border-left: 4px solid {COLORS['warning']}; "
            f"border-radius: 6px; padding: 12px 18px; font-weight: 600; font-size: 13px;"
        ),
    }

    def __init__(self, message: str, kind: str = 'success',
                 duration_ms: int = 3000, parent: QWidget = None):
        super().__init__(message, parent)
        self.setStyleSheet(self._STYLES.get(kind, self._STYLES['success']))
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setWordWrap(True)
        self.setMinimumHeight(36)

        # Position at top of parent
        if parent:
            self.setFixedWidth(min(parent.width() - 40, 600))
            x = (parent.width() - self.width()) // 2
            self.move(x, 12)

        # Fade-in
        self._opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)
        self._fade_in = QPropertyAnimation(self._opacity, b'opacity')
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)
        self._fade_in.setDuration(250)
        self._fade_in.setEasingCurve(QEasingCurve.OutCubic)

        # Fade-out (starts after duration)
        self._fade_out = QPropertyAnimation(self._opacity, b'opacity')
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.setDuration(400)
        self._fade_out.setEasingCurve(QEasingCurve.InCubic)
        self._fade_out.finished.connect(self._on_done)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._start_fade_out)

        self.raise_()
        self.show()
        self._fade_in.start()
        self._timer.start(duration_ms)

    def _start_fade_out(self):
        self._fade_out.start()

    def _on_done(self):
        self.hide()
        self.deleteLater()


def show_toast(parent, message, kind='success', duration_ms=3000):
    """Convenience function to display a toast notification on *parent*."""
    return ToastNotification(message, kind=kind, duration_ms=duration_ms, parent=parent)
