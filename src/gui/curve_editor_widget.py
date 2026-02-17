"""
Curve Editor Widget for editing LUT files visually.

This widget provides an interactive matplotlib-based editor for .lut files.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QTableWidget, QTableWidgetItem, QSplitter,
                              QLabel, QSpinBox, QDoubleSpinBox, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

from core.lut_parser import LUTCurve


class CustomNavigationToolbar(NavigationToolbar):
    """Custom toolbar with limited buttons."""
    
    # Only include home, back, forward, and save buttons
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Save')]


class CurveEditorWidget(QWidget):
    """Interactive widget for editing LUT curves."""
    
    # Signal emitted when curve data changes
    curve_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.curve = LUTCurve()
        self.selected_point_index = None
        self.dragging = False
        self.zoom_factor = 1.1  # Zoom factor for mouse wheel
        self.drag_axis_limits = None  # Store axis limits during drag to prevent auto-scaling
        self.smooth_curve = False  # Enable smooth curve interpolation
        
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
        
        # Add custom navigation toolbar (without zoom/pan/configure buttons)
        self.toolbar = CustomNavigationToolbar(self.canvas, self)
        
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        
        # Control buttons (removed "Add Point" button as requested)
        button_layout = QHBoxLayout()
        
        self.remove_point_btn = QPushButton("Remove Point")
        self.remove_point_btn.clicked.connect(self.remove_selected_point)
        self.remove_point_btn.setEnabled(False)
        button_layout.addWidget(self.remove_point_btn)
        
        # Add smooth curve checkbox
        self.smooth_curve_checkbox = QCheckBox("Smooth Curve (Spline)")
        self.smooth_curve_checkbox.stateChanged.connect(self.on_smooth_curve_changed)
        button_layout.addWidget(self.smooth_curve_checkbox)
        
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
        
        # Add point form (changed to integer spinboxes)
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("X:"))
        self.x_input = QSpinBox()
        self.x_input.setRange(-999999, 999999)
        form_layout.addWidget(self.x_input)
        
        form_layout.addWidget(QLabel("Y:"))
        self.y_input = QSpinBox()
        self.y_input.setRange(-999999, 999999)
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
        self.canvas.mpl_connect('scroll_event', self.on_scroll)  # Mouse wheel zoom
        
        # Connect key events for deletion and zoom
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
            # Round to integers for display
            self.table.setItem(i, 0, QTableWidgetItem(str(int(round(x)))))
            self.table.setItem(i, 1, QTableWidgetItem(str(int(round(y)))))
            
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
        if self.smooth_curve and len(points) >= 4:
            # Use cubic spline interpolation for smooth curve
            # Need at least 4 points for cubic spline
            try:
                # Create interpolation function
                f = interpolate.interp1d(x_vals, y_vals, kind='cubic', fill_value='extrapolate')
                
                # Generate smooth curve points
                x_min, x_max = min(x_vals), max(x_vals)
                x_smooth = np.linspace(x_min, x_max, 200)
                y_smooth = f(x_smooth)
                
                # Plot smooth curve
                self.ax.plot(x_smooth, y_smooth, 'b-', linewidth=2, alpha=0.7)
            except Exception as e:
                # Fallback to linear if spline fails
                print(f"Spline interpolation failed: {e}")
                self.ax.plot(x_vals, y_vals, 'b-', linewidth=2)
        else:
            # Plot linear curve
            self.ax.plot(x_vals, y_vals, 'b-', linewidth=2)
        
        # Plot the data points
        if self.selected_point_index is not None:
            # Highlight selected point
            for i, (x, y) in enumerate(points):
                if i == self.selected_point_index:
                    self.ax.plot(x, y, 'ro', markersize=10)
                else:
                    self.ax.plot(x, y, 'go', markersize=8)
        else:
            self.ax.plot(x_vals, y_vals, 'go', markersize=8)
            
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.grid(True, alpha=0.3)
        
        # Restore axis limits if dragging to prevent auto-scaling
        if self.drag_axis_limits is not None:
            self.ax.set_xlim(self.drag_axis_limits['xlim'])
            self.ax.set_ylim(self.drag_axis_limits['ylim'])
        
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
            
            # Store current axis limits to prevent auto-scaling during drag
            self.drag_axis_limits = {
                'xlim': self.ax.get_xlim(),
                'ylim': self.ax.get_ylim()
            }
            
            # Disable toolbar navigation to prevent graph panning during drag
            if hasattr(self.toolbar, 'mode') and self.toolbar.mode:
                self.toolbar.mode = ''
            
            # Update table selection
            self.table.selectRow(nearest_idx)
            
            self.plot_curve()
            
    def on_mouse_release(self, event):
        """Handle mouse release event."""
        if self.dragging:
            self.dragging = False
            self.drag_axis_limits = None  # Clear stored limits after drag completes
            self.curve_changed.emit()
            
    def on_mouse_move(self, event):
        """Handle mouse move event for dragging."""
        if not self.dragging or self.selected_point_index is None:
            return
            
        if event.inaxes != self.ax:
            return
            
        # Update point position (round to integer)
        new_x = round(event.xdata)
        new_y = round(event.ydata)
        
        self.curve.update_point(self.selected_point_index, new_x, new_y)
        self.curve.sort_points()
        
        # Find new index after sorting
        points = self.curve.get_points()
        for i, (x, y) in enumerate(points):
            if abs(x - new_x) < 0.5 and abs(y - new_y) < 0.5:
                self.selected_point_index = i
                break
                
        self.update_table()
        self.plot_curve()
        
    def on_key_press(self, event):
        """Handle key press events."""
        if event.key == 'delete' and self.selected_point_index is not None:
            self.remove_selected_point()
        elif event.key == '+' or event.key == '=':
            # Zoom in
            self.zoom(self.zoom_factor)
        elif event.key == '-' or event.key == '_':
            # Zoom out
            self.zoom(1 / self.zoom_factor)
    
    def on_scroll(self, event):
        """Handle mouse wheel scroll for zooming."""
        if event.inaxes != self.ax:
            return
        
        # Zoom in or out based on scroll direction
        if event.button == 'up':
            scale_factor = self.zoom_factor
        elif event.button == 'down':
            scale_factor = 1 / self.zoom_factor
        else:
            return
        
        # Get the current axis limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Get mouse position in data coordinates
        xdata = event.xdata
        ydata = event.ydata
        
        # Calculate new limits centered on mouse position
        new_width = (xlim[1] - xlim[0]) / scale_factor
        new_height = (ylim[1] - ylim[0]) / scale_factor
        
        relx = (xlim[1] - xdata) / (xlim[1] - xlim[0])
        rely = (ylim[1] - ydata) / (ylim[1] - ylim[0])
        
        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        
        self.canvas.draw()
    
    def zoom(self, scale_factor):
        """Zoom in or out by scale_factor."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Calculate center of current view
        xcenter = (xlim[0] + xlim[1]) / 2
        ycenter = (ylim[0] + ylim[1]) / 2
        
        # Calculate new limits
        new_width = (xlim[1] - xlim[0]) / scale_factor
        new_height = (ylim[1] - ylim[0]) / scale_factor
        
        self.ax.set_xlim([xcenter - new_width / 2, xcenter + new_width / 2])
        self.ax.set_ylim([ycenter - new_height / 2, ycenter + new_height / 2])
        
        self.canvas.draw()
            
    def add_point_from_form(self):
        """Add a point from the form inputs."""
        x = int(self.x_input.value())
        y = int(self.y_input.value())
        
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
            value = int(item.text())  # Parse as integer
            
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
    
    def on_smooth_curve_changed(self, state):
        """Handle smooth curve checkbox state change."""
        self.smooth_curve = (state == Qt.Checked)
        self.plot_curve()
