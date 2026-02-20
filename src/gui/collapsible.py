"""
Collapsible group box for AC Car Editor.

A QGroupBox that can be toggled open/closed with a click on the header.
Used for secondary/less-important parameter sections (e.g. Engine Damage).
"""

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot
from gui.theme import COLORS


class CollapsibleGroupBox(QGroupBox):
    """A QGroupBox that can be collapsed/expanded by clicking its title."""

    def __init__(self, title: str = "", collapsed: bool = True, parent=None):
        super().__init__(parent)
        self._title_text = title
        self._collapsed = collapsed

        self.setCheckable(True)
        self.setChecked(not collapsed)
        self._update_title()
        self.toggled.connect(self._on_toggled)

        # Internal container for the actual content
        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)

        outer = QVBoxLayout()
        outer.setContentsMargins(12, 8, 12, 8)
        outer.addWidget(self._content)
        super().setLayout(outer)

        self._content.setVisible(not collapsed)

    # Public API ----------------------------------------------------------

    def content_layout(self):
        """Return the QVBoxLayout where child widgets should be added."""
        return self._content_layout

    def setLayout(self, layout):
        """Override to redirect layout to the content area."""
        # Properly delete the old layout before setting the new one
        old = self._content.layout()
        if old is not None:
            while old.count():
                old.takeAt(0)
            from PyQt5.QtWidgets import QWidget as _QW
            _QW().setLayout(old)  # orphan it so Qt can reclaim memory
        self._content.setLayout(layout)
        self._content_layout = layout

    def is_collapsed(self):
        return self._collapsed

    def set_collapsed(self, collapsed: bool):
        self.setChecked(not collapsed)

    # Internals -----------------------------------------------------------

    @pyqtSlot(bool)
    def _on_toggled(self, checked):
        self._collapsed = not checked
        self._content.setVisible(checked)
        self._update_title()

    def _update_title(self):
        arrow = "▶" if self._collapsed else "▼"
        self.setTitle(f"{arrow}  {self._title_text}")
