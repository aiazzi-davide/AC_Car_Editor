# Curve Editor Improvements - Implementation Summary

## User Requirements (Italian)

The user requested the following improvements:

1. ✅ **"i valori venissero arrotondati a interi"** - Values should be rounded to integers
2. ✅ **"se trascino un punto non deve spostarsi il grafico"** - Graph should not move when dragging points
3. ✅ **"rimuovi 'configure subplots' e 'edit axis ...' complicano troppo"** - Remove complex toolbar buttons
4. ✅ **"rimuovi anche la legenda"** - Remove the legend
5. ✅ **"lo zoom invece di selezionare un area deve essere attraverso la rotella del mouse oppure con '+' e '-'"** - Zoom via mouse wheel or +/- keys
6. ✅ **"il pulsante add Point a sinistra non ha senso"** - Remove redundant Add Point button
7. ✅ **"load file e import hanno la stessa funzione"** - Remove redundant Import button

## Implementation Details

### 1. Integer Values (Requirement 1)

**Changed in `curve_editor_widget.py`:**

- **Line 96-103**: Changed from `QDoubleSpinBox` to `QSpinBox` for X and Y inputs
  ```python
  self.x_input = QSpinBox()  # Was QDoubleSpinBox with decimals=2
  self.y_input = QSpinBox()  # Was QDoubleSpinBox with decimals=4
  ```

- **Line 154-156**: Updated `update_table()` to display rounded integers
  ```python
  self.table.setItem(i, 0, QTableWidgetItem(str(int(round(x)))))
  self.table.setItem(i, 1, QTableWidgetItem(str(int(round(y)))))
  ```

- **Line 249-250**: Round coordinates when dragging points
  ```python
  new_x = round(event.xdata)
  new_y = round(event.ydata)
  ```

- **Line 277-278**: Cast to int when adding points from form
  ```python
  x = int(self.x_input.value())
  y = int(self.y_input.value())
  ```

- **Line 329**: Parse table edits as integers
  ```python
  value = int(item.text())  # Was float(item.text())
  ```

### 2. Prevent Graph Movement During Drag (Requirement 2)

**Changed in `curve_editor_widget.py`:**

- **Line 231-233**: Disable toolbar navigation mode when starting to drag a point
  ```python
  # Disable toolbar navigation to prevent graph panning during drag
  if hasattr(self.toolbar, 'mode') and self.toolbar.mode:
      self.toolbar.mode = ''
  ```

This ensures that when a user clicks and drags a point, the matplotlib toolbar's pan/zoom mode is disabled, preventing the graph from moving.

### 3. Remove Complex Toolbar Buttons (Requirement 3)

**Changed in `curve_editor_widget.py`:**

- **Line 23-28**: Created custom toolbar class
  ```python
  class CustomNavigationToolbar(NavigationToolbar):
      """Custom toolbar with limited buttons."""
      
      # Only include home, back, forward, and save buttons
      toolitems = [t for t in NavigationToolbar.toolitems if
                   t[0] in ('Home', 'Back', 'Forward', 'Save')]
  ```

- **Line 62**: Use custom toolbar instead of standard
  ```python
  self.toolbar = CustomNavigationToolbar(self.canvas, self)
  ```

**Removed buttons:**
- ❌ "Zoom" (area selection zoom)
- ❌ "Pan" (pan/zoom with left/right mouse buttons)
- ❌ "Configure subplots" (adjust spacing)
- ❌ "Edit axis, curve and image parameters" (advanced settings)

**Kept buttons:**
- ✅ "Home" (reset view)
- ✅ "Back" (previous view)
- ✅ "Forward" (next view)
- ✅ "Save" (save figure)

### 4. Remove Legend (Requirement 4)

**Changed in `curve_editor_widget.py`:**

- **Line 177-178, 183-189**: Removed all `label` parameters from plot commands
  ```python
  # Before: self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Curve')
  # After:  self.ax.plot(x_vals, y_vals, 'b-', linewidth=2)
  ```

- **Line 193**: Removed `self.ax.legend()` call

