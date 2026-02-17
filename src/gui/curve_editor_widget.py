"""
Curve Editor Widget for editing LUT files visually.

This widget provides an interactive matplotlib-based editor for .lut files.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QTableWidget, QTableWidgetItem, QSplitter,
                              QLabel, QSpinBox, QDoubleSpinBox, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from core.lut_parser import LUTCurve


class CurveEditorWidget(QWidget):
    """Interactive widget for editing LUT curves."""
    
    # Signal emitted when curve data changes
    curve_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.curve = LUTCurve()
        self.selected_point_index = None
        self.dragging = False
        
        # Axis labels (can be customized)
        self.x_label = "X"
        self.y_label = "Y"
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create splitter for graph and table
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side: Matplotlib graph
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # Add navigation toolbar for zoom/pan
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.add_point_btn = QPushButton("Add Point")
        self.add_point_btn.clicked.connect(self.show_add_point_dialog)
        button_layout.addWidget(self.add_point_btn)
        
        self.remove_point_btn = QPushButton("Remove Point")
        self.remove_point_btn.clicked.connect(self.remove_selected_point)
        self.remove_point_btn.setEnabled(False)
        button_layout.addWidget(self.remove_point_btn)
        
        button_layout.addStretch()
        graph_layout.addLayout(button_layout)
        
        splitter.addWidget(graph_widget)
        
        # Right side: Table view
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        table_layout.addWidget(QLabel("Data Points:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["X", "Y"])
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        self.table.itemChanged.connect(self.on_table_item_changed)
        table_layout.addWidget(self.table)
        
        # Add point form
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("X:"))
        self.x_input = QDoubleSpinBox()
        self.x_input.setRange(-999999, 999999)
        self.x_input.setDecimals(2)
        form_layout.addWidget(self.x_input)
        
        form_layout.addWidget(QLabel("Y:"))
        self.y_input = QDoubleSpinBox()
        self.y_input.setRange(-999999, 999999)
        self.y_input.setDecimals(4)
        form_layout.addWidget(self.y_input)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_point_from_form)
        form_layout.addWidget(add_btn)
        
        table_layout.addLayout(form_layout)
        
        splitter.addWidget(table_widget)
        
        # Set splitter sizes (60% graph, 40% table)
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
        
        # Connect mouse events for dragging
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        # Connect key events for deletion
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        
    def set_axis_labels(self, x_label, y_label):
        """Set the axis labels for the graph."""
        self.x_label = x_label
        self.y_label = y_label
        self.plot_curve()
        
    def load_curve(self, lut_curve):
        """Load a LUT curve into the editor."""
        self.curve = lut_curve
        self.selected_point_index = None
        self.update_table()
        self.plot_curve()
        
    def get_curve(self):
        """Get the current LUT curve."""
        return self.curve
        
    def update_table(self):
        """Update the table with current curve points."""
        self.table.itemChanged.disconnect(self.on_table_item_changed)
        
        points = self.curve.get_points()
        self.table.setRowCount(len(points))
        
        for i, (x, y) in enumerate(points):
            self.table.setItem(i, 0, QTableWidgetItem(str(x)))
            self.table.setItem(i, 1, QTableWidgetItem(str(y)))
            
        self.table.itemChanged.connect(self.on_table_item_changed)
        
    def plot_curve(self):
        """Plot the curve on the matplotlib canvas."""
        self.ax.clear()
        
        points = self.curve.get_points()
        if not points:
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return
            
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        
        # Plot the curve
        self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Curve')
        
        # Plot the points
        if self.selected_point_index is not None:
            # Highlight selected point
            for i, (x, y) in enumerate(points):
                if i == self.selected_point_index:
                    self.ax.plot(x, y, 'ro', markersize=10, label='Selected')
                else:
                    self.ax.plot(x, y, 'go', markersize=8)
        else:
            self.ax.plot(x_vals, y_vals, 'go', markersize=8, label='Points')
            
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        self.figure.tight_layout()
        self.canvas.draw()
        
    def on_mouse_press(self, event):
        """Handle mouse press event."""
        if event.inaxes != self.ax:
            return
            
        # Check if clicking on a point
        points = self.curve.get_points()
        if not points:
            return
            
        # Find nearest point
        min_dist = float('inf')
        nearest_idx = None
        
        for i, (x, y) in enumerate(points):
            # Transform to display coordinates for accurate distance
            display_point = self.ax.transData.transform((x, y))
            display_click = self.ax.transData.transform((event.xdata, event.ydata))
            dist = ((display_point[0] - display_click[0])**2 + 
                   (display_point[1] - display_click[1])**2)**0.5
            
            if dist < min_dist:
                min_dist = dist
                nearest_idx = i
                
        # Select point if close enough (within 10 pixels)
        if min_dist < 10:
            self.selected_point_index = nearest_idx
            self.dragging = True
            self.remove_point_btn.setEnabled(True)
            
            # Update table selection
            self.table.selectRow(nearest_idx)
            
            self.plot_curve()
            
    def on_mouse_release(self, event):
        """Handle mouse release event."""
        if self.dragging:
            self.dragging = False
            self.curve_changed.emit()
            
    def on_mouse_move(self, event):
        """Handle mouse move event for dragging."""
        if not self.dragging or self.selected_point_index is None:
            return
            
        if event.inaxes != self.ax:
            return
            
        # Update point position
        new_x = event.xdata
        new_y = event.ydata
        
        self.curve.update_point(self.selected_point_index, new_x, new_y)
        self.curve.sort_points()
        
        # Find new index after sorting
        points = self.curve.get_points()
        for i, (x, y) in enumerate(points):
            if abs(x - new_x) < 0.001 and abs(y - new_y) < 0.001:
                self.selected_point_index = i
                break
                
        self.update_table()
        self.plot_curve()
        
    def on_key_press(self, event):
        """Handle key press events."""
        if event.key == 'delete' and self.selected_point_index is not None:
            self.remove_selected_point()
            
    def show_add_point_dialog(self):
        """Show dialog to add a new point."""
        # Just focus on the input fields
        self.x_input.setFocus()
        
    def add_point_from_form(self):
        """Add a point from the form inputs."""
        x = self.x_input.value()
        y = self.y_input.value()
        
        self.curve.add_point(x, y)
        self.curve.sort_points()
        
        self.update_table()
        self.plot_curve()
        self.curve_changed.emit()
        
    def remove_selected_point(self):
        """Remove the currently selected point."""
        if self.selected_point_index is None:
            return
            
        points = self.curve.get_points()
        if len(points) <= 1:
            QMessageBox.warning(self, "Cannot Remove", 
                              "Cannot remove the last point. A curve must have at least one point.")
            return
            
        self.curve.remove_point(self.selected_point_index)
        self.selected_point_index = None
        self.remove_point_btn.setEnabled(False)
        
        self.update_table()
        self.plot_curve()
        self.curve_changed.emit()
        
    def on_table_selection_changed(self):
        """Handle table selection changes."""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            self.selected_point_index = selected_rows[0].row()
            self.remove_point_btn.setEnabled(True)
            self.plot_curve()
        else:
            self.selected_point_index = None
            self.remove_point_btn.setEnabled(False)
            
    def on_table_item_changed(self, item):
        """Handle manual table edits."""
        row = item.row()
        col = item.column()
        
        try:
            value = float(item.text())
            
            points = self.curve.get_points()
            if row < len(points):
                x, y = points[row]
                if col == 0:  # X value changed
                    self.curve.update_point(row, value, y)
                else:  # Y value changed
                    self.curve.update_point(row, x, value)
                    
                self.curve.sort_points()
                self.update_table()
                self.plot_curve()
                self.curve_changed.emit()
                
        except ValueError:
            # Invalid number, revert
            self.update_table()
