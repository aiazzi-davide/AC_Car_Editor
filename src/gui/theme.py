"""
Centralized theme and styling for AC Car Editor.
Defines colors, fonts, spacing and QSS stylesheets for a modern, consistent UI.
"""

# ── Color palette ──────────────────────────────────────────────────────
COLORS = {
    # Primary
    'primary':        '#3B82F6',   # Blue-500
    'primary_hover':  '#2563EB',   # Blue-600
    'primary_light':  '#DBEAFE',   # Blue-100

    # Accent / success
    'accent':         '#10B981',   # Emerald-500
    'accent_hover':   '#059669',   # Emerald-600
    'accent_light':   '#D1FAE5',   # Emerald-100

    # Warning / caution
    'warning':        '#F59E0B',   # Amber-500
    'warning_light':  '#FEF3C7',   # Amber-100
    'warning_text':   '#92400E',   # Amber-800

    # Error / critical
    'error':          '#EF4444',   # Red-500
    'error_light':    '#FEE2E2',   # Red-100
    'error_text':     '#991B1B',   # Red-800

    # Neutral / surfaces
    'bg':             '#F8FAFC',   # Slate-50
    'surface':        '#FFFFFF',
    'border':         '#E2E8F0',   # Slate-200
    'border_focus':   '#93C5FD',   # Blue-300
    'divider':        '#CBD5E1',   # Slate-300

    # Text
    'text':           '#1E293B',   # Slate-800
    'text_secondary': '#64748B',   # Slate-500
    'text_muted':     '#94A3B8',   # Slate-400
    'text_on_primary':'#FFFFFF',

    # Tab & selection
    'tab_active_bg':  '#FFFFFF',
    'tab_inactive_bg':'#F1F5F9',   # Slate-100
    'selection':      '#DBEAFE',   # Blue-100

    # Misc
    'scrollbar':      '#CBD5E1',
    'scrollbar_hover':'#94A3B8',
    'group_header':   '#F1F5F9',
}

# ── Global application stylesheet ──────────────────────────────────────
APP_STYLESHEET = f"""
/* ── Base ─────────────────────────────────────────────── */
QWidget {{
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: {COLORS['text']};
}}
QMainWindow, QDialog {{
    background-color: {COLORS['bg']};
}}

/* ── Group boxes ─────────────────────────────────────── */
QGroupBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 14px;
    padding: 16px 12px 10px 12px;
    font-weight: 600;
    font-size: 13px;
    color: {COLORS['text']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: 2px;
    padding: 0 6px;
    background-color: {COLORS['surface']};
    color: {COLORS['primary']};
}}

/* ── Tabs ────────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background: {COLORS['surface']};
    top: -1px;
}}
QTabBar::tab {{
    background: {COLORS['tab_inactive_bg']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 5px 15px;
    margin-right: 3px;
    color: {COLORS['text_secondary']};
    font-weight: 500;
    min-width: 85px;
}}
QTabBar::tab:selected {{
    background: {COLORS['tab_active_bg']};
    color: {COLORS['primary']};
    font-weight: 600;
    border-bottom: 2px solid {COLORS['primary']};
}}
QTabBar::tab:hover:!selected {{
    background: {COLORS['selection']};
    color: {COLORS['primary']};
}}

/* ── Buttons ─────────────────────────────────────────── */
QPushButton {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 500;
    color: {COLORS['text']};
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: {COLORS['selection']};
    border-color: {COLORS['primary']};
    color: {COLORS['primary']};
}}
QPushButton:pressed {{
    background-color: {COLORS['primary_light']};
}}
QPushButton:disabled {{
    background-color: {COLORS['tab_inactive_bg']};
    color: {COLORS['text_muted']};
    border-color: {COLORS['border']};
}}

/* ── Spin boxes ──────────────────────────────────────── */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 5px 8px;
    min-height: 22px;
    selection-background-color: {COLORS['selection']};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {COLORS['border_focus']};
    border-width: 2px;
    padding: 4px 7px;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid {COLORS['border']};
    border-top-right-radius: 5px;
    background: {COLORS['tab_inactive_bg']};
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background: {COLORS['selection']};
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    border-left: 1px solid {COLORS['border']};
    border-bottom-right-radius: 5px;
    background: {COLORS['tab_inactive_bg']};
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: {COLORS['selection']};
}}

/* ── Line edits ──────────────────────────────────────── */
QLineEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {COLORS['selection']};
}}
QLineEdit:focus {{
    border-color: {COLORS['border_focus']};
    border-width: 2px;
    padding: 5px 9px;
}}

/* ── Combo boxes ─────────────────────────────────────── */
QComboBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
    min-height: 22px;
}}
QComboBox:focus {{
    border-color: {COLORS['border_focus']};
}}
QComboBox::drop-down {{
    border-left: 1px solid {COLORS['border']};
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    width: 24px;
    background: {COLORS['tab_inactive_bg']};
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    selection-background-color: {COLORS['selection']};
    selection-color: {COLORS['primary']};
    outline: none;
}}

/* ── Check boxes ─────────────────────────────────────── */
QCheckBox {{
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['border']};
    border-radius: 4px;
    background: {COLORS['surface']};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS['primary']};
    border-color: {COLORS['primary']};
}}
QCheckBox::indicator:hover {{
    border-color: {COLORS['primary']};
}}

/* ── Text edits (read-only areas) ────────────────────── */
QTextEdit {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px;
    selection-background-color: {COLORS['selection']};
}}

/* ── List widget ─────────────────────────────────────── */
QListWidget {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    padding: 6px 10px;
    border-radius: 4px;
    margin: 1px 2px;
}}
QListWidget::item:selected {{
    background-color: {COLORS['selection']};
    color: {COLORS['primary']};
}}
QListWidget::item:hover:!selected {{
    background-color: {COLORS['tab_inactive_bg']};
}}

/* ── Scroll areas ────────────────────────────────────── */
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['scrollbar']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['scrollbar_hover']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

/* ── Splitter ────────────────────────────────────────── */
QSplitter::handle {{
    background: {COLORS['border']};
}}
QSplitter::handle:horizontal {{
    width: 2px;
}}

/* ── Status bar ──────────────────────────────────────── */
QStatusBar {{
    background-color: {COLORS['surface']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding: 2px 8px;
}}

/* ── Menu bar ────────────────────────────────────────── */
QMenuBar {{
    background-color: {COLORS['surface']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 2px 0;
}}
QMenuBar::item {{
    padding: 6px 12px;
    border-radius: 4px;
}}
QMenuBar::item:selected {{
    background-color: {COLORS['selection']};
    color: {COLORS['primary']};
}}
QMenu {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {COLORS['selection']};
    color: {COLORS['primary']};
}}

/* ── Form labels ─────────────────────────────────────── */
QFormLayout QLabel {{
    color: {COLORS['text_secondary']};
    font-weight: 500;
}}

/* ── Tooltips ────────────────────────────────────────── */
QToolTip {{
    background-color: {COLORS['text']};
    color: {COLORS['text_on_primary']};
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
}}
"""