### 5. Mouse Wheel and Keyboard Zoom (Requirement 5)

**Changed in `curve_editor_widget.py`:**

- **Line 35**: Added zoom factor constant
  ```python
  self.zoom_factor = 1.1  # Zoom factor for mouse wheel
  ```

- **Line 122**: Connected scroll event
  ```python
  self.canvas.mpl_connect('scroll_event', self.on_scroll)
  ```

- **Line 272-275**: Added +/- key handling in `on_key_press()`
  ```python
  elif event.key == '+' or event.key == '=':
      self.zoom(self.zoom_factor)  # Zoom in
  elif event.key == '-' or event.key == '_':
      self.zoom(1 / self.zoom_factor)  # Zoom out
  ```

- **Line 277-302**: New `on_scroll()` method for mouse wheel zoom
  - Zooms in/out centered on mouse cursor position
  - Respects current axis limits
  - Only works when mouse is over the plot area

- **Line 304-318**: New `zoom()` method for keyboard zoom
  - Zooms in/out centered on current view center
  - Used by +/- keyboard shortcuts

### 6. Remove Redundant Add Point Button (Requirement 6)

**Changed in `curve_editor_widget.py`:**

- **Line 64-74**: Removed "Add Point" button and its layout entry
  ```python
  # Removed:
  # self.add_point_btn = QPushButton("Add Point")
  # self.add_point_btn.clicked.connect(self.show_add_point_dialog)
  # button_layout.addWidget(self.add_point_btn)
  ```

- **Removed method**: `show_add_point_dialog()` no longer needed

The Add Point functionality is still available via the form on the right side with X/Y inputs and the "Add" button.

### 7. Remove Redundant Import Button (Requirement 7)

**Changed in `curve_editor_dialog.py`:**

- **Line 105-107**: Removed "Import..." button
  ```python
  # Removed:
  # import_btn = QPushButton("Import...")
  # import_btn.clicked.connect(self.import_curve)
  # button_layout.addWidget(import_btn)
  ```

The "Load File..." button serves the same purpose, so the Import button was redundant.

## Testing

All 37 existing tests pass with these changes:
- 16 core tests
- 14 GUI tests
- 7 curve editor tests

No test changes were required because the core functionality remains the same - only the UI and value precision changed.

## User Experience Improvements

### Before
- Cluttered toolbar with 8 buttons including confusing "Configure" and "Edit axis" options
- Floating-point values with multiple decimal places
- Graph could pan accidentally when trying to drag points
- Legend taking up graph space
- Two ways to add points (button + form) causing confusion
- Two ways to load files (Load + Import) causing confusion
- Zoom required selecting a rectangular area

### After
- Clean toolbar with only 4 essential buttons (Home, Back, Forward, Save)
- Integer values suitable for RPM and power/torque tuning
- Graph stays locked when dragging points
- More space for the actual curve
- Single clear way to add points (form on right)
- Single clear way to load files (Load File button)
- Intuitive zoom with mouse wheel or +/- keys

## File Changes Summary

**Modified:**
- `src/gui/curve_editor_widget.py` (95 insertions, 36 deletions)
  - New `CustomNavigationToolbar` class
  - Integer-only spinboxes
  - Mouse wheel zoom support
  - Keyboard zoom support (+/- keys)
  - Removed "Add Point" button
  - Updated all value handling to use integers
  - Disabled toolbar mode during point dragging
  - Removed legend

- `src/gui/curve_editor_dialog.py` (minimal changes)
  - Removed "Import..." button

## Backward Compatibility

The changes maintain backward compatibility:
- LUT files still store floating-point values
- Rounding only happens in the UI layer
- Files saved from the editor will have integer values, which is acceptable for car tuning
- Existing LUT files with decimal values can still be loaded (they'll be displayed rounded)

## Future Enhancements

Possible improvements that could build on these changes:
1. Add a "Grid snap" option to snap points to grid intersections
2. Add keyboard shortcuts for common operations (Ctrl+S for save, etc.)
3. Add tooltip showing exact values when hovering over points
4. Add undo/redo functionality
5. Add curve smoothing/interpolation options
