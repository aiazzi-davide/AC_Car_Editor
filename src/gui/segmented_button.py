"""
Segmented button group widget for AC Car Editor.

Replaces QComboBox for small, fixed option sets (e.g. RWD / FWD / AWD / AWD2).
Provides a modern toggle-button strip that is more visually explicit and user-friendly.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from gui.theme import COLORS


class SegmentedButtonGroup(QWidget):
    """A horizontal strip of mutually exclusive toggle buttons."""

    # Emitted when the selected option changes (index, text)
    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)

    _BASE_BTN = (
        f"QPushButton {{"
        f"  background-color: {COLORS['surface']};"
        f"  border: 1px solid {COLORS['border']};"
        f"  padding: 7px 16px;"
        f"  font-weight: 500;"
        f"  color: {COLORS['text_secondary']};"
        f"  min-width: 48px;"
        f"}}"
        f"QPushButton:hover {{"
        f"  background-color: {COLORS['selection']};"
        f"  color: {COLORS['primary']};"
        f"}}"
    )
    _ACTIVE_BTN = (
        f"QPushButton {{"
        f"  background-color: {COLORS['primary']};"
        f"  border: 1px solid {COLORS['primary']};"
        f"  padding: 7px 16px;"
        f"  font-weight: 700;"
        f"  color: {COLORS['text_on_primary']};"
        f"  min-width: 48px;"
        f"}}"
        f"QPushButton:hover {{"
        f"  background-color: {COLORS['primary_hover']};"
        f"}}"
    )

    def __init__(self, options: list, parent=None):
        super().__init__(parent)
        self._options = list(options)
        self._buttons = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for i, text in enumerate(self._options):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(1)  # PointingHand
            self._group.addButton(btn, i)
            self._buttons.append(btn)
            layout.addWidget(btn)

            # Round only the outer corners
            if len(self._options) == 1:
                btn.setStyleSheet(self._BASE_BTN + "QPushButton { border-radius: 6px; }")
            elif i == 0:
                btn.setStyleSheet(self._BASE_BTN +
                                  "QPushButton { border-top-left-radius: 6px; border-bottom-left-radius: 6px;"
                                  " border-top-right-radius: 0; border-bottom-right-radius: 0; }")
            elif i == len(self._options) - 1:
                btn.setStyleSheet(self._BASE_BTN +
                                  "QPushButton { border-top-right-radius: 6px; border-bottom-right-radius: 6px;"
                                  " border-top-left-radius: 0; border-bottom-left-radius: 0;"
                                  " border-left: none; }")
            else:
                btn.setStyleSheet(self._BASE_BTN +
                                  "QPushButton { border-radius: 0; border-left: none; }")

        self._group.buttonClicked.connect(self._on_clicked)

        # Default: select first
        if self._buttons:
            self._buttons[0].setChecked(True)
            self._apply_styles()

    # ── Public API (QComboBox-compatible) ──────────────────────────────

    def currentIndex(self):
        return self._group.checkedId()

    def currentText(self):
        idx = self.currentIndex()
        if 0 <= idx < len(self._options):
            return self._options[idx]
        return ""

    def setCurrentIndex(self, index):
        if 0 <= index < len(self._buttons):
            self._buttons[index].setChecked(True)
            self._apply_styles()

    def findText(self, text):
        for i, opt in enumerate(self._options):
            if opt == text:
                return i
        return -1

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        for btn in self._buttons:
            btn.setEnabled(enabled)

    def count(self):
        return len(self._options)

    def itemText(self, index):
        if 0 <= index < len(self._options):
            return self._options[index]
        return ""

    # ── Internal ──────────────────────────────────────────────────────

    def _on_clicked(self, button):
        idx = self._group.id(button)
        self._apply_styles()
        self.currentIndexChanged.emit(idx)
        self.currentTextChanged.emit(self._options[idx])

    def _apply_styles(self):
        checked_id = self._group.checkedId()
        for i, btn in enumerate(self._buttons):
            base = self._ACTIVE_BTN if i == checked_id else self._BASE_BTN
            # Re-apply corner rounding on top of active/base
            if len(self._options) == 1:
                btn.setStyleSheet(base + "QPushButton { border-radius: 6px; }")
            elif i == 0:
                btn.setStyleSheet(base +
                                  "QPushButton { border-top-left-radius: 6px; border-bottom-left-radius: 6px;"
                                  " border-top-right-radius: 0; border-bottom-right-radius: 0; }")
            elif i == len(self._options) - 1:
                btn.setStyleSheet(base +
                                  "QPushButton { border-top-right-radius: 6px; border-bottom-right-radius: 6px;"
                                  " border-top-left-radius: 0; border-bottom-left-radius: 0;"
                                  " border-left: none; }")
            else:
                btn.setStyleSheet(base + "QPushButton { border-radius: 0; border-left: none; }")