# ── Reusable style helpers ─────────────────────────────────────────────

def btn_primary():
    """Primary action button (e.g. Save)."""
    return (
        f"QPushButton {{ background-color: {COLORS['primary']}; color: {COLORS['text_on_primary']}; "
        f"font-weight: 600; border: none; border-radius: 6px; padding: 8px 20px; }}"
        f"QPushButton:hover {{ background-color: {COLORS['primary_hover']}; }}"
        f"QPushButton:pressed {{ background-color: #1D4ED8; }}"
    )

def btn_accent():
    """Accent / success button (e.g. Import from Library)."""
    return (
        f"QPushButton {{ background-color: {COLORS['accent']}; color: {COLORS['text_on_primary']}; "
        f"font-weight: 600; border: none; border-radius: 6px; padding: 8px 20px; }}"
        f"QPushButton:hover {{ background-color: {COLORS['accent_hover']}; }}"
        f"QPushButton:pressed {{ background-color: #047857; }}"
    )

def btn_danger():
    """Danger / destructive button."""
    return (
        f"QPushButton {{ background-color: {COLORS['error']}; color: {COLORS['text_on_primary']}; "
        f"font-weight: 600; border: none; border-radius: 6px; padding: 8px 20px; }}"
        f"QPushButton:hover {{ background-color: #DC2626; }}"
        f"QPushButton:pressed {{ background-color: #B91C1C; }}"
    )

def btn_outline():
    """Outline / secondary button."""
    return (
        f"QPushButton {{ background-color: transparent; color: {COLORS['primary']}; "
        f"font-weight: 600; border: 2px solid {COLORS['primary']}; border-radius: 6px; padding: 7px 18px; }}"
        f"QPushButton:hover {{ background-color: {COLORS['primary_light']}; }}"
    )

def info_banner():
    """Informational banner style (e.g. hints, disclaimers)."""
    return (
        f"background-color: {COLORS['warning_light']}; color: {COLORS['warning_text']}; "
        f"padding: 10px 14px; border-radius: 6px; border-left: 4px solid {COLORS['warning']};"
    )

def section_title():
    """Style for prominent section titles / car name."""
    return (
        f"font-size: 20px; font-weight: 700; color: {COLORS['text']};"
    )

def muted_text():
    """Style for secondary/muted text (e.g. speed labels)."""
    return f"color: {COLORS['text_muted']}; font-style: italic;"

def card_style():
    """Style for a card-like panel."""
    return (
        f"background-color: {COLORS['surface']}; "
        f"border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 16px;"
    )
